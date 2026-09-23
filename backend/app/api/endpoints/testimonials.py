from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ... import schemas, crud

router = APIRouter()

@router.get("", response_model=List[schemas.TestimonialResponse])
def read_testimonials(db: Session = Depends(get_db)):
    return crud.get_testimonials(db)

@router.get("/{id}", response_model=schemas.TestimonialResponse)
def read_testimonial_by_id(id: int, db: Session = Depends(get_db)):
    testimonial = crud.get_testimonial_by_id(db, id)
    if not testimonial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy đánh giá"
        )
    return testimonial
