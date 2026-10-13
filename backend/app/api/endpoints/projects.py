from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ... import models, schemas, crud, auth

router = APIRouter()

@router.get("", response_model=List[schemas.ProjectResponse])
def read_projects(category: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.get_projects(db, category=category)

@router.get("/{id}", response_model=schemas.ProjectResponse)
def read_project_by_id(id: str, db: Session = Depends(get_db)):
    project = crud.get_project_by_id(db, id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy dự án"
        )
    return project

# --- PROJECT REVIEWS ---
@router.get("/{id}/reviews", response_model=List[schemas.ProjectReviewResponse])
def get_project_reviews(id: str, db: Session = Depends(get_db)):
    project = crud.get_project_by_id(db, id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy dự án"
        )
    return crud.get_project_reviews(db, project_id=id)

@router.post("/{id}/reviews", response_model=schemas.ProjectReviewResponse)
def submit_project_review(
    id: str,
    review_in: schemas.ProjectReviewCreate,
    current_user: Optional[models.User] = Depends(auth.get_optional_current_user),
    db: Session = Depends(get_db)
):
    project = crud.get_project_by_id(db, id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy dự án"
        )

    # Use authenticated user info if logged in and not provided
    author_name = current_user.fullname if current_user and not review_in.author_name.strip() else review_in.author_name.strip()
    author_email = current_user.email if current_user and not review_in.author_email else (review_in.author_email.strip() if review_in.author_email else None)
    user_id = current_user.id if current_user else None

    if not author_name:
        raise HTTPException(status_code=400, detail="Vui lòng nhập tên của bạn!")

    if not review_in.comment.strip():
        raise HTTPException(status_code=400, detail="Vui lòng nhập nội dung nhận xét!")

    clean_comment = review_in.comment.strip()
    char_count = len(clean_comment)
    word_count = len(clean_comment.split())

    if char_count > 1500:
        raise HTTPException(
            status_code=400,
            detail=f"Nhận xét vượt quá giới hạn 1500 ký tự (hiện tại: {char_count} ký tự)!"
        )

    if word_count < 10:
        raise HTTPException(
            status_code=400,
            detail=f"Nhận xét cần tối thiểu 10 từ để đảm bảo chất lượng góp ý (hiện tại: {word_count} từ)!"
        )

    if word_count > 300:
        raise HTTPException(
            status_code=400,
            detail=f"Nhận xét tối đa 300 từ (hiện tại: {word_count} từ)!"
        )

    review = crud.create_project_review(
        db,
        project_id=id,
        author_name=author_name,
        author_email=author_email,
        rating=review_in.rating,
        comment=clean_comment,
        user_id=user_id
    )
    return review

