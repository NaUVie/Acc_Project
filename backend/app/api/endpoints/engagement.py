from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ... import models, schemas, crud, auth

router = APIRouter()

# --- REVIEWS ---
@router.get("/reviews/{course_handle}", response_model=List[schemas.CourseReviewResponse])
def get_reviews(course_handle: str, db: Session = Depends(get_db)):
    course = crud.get_course_by_handle(db, course_handle)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    reviews = crud.get_course_reviews(db, course.id)
    result = []
    for r in reviews:
        user_name = r.user.fullname if r.user else "Học viên"
        result.append(schemas.CourseReviewResponse(
            id=r.id,
            course_id=r.course_id,
            user_id=r.user_id,
            user_fullname=user_name,
            rating=r.rating,
            comment=r.comment,
            created_at=r.created_at
        ))
    return result

@router.post("/reviews/{course_handle}", response_model=schemas.CourseReviewResponse)
def create_review(
    course_handle: str,
    review_in: schemas.CourseReviewCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    course = crud.get_course_by_handle(db, course_handle)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    # Check enrollment
    is_enrolled = crud.check_enrollment(db, current_user.id, course.id)
    if not is_enrolled and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn cần đăng ký học khóa này trước khi viết đánh giá!"
        )

    review = crud.create_course_review(
        db,
        user_id=current_user.id,
        course_id=course.id,
        rating=review_in.rating,
        comment=review_in.comment
    )
    return schemas.CourseReviewResponse(
        id=review.id,
        course_id=review.course_id,
        user_id=review.user_id,
        user_fullname=current_user.fullname,
        rating=review.rating,
        comment=review.comment,
        created_at=review.created_at
    )

# --- LESSON NOTES ---
@router.get("/notes/{course_handle}", response_model=List[schemas.LessonNoteResponse])
def get_notes(
    course_handle: str,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    course = crud.get_course_by_handle(db, course_handle)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    notes = crud.get_user_lesson_notes(db, current_user.id, course.id)
    return notes

@router.post("/notes", response_model=schemas.LessonNoteResponse)
def create_note(
    note_in: schemas.LessonNoteCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    course = crud.get_course_by_handle(db, note_in.course_handle)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    note = crud.create_lesson_note(
        db,
        user_id=current_user.id,
        course_id=course.id,
        lesson_id=note_in.lesson_id,
        timestamp_seconds=note_in.timestamp_seconds,
        note_text=note_in.note_text
    )
    return note

@router.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    success = crud.delete_lesson_note(db, current_user.id, note_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return {"message": "Note deleted successfully"}

# --- WISHLIST ---
@router.get("/wishlist", response_model=List[schemas.WishlistResponse])
def get_wishlist(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    items = crud.get_user_wishlists(db, current_user.id)
    result = []
    for item in items:
        if item.course:
            result.append(schemas.WishlistResponse(
                id=item.id,
                course=item.course,
                created_at=item.created_at
            ))
    return result

@router.post("/wishlist/toggle/{course_id}")
def toggle_wishlist(
    course_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    added = crud.toggle_wishlist(db, current_user.id, course_id)
    return {"added": added, "message": "Đã thêm vào danh sách yêu thích" if added else "Đã xóa khỏi danh sách yêu thích"}
