from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from ...database import get_db
from ... import models, schemas, auth, crud

router = APIRouter(dependencies=[Depends(auth.get_current_admin)])

# ==================== USER MANAGEMENT (HỌC VIÊN) ====================

@router.get("/users", response_model=List[schemas.UserAdminResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.post("/users", response_model=schemas.UserAdminResponse, status_code=status.HTTP_201_CREATED)
def create_user_admin(user_in: schemas.UserAdminCreate, db: Session = Depends(get_db)):
    # Check if email exists
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã tồn tại trên hệ thống!"
        )

    hashed_pwd = auth.get_password_hash(user_in.password)
    unique_ref = f"ACC-{uuid.uuid4().hex[:6].upper()}"
    
    db_user = models.User(
        fullname=user_in.fullname,
        email=user_in.email,
        hashed_password=hashed_pwd,
        referral_code=unique_ref,
        referred_by_id=user_in.referred_by_id,
        role=user_in.role,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/users/{id}", response_model=schemas.UserAdminResponse)
def update_user_admin(id: int, user_in: schemas.UserAdminUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Học viên không tồn tại"
        )
    
    if user_in.fullname is not None:
        db_user.fullname = user_in.fullname
    if user_in.email is not None and user_in.email != db_user.email:
        existing_user = db.query(models.User).filter(models.User.email == user_in.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email này đã được sử dụng bởi tài khoản khác."
            )
        db_user.email = user_in.email
    if user_in.role is not None:
        db_user.role = user_in.role
    if user_in.is_active is not None:
        db_user.is_active = user_in.is_active
    if user_in.referred_by_id is not None:
        db_user.referred_by_id = user_in.referred_by_id if user_in.referred_by_id != 0 else None
        
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{id}", status_code=status.HTTP_200_OK)
def delete_user_admin(id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Học viên không tồn tại"
        )
    order_count = db.query(models.Order).filter(models.Order.user_id == id).count()
    if order_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Học viên đang có {order_count} đơn hàng. Không thể xóa."
        )
    db.delete(db_user)
    db.commit()
    return {"message": "Đã xóa học viên thành công"}


# ==================== ORDER MANAGEMENT (ĐƠN HÀNG) ====================

@router.get("/orders", response_model=List[schemas.OrderAdminResponse])
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    res = []
    for o in orders:
        res.append({
            "id": o.id,
            "user_id": o.user_id,
            "user_fullname": o.user.fullname if o.user else "Unknown User",
            "user_email": o.user.email if o.user else "unknown@domain.com",
            "total_price": o.total_price,
            "discount_applied": o.discount_applied,
            "status": o.status,
            "created_at": o.created_at,
            "items": o.items
        })
    return res

@router.post("/orders", response_model=schemas.OrderAdminResponse, status_code=status.HTTP_201_CREATED)
def create_order_admin(order_in: schemas.OrderAdminCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == order_in.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Học viên không tồn tại"
        )
        
    db_order = models.Order(
        user_id=order_in.user_id,
        total_price=order_in.total_price,
        discount_applied=order_in.discount_applied,
        status=order_in.status
    )
    db.add(db_order)
    db.flush()
    
    for cid in order_in.course_ids:
        course = db.query(models.Course).filter(models.Course.id == cid).first()
        if course:
            db_item = models.OrderItem(
                order_id=db_order.id,
                course_id=cid,
                price=course.price
            )
            db.add(db_item)
            
    db.commit()
    db.refresh(db_order)
    
    # Return formatted order response
    return {
        "id": db_order.id,
        "user_id": db_order.user_id,
        "user_fullname": user.fullname,
        "user_email": user.email,
        "total_price": db_order.total_price,
        "discount_applied": db_order.discount_applied,
        "status": db_order.status,
        "created_at": db_order.created_at,
        "items": db_order.items
    }

@router.put("/orders/{id}", response_model=schemas.OrderAdminResponse)
def update_order_admin(id: int, order_in: schemas.OrderAdminUpdate, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == id).first()
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Đơn hàng không tồn tại"
        )
        
    if order_in.status is not None:
        # Handle referral reward when transitioning to paid
        if order_in.status == "paid" and db_order.status != "paid":
            user = db_order.user
            if user and user.referred_by_id:
                referrer = db.query(models.User).filter(models.User.id == user.referred_by_id).first()
                if referrer:
                    total_earned = 0
                    for item in db_order.items:
                        comm_pct = crud.get_commission_percent_for_user_course(db, referrer.id, item.course_id)
                        total_earned += int(item.price * (comm_pct / 100.0))

                    existing_referral = db.query(models.Referral).filter(
                        models.Referral.referred_id == user.id
                    ).first()

                    if not existing_referral:
                        db_referral = models.Referral(
                            referrer_id=referrer.id,
                            referred_id=user.id,
                            commission_amount=total_earned,
                            status="completed"
                        )
                        db.add(db_referral)
                    else:
                        existing_referral.commission_amount += total_earned

                    referrer.store_credit_balance += total_earned

        db_order.status = order_in.status
        
    if order_in.discount_applied is not None:
        db_order.discount_applied = order_in.discount_applied
    if order_in.total_price is not None:
        db_order.total_price = order_in.total_price
        
    if order_in.course_ids is not None:
        # Recreate order items
        db.query(models.OrderItem).filter(models.OrderItem.order_id == id).delete()
        for cid in order_in.course_ids:
            course = db.query(models.Course).filter(models.Course.id == cid).first()
            if course:
                db_item = models.OrderItem(
                    order_id=id,
                    course_id=cid,
                    price=course.price
                )
                db.add(db_item)
                
    db.commit()
    db.refresh(db_order)
    
    return {
        "id": db_order.id,
        "user_id": db_order.user_id,
        "user_fullname": db_order.user.fullname if db_order.user else "Unknown User",
        "user_email": db_order.user.email if db_order.user else "unknown@domain.com",
        "total_price": db_order.total_price,
        "discount_applied": db_order.discount_applied,
        "status": db_order.status,
        "created_at": db_order.created_at,
        "items": db_order.items
    }

