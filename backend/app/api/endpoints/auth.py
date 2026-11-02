from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.orm import Session
from ...database import get_db
from ... import models, schemas, crud, auth
from ...rate_limit import rate_limit

router = APIRouter()

@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit(max_requests=5, window_seconds=60, scope="auth_register"))]
)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    db_user = crud.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    # Validate referral code if provided (case-insensitive)
    if user_in.referral_code_used:
        clean_code = user_in.referral_code_used.strip().upper()
        referrer = db.query(models.User).filter(func.upper(models.User.referral_code) == clean_code).first()
        if not referrer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid referral code"
            )
        if referrer.email.strip().lower() == user_in.email.strip().lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Không thể tự giới thiệu chính mình!"
            )
            
    return crud.create_user(db, user_in=user_in)

@router.post(
    "/login",
    response_model=schemas.Token,
    dependencies=[Depends(rate_limit(max_requests=10, window_seconds=60, scope="auth_login"))]
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Retrieve user by email (username field in OAuth2 request)
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản của bạn đã bị vô hiệu hóa. Vui lòng liên hệ quản trị viên."
        )
    # Generate token
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def read_current_user(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@router.put("/me", response_model=schemas.UserResponse)
def update_current_user_profile(
    user_update: schemas.UserUpdateProfile,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if user_update.fullname is not None and user_update.fullname.strip():
        current_user.fullname = user_update.fullname.strip()

    if user_update.phone is not None:
        current_user.phone = user_update.phone.strip() if user_update.phone.strip() else None

    if user_update.password is not None and user_update.password.strip():
        # Require old password to change password
        if not user_update.old_password or not user_update.old_password.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vui lòng nhập mật khẩu hiện tại (mật khẩu cũ) để đổi mật khẩu mới!"
            )
        if not auth.verify_password(user_update.old_password.strip(), current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mật khẩu hiện tại (mật khẩu cũ) không chính xác!"
            )
        new_pwd = user_update.password.strip()
        if len(new_pwd) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mật khẩu mới phải có tối thiểu 8 ký tự!"
            )
        if len(new_pwd.encode("utf-8")) > 72:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mật khẩu mới tối đa 72 byte!"
            )
        current_user.hashed_password = auth.get_password_hash(new_pwd)

    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/referrals", response_model=schemas.ReferralSummary)
def read_user_referrals(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    summary = crud.get_referral_summary(db, user_id=current_user.id)
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return summary

@router.post(
    "/forgot-password",
    dependencies=[Depends(rate_limit(max_requests=5, window_seconds=60, scope="auth_forgot_pwd"))]
)
def request_password_reset(
    req: schemas.PasswordResetRequestCreate,
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_email(db, email=req.email)

    phone_clean = req.phone.strip() if req.phone and req.phone.strip() else (user.phone if user and user.phone else "0900000000")
    digits = [c for c in phone_clean if c.isdigit()]
    if len(digits) < 9 or len(digits) > 15:
        phone_clean = "0900000000"

    fullname = user.fullname if user else "Học viên"
    note = req.note.strip() if req.note and req.note.strip() else "Không có ghi chú thêm."
    user_status = f"Đã tìm thấy tài khoản học viên (ID #{user.id}, Họ tên: {fullname})" if user else "Chưa có tài khoản trong hệ thống với email này"

    inquiry_msg = (
        f"[YÊU CẦU CẤP LẠI MẬT KHẨU]\n"
        f"- Email: {req.email.strip()}\n"
        f"- Họ tên: {fullname}\n"
        f"- Số điện thoại: {req.phone.strip() if req.phone else (user.phone if user and user.phone else 'Chưa cung cấp')}\n"
        f"- Ghi chú: {note}\n"
        f"- Hệ thống: {user_status}"
    )

    contact_in = schemas.ContactCreate(
        first_name="[Quên MK]",
        last_name=fullname[:95],
        email=req.email.strip(),
        phone=phone_clean,
        course_handle="forgot_password",
        message=inquiry_msg
    )
    crud.create_contact(db, contact_in=contact_in)

    return {
        "success": True,
        "message": "Yêu cầu cấp lại mật khẩu đã được gửi đến Ban quản trị thành công.",
        "email": req.email.strip()
    }
