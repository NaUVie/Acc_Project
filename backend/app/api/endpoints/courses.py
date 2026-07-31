from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ... import schemas, crud

router = APIRouter()

@router.get("", response_model=List[schemas.CourseResponse])
def read_courses(
    category: Optional[str] = Query(None, description="Filter courses by category slug"),
    db: Session = Depends(get_db)
):
    courses = crud.get_courses(db, category_slug=category)
    return courses

@router.get("/{handle}", response_model=schemas.CourseResponse)
def read_course(handle: str, db: Session = Depends(get_db)):
    course = crud.get_course_by_handle(db, handle=handle)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with handle '{handle}' not found."
        )
    return course