@router.delete("/orders/{id}", status_code=status.HTTP_200_OK)
def delete_order_admin(id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == id).first()
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Đơn hàng không tồn tại"
        )
    db.delete(db_order)
    db.commit()
    return {"message": "Đã xóa đơn hàng thành công"}


# ==================== CONTACT LEAD MANAGEMENT ====================

@router.get("/contacts", response_model=List[schemas.ContactResponse])
def get_all_contacts(db: Session = Depends(get_db)):
    return db.query(models.Contact).all()

@router.put("/contacts/{id}/resolve", response_model=schemas.ContactResponse)
def toggle_contact_resolved(id: int, db: Session = Depends(get_db)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == id).first()
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lời nhắn liên hệ không tồn tại"
        )
    db_contact.is_resolved = not db_contact.is_resolved
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.delete("/contacts/{id}", status_code=status.HTTP_200_OK)
def delete_contact_admin(id: int, db: Session = Depends(get_db)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == id).first()
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lời nhắn liên hệ không tồn tại"
        )
    db.delete(db_contact)
    db.commit()
    return {"message": "Đã xóa tin nhắn liên hệ thành công"}


# ==================== CATEGORY MANAGEMENT ====================

@router.get("/categories", response_model=List[schemas.CategoryResponse])
def get_categories_admin(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

@router.post("/categories", response_model=schemas.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category_admin(cat_in: schemas.CategoryCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Category).filter(models.Category.slug == cat_in.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Chuyên mục với mã Slug này đã tồn tại.")
    cat = models.Category(slug=cat_in.slug, name=cat_in.name)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

@router.put("/categories/{slug}", response_model=schemas.CategoryResponse)
def update_category_admin(slug: str, cat_in: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    cat = db.query(models.Category).filter(models.Category.slug == slug).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Không tìm thấy chuyên mục")
    cat.name = cat_in.name
    db.commit()
    db.refresh(cat)
    return cat

@router.delete("/categories/{slug}")
def delete_category_admin(slug: str, db: Session = Depends(get_db)):
    cat = db.query(models.Category).filter(models.Category.slug == slug).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Không tìm thấy chuyên mục")
    course_count = db.query(models.Course).filter(models.Course.category_slug == slug).count()
    if course_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Chuyên mục đang chứa {course_count} khóa học. Vui lòng di chuyển hoặc xóa khóa học trước khi xóa chuyên mục."
        )
    db.delete(cat)
    db.commit()
    return {"message": f"Đã xóa chuyên mục '{slug}' thành công"}


# ==================== COURSE CATALOG MANAGEMENT ====================

@router.post("/courses", response_model=schemas.CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course_admin(course_in: schemas.CourseAdminCreate, db: Session = Depends(get_db)):
    # Verify category slug exists
    cat = db.query(models.Category).filter(models.Category.slug == course_in.category_slug).first()
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Chuyên mục '{course_in.category_slug}' chưa tồn tại. Vui lòng tạo chuyên mục trước."
        )

    # Check duplicate handle
    existing_handle = db.query(models.Course).filter(models.Course.handle == course_in.handle).first()
    if existing_handle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Mã đường dẫn tĩnh (Slug / Handle) '{course_in.handle}' này đã được sử dụng bởi khóa học '{existing_handle.title}'. Vui lòng đổi Slug khác!"
        )

    # Generate big integer ID if not provided
    max_id = db.query(func.max(models.Course.id)).scalar() or 0
    cid = max_id + 1
    
    db_course = models.Course(
        id=cid,
        title=course_in.title,
        category_slug=course_in.category_slug,
        program_id=course_in.program_id,
        handle=course_in.handle,
        price=course_in.price,
        original_price=course_in.original_price,
        image=course_in.image,
        cover_image=course_in.cover_image,
        description=course_in.description,
        duration=course_in.duration,
        level=course_in.level,
        curriculum_data=course_in.curriculum_data,
        outcomes=course_in.outcomes,
        requirements=course_in.requirements,
        custom_roadmap=course_in.custom_roadmap,
        lecturer_ids=course_in.lecturer_ids
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.put("/courses/{id}", response_model=schemas.CourseResponse)
def update_course_admin(id: int, course_in: schemas.CourseAdminUpdate, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == id).first()
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Khóa học không tồn tại"
        )

    if course_in.title is not None:
        db_course.title = course_in.title
    if course_in.category_slug is not None:
        db_course.category_slug = course_in.category_slug
    if course_in.program_id is not None:
        db_course.program_id = course_in.program_id
    if course_in.handle is not None and course_in.handle != db_course.handle:
        existing_handle = db.query(models.Course).filter(models.Course.handle == course_in.handle).first()
        if existing_handle:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mã đường dẫn tĩnh (Slug / Handle) '{course_in.handle}' đã trùng với khóa học '{existing_handle.title}'. Vui lòng đổi tên hoặc Slug khác!"
            )
        db_course.handle = course_in.handle
    if course_in.price is not None:
        db_course.price = course_in.price
    if course_in.original_price is not None:
        db_course.original_price = course_in.original_price
    if course_in.image is not None:
        db_course.image = course_in.image
    if course_in.cover_image is not None:
        db_course.cover_image = course_in.cover_image
    if course_in.description is not None:
        db_course.description = course_in.description
    if course_in.duration is not None:
        db_course.duration = course_in.duration
    if course_in.level is not None:
        db_course.level = course_in.level
    if course_in.curriculum_data is not None:
        db_course.curriculum_data = course_in.curriculum_data
    if course_in.outcomes is not None:
        db_course.outcomes = course_in.outcomes
    if course_in.requirements is not None:
        db_course.requirements = course_in.requirements
    if course_in.custom_roadmap is not None:
        db_course.custom_roadmap = course_in.custom_roadmap
    if course_in.lecturer_ids is not None:
        db_course.lecturer_ids = course_in.lecturer_ids
        
    db.commit()
    db.refresh(db_course)
    return db_course
@router.get("/courses/{id}/related-summary")
def get_course_related_summary_admin(id: int, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == id).first()
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Khóa học không tồn tại"
        )
    
    enrollments_count = db.query(models.Enrollment).filter(models.Enrollment.course_id == id).count()
    reviews_count = db.query(models.CourseReview).filter(models.CourseReview.course_id == id).count()
    notes_count = db.query(models.LessonNote).filter(models.LessonNote.course_id == id).count()
    wishlists_count = db.query(models.Wishlist).filter(models.Wishlist.course_id == id).count()
    cart_count = db.query(models.CartItem).filter(models.CartItem.course_id == id).count()
    order_items_count = db.query(models.OrderItem).filter(models.OrderItem.course_id == id).count()

    return {
        "course_title": db_course.title,
        "enrollments_count": enrollments_count,
        "reviews_count": reviews_count,
        "notes_count": notes_count,
        "wishlists_count": wishlists_count,
        "cart_count": cart_count,
        "order_items_count": order_items_count
    }

