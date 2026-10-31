from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....database import get_db
from .... import models, schemas, crud

router = APIRouter()

# ==================== PROJECT MANAGEMENT ====================

@router.get("/projects", response_model=List[schemas.ProjectResponse])
def get_all_projects_admin(db: Session = Depends(get_db)):
    return crud.get_projects(db)

@router.post("/projects", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project_admin(project_in: schemas.ProjectCreate, db: Session = Depends(get_db)):
    existing = crud.get_project_by_id(db, project_in.id)
    if existing:
        raise HTTPException(status_code=400, detail="Mã dự án (ID) đã tồn tại!")
    return crud.create_project(db, project_in)

@router.put("/projects/{id}", response_model=schemas.ProjectResponse)
def update_project_admin(id: str, project_in: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    updated = crud.update_project(db, id, project_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Dự án không tồn tại")
    return updated

@router.delete("/projects/{id}", status_code=status.HTTP_200_OK)
def delete_project_admin(id: str, db: Session = Depends(get_db)):
    success = crud.delete_project(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Dự án không tồn tại")
    return {"message": "Đã xóa dự án thành công"}


# ==================== PROJECT REVIEWS MANAGEMENT ====================

@router.get("/project-reviews", response_model=List[schemas.ProjectReviewAdminResponse])
def get_all_project_reviews_admin(project_id: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.get_all_project_reviews_admin(db, project_id=project_id)

@router.put("/project-reviews/{id}/toggle-approval", response_model=schemas.ProjectReviewAdminResponse)
def toggle_project_review_approval(id: int, db: Session = Depends(get_db)):
    review = db.query(models.ProjectReview).filter(models.ProjectReview.id == id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Nhận xét không tồn tại")
    review.is_approved = not review.is_approved
    db.commit()
    db.refresh(review)
    return review

@router.delete("/project-reviews/{id}", status_code=status.HTTP_200_OK)
def delete_project_review_admin(id: int, db: Session = Depends(get_db)):
    success = crud.delete_project_review(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Nhận xét không tồn tại")
    return {"message": "Đã xóa nhận xét thành công"}

