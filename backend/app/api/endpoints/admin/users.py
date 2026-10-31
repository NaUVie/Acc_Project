import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....database import get_db
from .... import models, schemas, auth

router = APIRouter()

# ==================== USER MANAGEMENT (HỌC VIÊN) ====================

@router.get("/users", response_model=List[schemas.UserAdminResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.post("/users", response_model=schemas.UserAdminResponse, status_code=status.HTTP_201_CREATED)
def create_user_admin(user_in: schemas.UserAdminCreate, db: Session = Depends(get_db)):
    # Check if email exists
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã tồn tại trên hệ thống!"
        )

    hashed_pwd = auth.get_password_hash(user_in.password)
    unique_ref = f"ACC-{uuid.uuid4().hex[:6].upper()}"
    
    db_user = models.User(
        fullname=user_in.fullname,
        email=user_in.email,
        hashed_password=hashed_pwd,
        referral_code=unique_ref,
        referred_by_id=user_in.referred_by_id,
        role=user_in.role,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/users/{id}", response_model=schemas.UserAdminResponse)
def update_user_admin(id: int, user_in: schemas.UserAdminUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Học viên không tồn tại"
        )
    
    if user_in.fullname is not None:
        db_user.fullname = user_in.fullname
    if user_in.email is not None and user_in.email != db_user.email:
        existing_user = db.query(models.User).filter(models.User.email == user_in.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email đã được sử dụng bởi người dùng khác!"
            )
        db_user.email = user_in.email
    if user_in.role is not None:
        db_user.role = user_in.role
    if user_in.is_active is not None:
        db_user.is_active = user_in.is_active
    if user_in.password:
        db_user.hashed_password = auth.get_password_hash(user_in.password)
        
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{id}", status_code=status.HTTP_200_OK)
def delete_user_admin(id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Học viên không tồn tại"
        )
    
    # Check if user has orders or enrollments
    order_count = db.query(models.Order).filter(models.Order.user_id == id).count()
    if order_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không thể xóa học viên đã có lịch sử đơn hàng. Hãy vô hiệu hóa tài khoản thay vì xóa."
        )
        
    db.delete(db_user)
    db.commit()
    return {"message": "Đã xóa học viên thành công"}