@router.delete("/courses/{id}", status_code=status.HTTP_200_OK)
def delete_course_admin(id: int, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == id).first()
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Khóa học không tồn tại"
        )

    # Clean up related child records first to prevent FK constraint failures
    from sqlalchemy import text
    params = {"id": id}
    db.execute(text("DELETE FROM course_tags WHERE course_id = :id"), params)
    db.execute(text("DELETE FROM enrollments WHERE course_id = :id"), params)
    db.execute(text("DELETE FROM cart_items WHERE course_id = :id"), params)
    db.execute(text("DELETE FROM wishlists WHERE course_id = :id"), params)
    db.execute(text("DELETE FROM lesson_notes WHERE course_id = :id"), params)
    db.execute(text("DELETE FROM course_reviews WHERE course_id = :id"), params)
    db.execute(text("DELETE FROM user_course_commissions WHERE course_id = :id"), params)
    db.execute(text("DELETE FROM bundle_courses WHERE course_id = :id"), params)
    db.execute(text("DELETE FROM bundle_gift_courses WHERE course_id = :id"), params)
    db.execute(text("DELETE FROM order_items WHERE course_id = :id"), params)
    db.execute(text("DELETE FROM courses WHERE id = :id"), params)
    db.commit()
    return {"message": "Đã xóa khóa học thành công"}


