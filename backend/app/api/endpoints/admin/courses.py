from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, text
from sqlalchemy.orm import Session

from ....database import get_db
from .... import models, schemas

router = APIRouter()

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

