from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ... import schemas, crud, models, auth

router = APIRouter()

@router.get("", response_model=List[schemas.CoursePublicResponse])
def read_courses(
    category: Optional[str] = Query(None, description="Filter courses by category slug"),
    db: Session = Depends(get_db)
):
    courses = crud.get_courses(db, category_slug=category)
    return courses

@router.get("/programs", response_model=List[schemas.ProgramResponse])
def read_programs(db: Session = Depends(get_db)):
    return db.query(models.Program).all()

@router.get("/bundles", response_model=List[schemas.BundleResponse])
def read_bundles(db: Session = Depends(get_db)):
    return db.query(models.Bundle).all()

@router.get("/{handle}", response_model=schemas.CoursePublicResponse)
def read_course(handle: str, db: Session = Depends(get_db)):
    course = crud.get_course_by_handle(db, handle=handle)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with handle '{handle}' not found."
        )
    return course

@router.get("/{handle}/study", response_model=schemas.CourseStudyResponse)
def get_course_study_data(
    handle: str,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get full course data including curriculum_data for study interface.
    Requires user authentication and active course enrollment (or admin privileges).
    """
    course = crud.get_course_by_handle(db, handle=handle)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with handle '{handle}' not found."
        )
    
    # Check enrollment or admin role
    is_enrolled = crud.check_enrollment(db, user_id=current_user.id, course_id=course.id)
    if not is_enrolled and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn chưa mua khóa học này. Vui lòng đăng ký để học tập!"
        )
    
    return course