# ==================== PROGRAM MANAGEMENT (CHƯƠNG TRÌNH ĐÀO TẠO) ====================

@router.get("/programs", response_model=List[schemas.ProgramResponse])
def get_all_programs_admin(db: Session = Depends(get_db)):
    return db.query(models.Program).all()

@router.post("/programs", response_model=schemas.ProgramResponse, status_code=status.HTTP_201_CREATED)
def create_program_admin(prog_in: schemas.ProgramCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Program).filter(models.Program.slug == prog_in.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slug chương trình đã tồn tại!"
        )
    db_prog = models.Program(
        title=prog_in.title,
        slug=prog_in.slug,
        description=prog_in.description,
        image=prog_in.image
    )
    db.add(db_prog)
    db.commit()
    db.refresh(db_prog)

    if prog_in.course_ids is not None:
        db.query(models.Course).filter(models.Course.program_id == db_prog.id).update({"program_id": None})
        if prog_in.course_ids:
            db.query(models.Course).filter(models.Course.id.in_(prog_in.course_ids)).update({"program_id": db_prog.id}, synchronize_session=False)
        db.commit()
        db.refresh(db_prog)

    return db_prog

@router.put("/programs/{id}", response_model=schemas.ProgramResponse)
def update_program_admin(id: int, prog_in: schemas.ProgramUpdate, db: Session = Depends(get_db)):
    db_prog = db.query(models.Program).filter(models.Program.id == id).first()
    if not db_prog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chương trình đào tạo không tồn tại"
        )
    if prog_in.title is not None:
        db_prog.title = prog_in.title
    if prog_in.slug is not None:
        db_prog.slug = prog_in.slug
    if prog_in.description is not None:
        db_prog.description = prog_in.description
    if prog_in.image is not None:
        db_prog.image = prog_in.image

    if prog_in.course_ids is not None:
        db.query(models.Course).filter(models.Course.program_id == id).update({"program_id": None})
        if prog_in.course_ids:
            db.query(models.Course).filter(models.Course.id.in_(prog_in.course_ids)).update({"program_id": id}, synchronize_session=False)

    db.commit()
    db.refresh(db_prog)
    return db_prog

@router.delete("/programs/{id}", status_code=status.HTTP_200_OK)
def delete_program_admin(id: int, db: Session = Depends(get_db)):
    db_prog = db.query(models.Program).filter(models.Program.id == id).first()
    if not db_prog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chương trình đào tạo không tồn tại"
        )
    db.query(models.Course).filter(models.Course.program_id == id).update({"program_id": None})
    db.commit()
    db.delete(db_prog)
    db.commit()
    return {"message": "Đã xóa chương trình đào tạo thành công"}


# ==================== BUNDLE MANAGEMENT (GÓI COMBO BUNDLE) ====================

@router.get("/bundles", response_model=List[schemas.BundleResponse])
def get_all_bundles_admin(db: Session = Depends(get_db)):
    return db.query(models.Bundle).all()

@router.post("/bundles", response_model=schemas.BundleResponse, status_code=status.HTTP_201_CREATED)
def create_bundle_admin(bundle_in: schemas.BundleCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Bundle).filter(models.Bundle.handle == bundle_in.handle).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Handle gói bundle đã tồn tại!"
        )
    db_bundle = models.Bundle(
        title=bundle_in.title,
        handle=bundle_in.handle,
        description=bundle_in.description,
        price=bundle_in.price,
        original_price=bundle_in.original_price,
        image=bundle_in.image
    )
    db.add(db_bundle)
    db.flush()

    if bundle_in.course_ids:
        courses = db.query(models.Course).filter(models.Course.id.in_(bundle_in.course_ids)).all()
        db_bundle.courses = courses

    if bundle_in.gift_course_ids:
        gift_courses = db.query(models.Course).filter(models.Course.id.in_(bundle_in.gift_course_ids)).all()
        db_bundle.gift_courses = gift_courses

    db.commit()
    db.refresh(db_bundle)
    return db_bundle

