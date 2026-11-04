from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ... import models, schemas, crud

router = APIRouter()

@router.get("", response_model=List[schemas.TestimonialResponse])
def read_testimonials(
    response: Response, 
    course_id: Optional[int] = Query(None, description="Lọc cảm nhận theo ID khóa học"),
    db: Session = Depends(get_db)
):
    response.headers["Cache-Control"] = "public, max-age=60, stale-while-revalidate=30"
    return crud.get_testimonials(db, only_approved=True, course_id=course_id)

@router.post("", response_model=schemas.TestimonialResponse, status_code=status.HTTP_201_CREATED)
def submit_testimonial_public(test_in: schemas.TestimonialCreate, db: Session = Depends(get_db)):
    """
    Học viên gửi nhận xét / cảm nhận mà không cần đăng nhập.
    Mặc định is_approved = False để chờ Admin duyệt.
    """
    data = test_in.model_dump()
    data["is_approved"] = False
    data["testimonial_type"] = data.get("testimonial_type") or "text"
    if not data.get("quote"):
        data["quote"] = data.get("text")
    db_test = models.Testimonial(**data)
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

@router.get("/{id}", response_model=schemas.TestimonialResponse)
def read_testimonial_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "public, max-age=60, stale-while-revalidate=30"
    testimonial = crud.get_testimonial_by_id(db, id)
    if not testimonial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy đánh giá"
        )
    return testimonial
