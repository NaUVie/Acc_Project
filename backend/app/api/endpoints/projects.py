from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ... import schemas, crud

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