@router.put("/bundles/{id}", response_model=schemas.BundleResponse)
def update_bundle_admin(id: int, bundle_in: schemas.BundleUpdate, db: Session = Depends(get_db)):
    db_bundle = db.query(models.Bundle).filter(models.Bundle.id == id).first()
    if not db_bundle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gói combo bundle không tồn tại"
        )
    if bundle_in.title is not None:
        db_bundle.title = bundle_in.title
    if bundle_in.handle is not None:
        db_bundle.handle = bundle_in.handle
    if bundle_in.description is not None:
        db_bundle.description = bundle_in.description
    if bundle_in.price is not None:
        db_bundle.price = bundle_in.price
    if bundle_in.original_price is not None:
        db_bundle.original_price = bundle_in.original_price
    if bundle_in.image is not None:
        db_bundle.image = bundle_in.image

    if bundle_in.course_ids is not None:
        courses = db.query(models.Course).filter(models.Course.id.in_(bundle_in.course_ids)).all()
        db_bundle.courses = courses

    if bundle_in.gift_course_ids is not None:
        gift_courses = db.query(models.Course).filter(models.Course.id.in_(bundle_in.gift_course_ids)).all()
        db_bundle.gift_courses = gift_courses

    db.commit()
    db.refresh(db_bundle)
    return db_bundle

@router.delete("/bundles/{id}", status_code=status.HTTP_200_OK)
def delete_bundle_admin(id: int, db: Session = Depends(get_db)):
    db_bundle = db.query(models.Bundle).filter(models.Bundle.id == id).first()
    if not db_bundle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gói combo bundle không tồn tại"
        )
    db.delete(db_bundle)
    db.commit()
    return {"message": "Đã xóa gói combo bundle thành công"}

@router.put("/contact-settings", response_model=schemas.ContactSettingResponse)
def update_contact_settings(
    settings_in: schemas.ContactSettingUpdate,
    db: Session = Depends(get_db)
):
    db_settings = db.query(models.ContactSetting).first()
    if not db_settings:
        db_settings = models.ContactSetting()
        db.add(db_settings)
        db.commit()
        db.refresh(db_settings)
    
    if settings_in.address is not None:
        db_settings.address = settings_in.address
    if settings_in.hotline is not None:
        db_settings.hotline = settings_in.hotline
    if settings_in.email is not None:
        db_settings.email = settings_in.email
    if settings_in.zalo is not None:
        db_settings.zalo = settings_in.zalo
    if settings_in.viber is not None:
        db_settings.viber = settings_in.viber
        
    db.commit()
    db.refresh(db_settings)
    return db_settings

# ==================== HOME INTRO SETTINGS ====================

@router.get("/home-intro", response_model=schemas.HomeIntroSettingResponse)
def get_home_intro_settings_admin(db: Session = Depends(get_db)):
    settings = db.query(models.HomeIntroSetting).first()
    if not settings:
        settings = models.HomeIntroSetting()
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

@router.put("/home-intro", response_model=schemas.HomeIntroSettingResponse)
def update_home_intro_settings_admin(
    settings_in: schemas.HomeIntroSettingUpdate,
    db: Session = Depends(get_db)
):
    settings = db.query(models.HomeIntroSetting).first()
    if not settings:
        settings = models.HomeIntroSetting()
        db.add(settings)
        db.commit()
        db.refresh(settings)

    if settings_in.title is not None:
        settings.title = settings_in.title
    if settings_in.desc1 is not None:
        settings.desc1 = settings_in.desc1
    if settings_in.desc2 is not None:
        settings.desc2 = settings_in.desc2
    if settings_in.counter_number is not None:
        settings.counter_number = settings_in.counter_number
    if settings_in.counter_label is not None:
        settings.counter_label = settings_in.counter_label
    if settings_in.video_url is not None:
        settings.video_url = settings_in.video_url
    if settings_in.poster_url is not None:
        settings.poster_url = settings_in.poster_url
    if settings_in.btn_label is not None:
        settings.btn_label = settings_in.btn_label

    db.commit()
    db.refresh(settings)
    return settings

# ==================== BANNER MANAGEMENT ====================

@router.get("/banners", response_model=List[schemas.BannerResponse])
def get_all_banners_admin(db: Session = Depends(get_db)):
    return crud.get_banners(db, active_only=False)

