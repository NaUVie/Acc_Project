import os
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ... import models, schemas, crud, auth, vnpay
from ...config import VNPAY_TMN_CODE, VNPAY_HASH_SECRET, VNPAY_PAYMENT_URL, VNPAY_RETURN_URL

router = APIRouter()

ALLOW_MOCK_PAYMENT = os.getenv("ALLOW_MOCK_PAYMENT", "true").lower() == "true"

@router.get("", response_model=List[schemas.OrderResponse])
def read_orders(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_user_orders(db, user_id=current_user.id)

@router.post("/checkout", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def checkout(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    order = crud.checkout_cart(db, user_id=current_user.id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your cart is empty"
        )
    return order

@router.post("/{id}/pay", response_model=schemas.OrderResponse)
def mock_payment(
    id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if not ALLOW_MOCK_PAYMENT and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tính năng giả lập thanh toán đã bị tắt trong môi trường Production."
        )

    # Verify order belongs to current user (or admin)
    query = db.query(models.Order).filter(models.Order.id == id)
    if current_user.role != "admin":
        query = query.filter(models.Order.user_id == current_user.id)
    
    order = query.first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
        
    if order.status == "paid":
        return order
        
    updated_order = crud.pay_order(db, order_id=id)
    return updated_order

@router.post("/{id}/vnpay-url")
def create_vnpay_url(
    id: int,
    request: Request,
    bank_code: Optional[str] = None,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.Order).filter(models.Order.id == id)
    if current_user.role != "admin":
        query = query.filter(models.Order.user_id == current_user.id)
    
    order = query.first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Đơn hàng không tồn tại"
        )
    if order.status == "paid":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Đơn hàng đã được thanh toán"
        )
    if order.total_price <= 0:
        # If total is 0 (due to 100% coupon or store credit), pay directly
        crud.pay_order(db, order_id=id)
        return {"payment_url": None, "status": "paid", "message": "Đơn hàng 0đ đã được kích hoạt trực tiếp"}

    # Get client IP
    client_ip = request.client.host if request.client else "127.0.0.1"
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()

    # Determine dynamic return_url based on Origin/Referer of client, fallback to config
    origin = request.headers.get("origin")
    referer = request.headers.get("referer")
    base_client_url = None
    if origin:
        base_client_url = origin.rstrip("/")
    elif referer:
        import urllib.parse
        parsed = urllib.parse.urlparse(referer)
        base_client_url = f"{parsed.scheme}://{parsed.netloc}".rstrip("/")
        
    if base_client_url:
        actual_return_url = f"{base_client_url}/payment/vnpay-return"
    else:
        actual_return_url = VNPAY_RETURN_URL

    payment_url = vnpay.generate_vnpay_url(
        order_id=order.id,
        amount=order.total_price,
        order_info=f"Thanh toan don hang ACC #{order.id}",
        ip_addr=client_ip,
        tmn_code=VNPAY_TMN_CODE,
        hash_secret=VNPAY_HASH_SECRET,
        payment_url=VNPAY_PAYMENT_URL,
        return_url=actual_return_url,
        bank_code=bank_code
    )

    return {"payment_url": payment_url, "order_id": order.id, "amount": order.total_price}

@router.get("/vnpay-return")
def vnpay_return_handler(
    request: Request,
    db: Session = Depends(get_db)
):
    params = dict(request.query_params)
    is_valid = vnpay.verify_vnpay_response(params, VNPAY_HASH_SECRET)
    if not is_valid:
        return {
            "success": False,
            "message": "Chữ ký bảo mật không hợp lệ (Invalid Checksum)!",
            "rsp_code": "97"
        }

    vnp_response_code = params.get("vnp_ResponseCode")
    vnp_txn_ref = params.get("vnp_TxnRef")

    if not vnp_txn_ref:
        return {
            "success": False,
            "message": "Không tìm thấy mã đơn hàng",
            "rsp_code": "01"
        }

    try:
        order_id = int(vnp_txn_ref)
    except ValueError:
        return {
            "success": False,
            "message": "Mã đơn hàng không hợp lệ",
            "rsp_code": "01"
        }

    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        return {
            "success": False,
            "message": "Đơn hàng không tồn tại",
            "rsp_code": "01"
        }

    if vnp_response_code == "00":
        if db_order.status != "paid":
            crud.pay_order(db, order_id=order_id)
        return {
            "success": True,
            "order_id": order_id,
            "message": "Giao dịch thành công!",
            "rsp_code": "00"
        }
    else:
        return {
            "success": False,
            "order_id": order_id,
            "message": f"Giao dịch không thành công hoặc đã bị hủy (Mã phản hồi: {vnp_response_code})",
            "rsp_code": vnp_response_code
        }

