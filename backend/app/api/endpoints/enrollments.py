import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ... import models, schemas, crud, auth

router = APIRouter()

ALLOW_MOCK_PAYMENT = os.getenv("ALLOW_MOCK_PAYMENT", "true").lower() == "true"

@router.get("", response_model=List[schemas.EnrollmentResponse])
def get_my_enrollments(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get all courses the current user is enrolled in (has paid access to)."""
    return crud.get_user_enrollments(db, user_id=current_user.id)

@router.get("/check/{course_id}", response_model=schemas.EnrollmentCheckResponse)
def check_my_enrollment(
    course_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Check if the current user is enrolled in a specific course."""
    enrolled = crud.check_enrollment(db, user_id=current_user.id, course_id=course_id)
    return schemas.EnrollmentCheckResponse(enrolled=enrolled, course_id=course_id)

@router.post("/mock/{course_id}", response_model=schemas.EnrollmentResponse)
def mock_enroll(
    course_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mock enrollment: directly enroll user in a course without payment.
    Requires ALLOW_MOCK_PAYMENT=true or admin privileges.
    """
    if not ALLOW_MOCK_PAYMENT and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tính năng cấp khóa học tự do đã bị tắt."
        )

    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    enrollment = crud.enroll_user_in_course(db, user_id=current_user.id, course_id=course_id)
    return enrollment