@router.post("/banners", response_model=schemas.BannerResponse, status_code=status.HTTP_201_CREATED)
def create_banner_admin(banner_in: schemas.BannerCreate, db: Session = Depends(get_db)):
    return crud.create_banner(db, banner_in)

@router.put("/banners/{id}", response_model=schemas.BannerResponse)
def update_banner_admin(id: int, banner_in: schemas.BannerUpdate, db: Session = Depends(get_db)):
    updated = crud.update_banner(db, id, banner_in)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner không tồn tại"
        )
    return updated

@router.delete("/banners/{id}", status_code=status.HTTP_200_OK)
def delete_banner_admin(id: int, db: Session = Depends(get_db)):
    success = crud.delete_banner(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner không tồn tại"
        )
    return {"message": "Đã xóa banner thành công"}


# ==================== EXPORT EXCEL / CSV REPORTS ====================

from fastapi.responses import Response

@router.get("/export/orders")
def export_orders_csv(
    period: Optional[str] = "all",
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.Order)
    now = datetime.now(timezone.utc)
    if period == "month":
        query = query.filter(models.Order.created_at >= now - timedelta(days=30))
    elif period == "quarter":
        query = query.filter(models.Order.created_at >= now - timedelta(days=90))
    elif period == "year":
        query = query.filter(models.Order.created_at >= now - timedelta(days=365))
        
    orders = query.order_by(models.Order.id.desc()).all()
    lines = ["Mã Đơn,Tên Học Viên,Email,Tổng Tiền (VNĐ),Giảm Giá (VNĐ),Trạng Thái,Ngày Tạo"]
    for o in orders:
        uname = o.user.fullname.replace(",", " ") if o.user else "N/A"
        uemail = o.user.email if o.user else "N/A"
        created = o.created_at.strftime("%Y-%m-%d %H:%M:%S") if o.created_at else ""
        lines.append(f'"{o.id}","{uname}","{uemail}",{o.total_price},{o.discount_applied},"{o.status}","{created}"')
    
    csv_data = "\ufeff" + "\n".join(lines)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=danh_sach_don_hang_{period}_acc.csv"}
    )

@router.get("/export/users")
def export_users_csv(
    period: Optional[str] = "all",
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.User)
    now = datetime.now(timezone.utc)
    if period == "month":
        query = query.filter(models.User.created_at >= now - timedelta(days=30))
    elif period == "quarter":
        query = query.filter(models.User.created_at >= now - timedelta(days=90))
    elif period == "year":
        query = query.filter(models.User.created_at >= now - timedelta(days=365))

    users = query.order_by(models.User.id.desc()).all()
    lines = ["ID,Họ và Tên,Email,Mã Ref,Ví Giảm Giá (VNĐ),Vai Trò,Trạng Thái,Ngày Đăng Ký"]
    for u in users:
        uname = u.fullname.replace(",", " ")
        created = u.created_at.strftime("%Y-%m-%d %H:%M:%S") if u.created_at else ""
        st = "Hoạt động" if u.is_active else "Khoá"
        lines.append(f'"{u.id}","{uname}","{u.email}","{u.referral_code}",{u.store_credit_balance},"{u.role}","{st}","{created}"')

    csv_data = "\ufeff" + "\n".join(lines)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=danh_sach_hoc_vien_{period}_acc.csv"}
    )

@router.get("/export/revenue")
def export_revenue_csv(
    period: Optional[str] = "all",
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.Order).filter(models.Order.status == "paid")
    now = datetime.now(timezone.utc)
    if period == "month":
        query = query.filter(models.Order.created_at >= now - timedelta(days=30))
    elif period == "quarter":
        query = query.filter(models.Order.created_at >= now - timedelta(days=90))
    elif period == "year":
        query = query.filter(models.Order.created_at >= now - timedelta(days=365))

    paid_orders = query.order_by(models.Order.created_at.desc()).all()
    total_rev = sum(o.total_price for o in paid_orders)
    lines = [f"BÁO CÁO DOANH THU ACC ACADEMY ({period.upper()}),,,Tổng Doanh Thu: {total_rev:,} VNĐ", "Mã Đơn,Tên Học Viên,Email,Doanh Thu Đơn (VNĐ),Ngày Thanh Toán"]
    for o in paid_orders:
        uname = o.user.fullname.replace(",", " ") if o.user else "N/A"
        uemail = o.user.email if o.user else "N/A"
        created = o.created_at.strftime("%Y-%m-%d %H:%M:%S") if o.created_at else ""
        lines.append(f'"{o.id}","{uname}","{uemail}",{o.total_price},"{created}"')

    csv_data = "\ufeff" + "\n".join(lines)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=bao_cao_doanh_thu_{period}_acc.csv"}
    )


