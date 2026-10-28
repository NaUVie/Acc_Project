from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ... import schemas, crud

router = APIRouter()

@router.get("", response_model=List[schemas.LecturerResponse])
def read_lecturers(response: Response, featured: bool = False, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "no-cache, must-revalidate"
    return crud.get_lecturers(db, featured_only=featured)

@router.get("/majors", response_model=List[schemas.LecturerMajorResponse])
def read_lecturer_majors(response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "no-cache, must-revalidate"
    return crud.get_lecturer_majors(db)

@router.get("/{id}", response_model=schemas.LecturerResponse)
def read_lecturer_by_id(id: str, response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "no-cache, must-revalidate"
    lecturer = crud.get_lecturer_by_id(db, id)
    if not lecturer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy thông tin giảng viên"
        )
    return lecturer
