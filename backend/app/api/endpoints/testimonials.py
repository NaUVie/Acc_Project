from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ... import schemas, crud

router = APIRouter()

@router.get("", response_model=List[schemas.TestimonialResponse])
def read_testimonials(response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "public, max-age=180, stale-while-revalidate=60"
    return crud.get_testimonials(db)

@router.get("/{id}", response_model=schemas.TestimonialResponse)
def read_testimonial_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "public, max-age=180, stale-while-revalidate=60"
    testimonial = crud.get_testimonial_by_id(db, id)
    if not testimonial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy đánh giá"
        )
    return testimonial