# ==================== LECTURER MAJOR MANAGEMENT ====================

@router.get("/lecturer-majors", response_model=List[schemas.LecturerMajorResponse])
def get_all_lecturer_majors_admin(db: Session = Depends(get_db)):
    return crud.get_lecturer_majors(db)

@router.post("/lecturer-majors", response_model=schemas.LecturerMajorResponse, status_code=status.HTTP_201_CREATED)
def create_lecturer_major_admin(major_in: schemas.LecturerMajorCreate, db: Session = Depends(get_db)):
    existing = crud.get_lecturer_major_by_id(db, major_in.id)
    if existing:
        raise HTTPException(status_code=400, detail="Mã chuyên ngành (ID) này đã tồn tại!")
    return crud.create_lecturer_major(db, major_in)

@router.put("/lecturer-majors/{id}", response_model=schemas.LecturerMajorResponse)
def update_lecturer_major_admin(id: str, major_in: schemas.LecturerMajorUpdate, db: Session = Depends(get_db)):
    updated = crud.update_lecturer_major(db, id, major_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Chuyên ngành không tồn tại")
    return updated

@router.delete("/lecturer-majors/{id}", status_code=status.HTTP_200_OK)
def delete_lecturer_major_admin(id: str, db: Session = Depends(get_db)):
    success = crud.delete_lecturer_major(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Chuyên ngành không tồn tại")
    return {"message": "Đã xóa chuyên ngành giảng viên thành công"}


# ==================== LECTURER MANAGEMENT ====================

@router.get("/lecturers", response_model=List[schemas.LecturerResponse])
def get_all_lecturers_admin(db: Session = Depends(get_db)):
    return crud.get_lecturers(db)

@router.post("/lecturers", response_model=schemas.LecturerResponse, status_code=status.HTTP_201_CREATED)
def create_lecturer_admin(lecturer_in: schemas.LecturerCreate, db: Session = Depends(get_db)):
    existing = crud.get_lecturer_by_id(db, lecturer_in.id)
    if existing:
        raise HTTPException(status_code=400, detail="Mã giảng viên (ID) đã tồn tại!")
    return crud.create_lecturer(db, lecturer_in)

@router.put("/lecturers/reorder", status_code=status.HTTP_200_OK)
def reorder_lecturers_admin(
    items: List[schemas.LecturerReorderItem],
    major_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    crud.reorder_lecturers(db, items, major_id=major_id)
    return {"message": "Đã cập nhật thứ tự giảng viên thành công"}

@router.put("/lecturers/{id}/toggle-featured", response_model=schemas.LecturerResponse)
def toggle_lecturer_featured_admin(id: str, db: Session = Depends(get_db)):
    try:
        updated = crud.toggle_lecturer_featured(db, id)
        if not updated:
            raise HTTPException(status_code=404, detail="Giảng viên không tồn tại")
        return updated
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.put("/lecturers/{id}", response_model=schemas.LecturerResponse)
def update_lecturer_admin(id: str, lecturer_in: schemas.LecturerUpdate, db: Session = Depends(get_db)):
    try:
        updated = crud.update_lecturer(db, id, lecturer_in)
        if not updated:
            raise HTTPException(status_code=404, detail="Giảng viên không tồn tại")
        return updated
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.delete("/lecturers/{id}", status_code=status.HTTP_200_OK)
def delete_lecturer_admin(id: str, db: Session = Depends(get_db)):
    success = crud.delete_lecturer(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Giảng viên không tồn tại")
    return {"message": "Đã xóa thông tin giảng viên thành công"}


# ==================== PROJECT MANAGEMENT ====================

@router.get("/projects", response_model=List[schemas.ProjectResponse])
def get_all_projects_admin(db: Session = Depends(get_db)):
    return crud.get_projects(db)

@router.post("/projects", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project_admin(project_in: schemas.ProjectCreate, db: Session = Depends(get_db)):
    existing = crud.get_project_by_id(db, project_in.id)
    if existing:
        raise HTTPException(status_code=400, detail="Mã dự án (ID) đã tồn tại!")
    return crud.create_project(db, project_in)

@router.put("/projects/{id}", response_model=schemas.ProjectResponse)
def update_project_admin(id: str, project_in: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    updated = crud.update_project(db, id, project_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Dự án không tồn tại")
    return updated

@router.delete("/projects/{id}", status_code=status.HTTP_200_OK)
def delete_project_admin(id: str, db: Session = Depends(get_db)):
    success = crud.delete_project(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Dự án không tồn tại")
    return {"message": "Đã xóa dự án thành công"}

# ==================== PROJECT REVIEWS MANAGEMENT ====================

@router.get("/project-reviews", response_model=List[schemas.ProjectReviewAdminResponse])
def get_all_project_reviews_admin(project_id: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.get_all_project_reviews_admin(db, project_id=project_id)

@router.put("/project-reviews/{id}/toggle-approval", response_model=schemas.ProjectReviewAdminResponse)
def toggle_project_review_approval(id: int, db: Session = Depends(get_db)):
    review = db.query(models.ProjectReview).filter(models.ProjectReview.id == id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Nhận xét không tồn tại")
    review.is_approved = not review.is_approved
    db.commit()
    db.refresh(review)
    return review

@router.delete("/project-reviews/{id}", status_code=status.HTTP_200_OK)
def delete_project_review_admin(id: int, db: Session = Depends(get_db)):
    success = crud.delete_project_review(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Nhận xét không tồn tại")
    return {"message": "Đã xóa nhận xét thành công"}


# ==================== BLOG POST MANAGEMENT ====================

@router.get("/blogs", response_model=List[schemas.BlogPostResponse])
def get_all_blogs_admin(db: Session = Depends(get_db)):
    return crud.get_blog_posts(db)

@router.post("/blogs", response_model=schemas.BlogPostResponse, status_code=status.HTTP_201_CREATED)
def create_blog_admin(blog_in: schemas.BlogPostCreate, db: Session = Depends(get_db)):
    existing = crud.get_blog_by_id_or_handle(db, blog_in.handle)
    if existing:
        raise HTTPException(status_code=400, detail="Handle bài viết đã tồn tại!")
    return crud.create_blog_post(db, blog_in)

@router.put("/blogs/{id}", response_model=schemas.BlogPostResponse)
def update_blog_admin(id: int, blog_in: schemas.BlogPostUpdate, db: Session = Depends(get_db)):
    updated = crud.update_blog_post(db, id, blog_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Bài viết không tồn tại")
    return updated

@router.delete("/blogs/{id}", status_code=status.HTTP_200_OK)
def delete_blog_admin(id: int, db: Session = Depends(get_db)):
    success = crud.delete_blog_post(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Bài viết không tồn tại")
    return {"message": "Đã xóa bài viết thành công"}


# ==================== TESTIMONIAL MANAGEMENT ====================

@router.get("/testimonials", response_model=List[schemas.TestimonialResponse])
def get_all_testimonials_admin(db: Session = Depends(get_db)):
    return crud.get_testimonials(db)

@router.post("/testimonials", response_model=schemas.TestimonialResponse, status_code=status.HTTP_201_CREATED)
def create_testimonial_admin(test_in: schemas.TestimonialCreate, db: Session = Depends(get_db)):
    return crud.create_testimonial(db, test_in)

@router.put("/testimonials/{id}", response_model=schemas.TestimonialResponse)
def update_testimonial_admin(id: int, test_in: schemas.TestimonialUpdate, db: Session = Depends(get_db)):
    updated = crud.update_testimonial(db, id, test_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Đánh giá không tồn tại")
    return updated

@router.delete("/testimonials/{id}", status_code=status.HTTP_200_OK)
def delete_testimonial_admin(id: int, db: Session = Depends(get_db)):
    success = crud.delete_testimonial(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Đánh giá không tồn tại")
    return {"message": "Đã xóa đánh giá thành công"}


# ==================== PARTNER MANAGEMENT ====================

@router.get("/partners", response_model=List[schemas.PartnerResponse])
def get_all_partners_admin(db: Session = Depends(get_db)):
    return crud.get_partners(db, active_only=False)

@router.post("/partners", response_model=schemas.PartnerResponse, status_code=status.HTTP_201_CREATED)
def create_partner_admin(partner_in: schemas.PartnerCreate, db: Session = Depends(get_db)):
    return crud.create_partner(db, partner_in)

@router.put("/partners/{id}", response_model=schemas.PartnerResponse)
def update_partner_admin(id: int, partner_in: schemas.PartnerUpdate, db: Session = Depends(get_db)):
    updated = crud.update_partner(db, id, partner_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Đối tác không tồn tại")
    return updated

@router.delete("/partners/{id}", status_code=status.HTTP_200_OK)
def delete_partner_admin(id: int, db: Session = Depends(get_db)):
    success = crud.delete_partner(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Đối tác không tồn tại")
    return {"message": "Đã xóa đối tác thành công"}





