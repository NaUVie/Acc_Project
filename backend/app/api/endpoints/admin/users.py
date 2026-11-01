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

    if user_in.referred_by_id:
        referrer = db.query(models.User).filter(models.User.id == user_in.referred_by_id).first()
        if not referrer:
            raise HTTPException(status_code=400, detail="Người giới thiệu không tồn tại!")

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
    if user_in.password and user_in.password.strip():
        new_pwd = user_in.password.strip()
        if len(new_pwd) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mật khẩu mới phải có tối thiểu 6 ký tự!"
            )
        db_user.hashed_password = auth.get_password_hash(new_pwd)
        
    if user_in.referred_by_id is not None:
        if user_in.referred_by_id == id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Học viên không thể tự giới thiệu chính mình!"
            )
        if user_in.referred_by_id > 0:
            referrer = db.query(models.User).filter(models.User.id == user_in.referred_by_id).first()
            if not referrer:
                raise HTTPException(status_code=400, detail="Người giới thiệu không tồn tại!")
            if referrer.referred_by_id == id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Không thể tạo vòng lặp giới thiệu chéo giữa 2 học viên!"
                )
            db_user.referred_by_id = user_in.referred_by_id
        else:
            db_user.referred_by_id = None
        
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{id}", status_code=status.HTTP_200_OK)
def delete_user_admin(
    id: int, 
    current_admin: models.User = Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    if id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không thể xóa chính tài khoản Admin bạn đang sử dụng!"
        )

    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Học viên không tồn tại"
        )
    
    # Check if user has orders
    order_count = db.query(models.Order).filter(models.Order.user_id == id).count()
    if order_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không thể xóa học viên đã có lịch sử đơn hàng. Hãy khóa/vô hiệu hóa tài khoản thay vì xóa."
        )

    # Detach referred users so foreign key constraint is satisfied
    db.query(models.User).filter(models.User.referred_by_id == id).update({"referred_by_id": None})
    
    # Clean up referrals, commissions, cart, wishlist, notes, reviews
    db.query(models.Referral).filter((models.Referral.referrer_id == id) | (models.Referral.referred_id == id)).delete()
    db.query(models.UserCourseCommission).filter(models.UserCourseCommission.user_id == id).delete()
    db.query(models.CartItem).filter(models.CartItem.user_id == id).delete()
    db.query(models.Wishlist).filter(models.Wishlist.user_id == id).delete()
    db.query(models.LessonNote).filter(models.LessonNote.user_id == id).delete()
    db.query(models.CourseReview).filter(models.CourseReview.user_id == id).delete()
    db.query(models.Enrollment).filter(models.Enrollment.user_id == id).delete()

    db.delete(db_user)
    db.commit()
    return {"message": "Đã xóa học viên thành công"}

