from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ... import schemas, crud

router = APIRouter()

@router.get("", response_model=List[schemas.TestimonialResponse])
def read_testimonials(db: Session = Depends(get_db)):
    return crud.get_testimonials(db)
