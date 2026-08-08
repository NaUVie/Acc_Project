from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from ...database import get_db
from ... import models, schemas, auth

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
    if user_in.email is not None:
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
                existing_referral = db.query(models.Referral).filter(
                    models.Referral.referred_id == user.id
                ).first()
                if not existing_referral:
                    commission = int(order_in.total_price or db_order.total_price * 0.10)
                    commission_capped = min(commission, 29000000)
                    db_referral = models.Referral(
                        referrer_id=user.referred_by_id,
                        referred_id=user.id,
                        commission_amount=commission_capped,
                        status="completed"
                    )
                    db.add(db_referral)
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


# ==================== COURSE CATALOG MANAGEMENT ====================

@router.post("/courses", response_model=schemas.CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course_admin(course_in: schemas.CourseAdminCreate, db: Session = Depends(get_db)):
    # Verify/create category slug
    cat = db.query(models.Category).filter(models.Category.slug == course_in.category_slug).first()
    if not cat:
        cat_name = "Kỹ năng AI"
        if course_in.category_slug == "ky-nang-mem":
            cat_name = "Kỹ năng mềm"
        elif course_in.category_slug == "ky-nang-chuyen-mon":
            cat_name = "Kỹ năng chuyên môn"
        elif course_in.category_slug == "bundles":
            cat_name = "Combo / Gói"
        cat = models.Category(slug=course_in.category_slug, name=cat_name)
        db.add(cat)
        db.commit()

    # Generate big integer ID if not provided
    cid = db.query(models.Course).count() + 1
    
    db_course = models.Course(
        id=cid,
        title=course_in.title,
        category_slug=course_in.category_slug,
        program_id=course_in.program_id,
        handle=course_in.handle,
        price=course_in.price,
        original_price=course_in.original_price,
        image=course_in.image,
        description=course_in.description,
        duration=course_in.duration,
        level=course_in.level,
        curriculum_data=course_in.curriculum_data
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
        db_course.program_id = course_in.program_id if course_in.program_id != 0 else None
    if course_in.handle is not None:
        db_course.handle = course_in.handle
    if course_in.price is not None:
        db_course.price = course_in.price
    if course_in.original_price is not None:
        db_course.original_price = course_in.original_price
    if course_in.image is not None:
        db_course.image = course_in.image
    if course_in.description is not None:
        db_course.description = course_in.description
    if course_in.duration is not None:
        db_course.duration = course_in.duration
    if course_in.level is not None:
        db_course.level = course_in.level
    if course_in.curriculum_data is not None:
        db_course.curriculum_data = course_in.curriculum_data
        
    db.commit()
    db.refresh(db_course)
    return db_course

@router.delete("/courses/{id}", status_code=status.HTTP_200_OK)
def delete_course_admin(id: int, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == id).first()
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Khóa học không tồn tại"
        )
    db.delete(db_course)
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

