from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session, selectinload
from typing import List, Optional
from ...database import get_db
from ... import schemas, crud, models, auth

router = APIRouter()

@router.get("", response_model=List[schemas.CoursePublicResponse])
def read_courses(
    response: Response,
    category: Optional[str] = Query(None, description="Filter courses by category slug"),
    _t: Optional[str] = Query(None, description="Cache buster timestamp"),
    db: Session = Depends(get_db)
):
    if _t:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    else:
        response.headers["Cache-Control"] = "public, max-age=30, stale-while-revalidate=15"
    courses = crud.get_courses(db, category_slug=category)
    return courses

@router.get("/categories", response_model=List[schemas.CategoryResponse])
def read_categories(response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "public, max-age=180, stale-while-revalidate=60"
    return crud.get_categories(db)

@router.get("/banners", response_model=List[schemas.BannerResponse])
def read_banners(response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "public, max-age=180, stale-while-revalidate=60"
    return crud.get_banners(db, active_only=True)

@router.get("/partners", response_model=List[schemas.PartnerResponse])
def read_partners(response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "public, max-age=300, stale-while-revalidate=60"
    return crud.get_partners(db, active_only=True)


@router.get("/{handle}", response_model=schemas.CoursePublicResponse)
def read_course(handle: str, response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "public, max-age=120, stale-while-revalidate=60"
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

@router.get("/{handle}/progress", response_model=schemas.CourseProgressResponse)
def get_course_progress(
    handle: str,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    course = crud.get_course_by_handle(db, handle=handle)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    is_enrolled = crud.check_enrollment(db, user_id=current_user.id, course_id=course.id)
    if not is_enrolled and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn chưa mua khóa học này."
        )
    
    completed_lessons = crud.get_user_course_progress(db, user_id=current_user.id, course_id=course.id)
    return {"course_id": course.id, "completed_lessons": completed_lessons}

@router.post("/{handle}/progress", response_model=schemas.CourseProgressResponse)
def update_course_progress(
    handle: str,
    progress_in: schemas.CourseProgressUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    course = crud.get_course_by_handle(db, handle=handle)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    is_enrolled = crud.check_enrollment(db, user_id=current_user.id, course_id=course.id)
    if not is_enrolled and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn chưa mua khóa học này."
        )
    
    crud.update_user_course_progress(
        db, user_id=current_user.id, course_id=course.id, completed_lessons=progress_in.completed_lessons
    )
    return {"course_id": course.id, "completed_lessons": progress_in.completed_lessons}
