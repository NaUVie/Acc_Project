from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from ...database import get_db
from ... import models, schemas, crud, auth
from ...rate_limit import rate_limit

router = APIRouter()

# --- COUPONS ---
@router.post(
    "/coupons/apply",
    response_model=schemas.CouponApplyResponse,
    dependencies=[Depends(rate_limit(max_requests=15, window_seconds=60, scope="coupon_apply"))]
)
def apply_coupon(
    req: schemas.CouponApplyRequest,
    current_user: Optional[models.User] = Depends(auth.get_optional_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id if current_user else None
    crud.cleanup_expired_pending_orders(db, timeout_minutes=30, cancel_user_pending_id=user_id)
    coupon = crud.get_coupon_by_code(db, req.code)
    if not coupon:
        return schemas.CouponApplyResponse(
            valid=False,
            code=req.code,
            discount_amount=0,
            message="Mã giảm giá không tồn tại!"
        )

    if not coupon.is_active:
        return schemas.CouponApplyResponse(
            valid=False,
            code=req.code,
            discount_amount=0,
            message="Mã giảm giá này đã ngừng kích hoạt!"
        )

    if coupon.usage_limit > 0 and coupon.times_used >= coupon.usage_limit:
        return schemas.CouponApplyResponse(
            valid=False,
            code=req.code,
            discount_amount=0,
            message="Mã giảm giá này đã hết lượt sử dụng!"
        )

    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    if coupon.valid_from:
        v_from = coupon.valid_from.replace(tzinfo=timezone.utc) if coupon.valid_from.tzinfo is None else coupon.valid_from
        if now < v_from:
            return schemas.CouponApplyResponse(
                valid=False,
                code=req.code,
                discount_amount=0,
                message="Mã giảm giá chưa đến thời hạn sử dụng!"
            )

    if coupon.valid_to:
        v_to = coupon.valid_to.replace(tzinfo=timezone.utc) if coupon.valid_to.tzinfo is None else coupon.valid_to
        if now > v_to:
            return schemas.CouponApplyResponse(
                valid=False,
                code=req.code,
                discount_amount=0,
                message="Mã giảm giá đã quá hạn sử dụng!"
            )

    if req.cart_total < coupon.min_order_value:
        min_formatted = f"{coupon.min_order_value:,} VNĐ"
        return schemas.CouponApplyResponse(
            valid=False,
            code=req.code,
            discount_amount=0,
            message=f"Đơn hàng phải tối thiểu {min_formatted} mới được áp dụng mã này!"
        )

    discount_amount = 0
    if coupon.discount_type == "percent":
        discount_amount = int(req.cart_total * (coupon.discount_value / 100.0))
        if coupon.max_discount_amount > 0:
            discount_amount = min(discount_amount, coupon.max_discount_amount)
    else:
        discount_amount = min(coupon.discount_value, req.cart_total)

    discount_amount = max(0, min(discount_amount, req.cart_total))

    return schemas.CouponApplyResponse(
        valid=True,
        code=coupon.code,
        discount_amount=discount_amount,
        message=f"Áp dụng thành công mã {coupon.code}!"
    )

@router.get("/admin/coupons", response_model=List[schemas.CouponResponse])
def get_coupons_admin(
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db)
):
    return crud.get_all_coupons(db)

@router.post("/admin/coupons", response_model=schemas.CouponResponse)
def create_coupon_admin(
    coupon_in: schemas.CouponCreate,
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db)
):
    existing = crud.get_coupon_by_code(db, coupon_in.code)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mã giảm giá này đã tồn tại!")
    return crud.create_coupon(db, coupon_in)

@router.delete("/admin/coupons/{coupon_id}")
def delete_coupon_admin(
    coupon_id: int,
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db)
):
    success = crud.delete_coupon(db, coupon_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found")
    return {"message": "Xóa mã giảm giá thành công"}

# --- CHECKOUT WITH COUPON & STORE CREDIT ---
@router.post("/checkout-options", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def checkout_with_options(
    coupon_code: Optional[str] = None,
    use_store_credit: bool = False,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    try:
        order = crud.checkout_cart_with_options(
            db,
            user_id=current_user.id,
            coupon_code=coupon_code,
            use_store_credit=use_store_credit
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not order:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Giỏ hàng của bạn đang trống!")
    return order

# --- REFERRALS & CUSTOM COMMISSION ---
@router.get("/referrals/my-summary")
def get_my_referral_summary(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    summary = crud.get_referral_summary(db, current_user.id)
    return {
        "referral_code": current_user.referral_code,
        "store_credit_balance": current_user.store_credit_balance,
        "total_referrals": summary.total_referrals if summary else 0,
        "total_commission_earned": summary.total_commission_earned if summary else 0,
        "referrals_list": summary.referrals_list if summary else []
    }

@router.get("/admin/commissions", response_model=List[schemas.UserCourseCommissionResponse])
def get_custom_commissions_admin(
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db)
):
    commissions = (
        db.query(models.UserCourseCommission)
        .options(
            joinedload(models.UserCourseCommission.user),
            joinedload(models.UserCourseCommission.course)
        )
        .all()
    )
    result = []
    for c in commissions:
        result.append(schemas.UserCourseCommissionResponse(
            id=c.id,
            user_id=c.user_id,
            user_fullname=c.user.fullname if c.user else f"User #{c.user_id}",
            course_id=c.course_id,
            course_title=c.course.title if c.course else f"Course #{c.course_id}",
            commission_percent=c.commission_percent,
            created_at=c.created_at
        ))
    return result

@router.post("/admin/commissions/set", response_model=schemas.UserCourseCommissionResponse)
def set_custom_commission_admin(
    comm_in: schemas.UserCourseCommissionCreate,
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_id(db, comm_in.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại")
    
    course = db.query(models.Course).filter(models.Course.id == comm_in.course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khóa học không tồn tại")

    comm = crud.set_custom_commission(
        db,
        user_id=comm_in.user_id,
        course_id=comm_in.course_id,
        commission_percent=comm_in.commission_percent
    )
    return schemas.UserCourseCommissionResponse(
        id=comm.id,
        user_id=comm.user_id,
        user_fullname=user.fullname,
        course_id=comm.course_id,
        course_title=course.title,
        commission_percent=comm.commission_percent,
        created_at=comm.created_at
    )
