from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ....database import get_db
from .... import schemas, crud

router = APIRouter()

# ==================== LECTURER MAJOR MANAGEMENT ====================

@router.get("/lecturer-majors", response_model=List[schemas.LecturerMajorResponse])
def get_all_lecturer_majors_admin(db: Session = Depends(get_db)):
    return crud.get_lecturer_majors(db)

@router.post("/lecturer-majors", response_model=schemas.LecturerMajorResponse, status_code=status.HTTP_201_CREATED)
def create_lecturer_major_admin(major_in: schemas.LecturerMajorCreate, db: Session = Depends(get_db)):
    existing = crud.get_lecturer_major_by_id(db, major_in.id)
    if existing:
        raise HTTPException(status_code=400, detail="Mã chuyên ngành (ID) này đã tồn tại!")
    return crud.create_lecturer_major(db, major_in)

@router.put("/lecturer-majors/{id}", response_model=schemas.LecturerMajorResponse)
def update_lecturer_major_admin(id: str, major_in: schemas.LecturerMajorUpdate, db: Session = Depends(get_db)):
    updated = crud.update_lecturer_major(db, id, major_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Chuyên ngành không tồn tại")
    return updated

@router.delete("/lecturer-majors/{id}", status_code=status.HTTP_200_OK)
def delete_lecturer_major_admin(id: str, db: Session = Depends(get_db)):
    success = crud.delete_lecturer_major(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Chuyên ngành không tồn tại")
    return {"message": "Đã xóa chuyên ngành giảng viên thành công"}


# ==================== LECTURER MANAGEMENT ====================

@router.get("/lecturers", response_model=List[schemas.LecturerResponse])
def get_all_lecturers_admin(db: Session = Depends(get_db)):
    return crud.get_lecturers(db, include_details=False)

@router.post("/lecturers", response_model=schemas.LecturerResponse, status_code=status.HTTP_201_CREATED)
def create_lecturer_admin(lecturer_in: schemas.LecturerCreate, db: Session = Depends(get_db)):
    existing = crud.get_lecturer_by_id(db, lecturer_in.id)
    if existing:
        raise HTTPException(status_code=400, detail="Mã giảng viên (ID) đã tồn tại!")
    return crud.create_lecturer(db, lecturer_in)

@router.put("/lecturers/reorder", status_code=status.HTTP_200_OK)
def reorder_lecturers_admin(
    items: List[schemas.LecturerReorderItem],
    major_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    crud.reorder_lecturers(db, items, major_id=major_id)
    return {"message": "Đã cập nhật thứ tự giảng viên thành công"}

@router.put("/lecturers/{id}/toggle-featured", response_model=schemas.LecturerResponse)
def toggle_lecturer_featured_admin(id: str, db: Session = Depends(get_db)):
    try:
        updated = crud.toggle_lecturer_featured(db, id)
        if not updated:
            raise HTTPException(status_code=404, detail="Giảng viên không tồn tại")
        return updated
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.put("/lecturers/{id}", response_model=schemas.LecturerResponse)
def update_lecturer_admin(id: str, lecturer_in: schemas.LecturerUpdate, db: Session = Depends(get_db)):
    try:
        updated = crud.update_lecturer(db, id, lecturer_in)
        if not updated:
            raise HTTPException(status_code=404, detail="Giảng viên không tồn tại")
        return updated
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.delete("/lecturers/{id}", status_code=status.HTTP_200_OK)
def delete_lecturer_admin(id: str, db: Session = Depends(get_db)):
    success = crud.delete_lecturer(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Giảng viên không tồn tại")
    return {"message": "Đã xóa thông tin giảng viên thành công"}

