from datetime import datetime, timezone, timedelta
from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ....database import get_db
from .... import models, auth

router = APIRouter()

# ==================== EXPORT EXCEL / CSV REPORTS ====================

def filter_by_period(query, created_at_column, period: Optional[str]):
    if not period or period == "all":
        return query
    now = datetime.now(timezone.utc)
    if period == "today":
        # Hôm nay: Bắt đầu từ 00:00:00 theo giờ Việt Nam (UTC+7)
        today_vn = datetime.now(timezone(timedelta(hours=7))).replace(hour=0, minute=0, second=0, microsecond=0)
        return query.filter(created_at_column >= today_vn.astimezone(timezone.utc))
    elif period in ("7days", "week"):
        return query.filter(created_at_column >= now - timedelta(days=7))
    elif period == "month":
        return query.filter(created_at_column >= now - timedelta(days=30))
    elif period == "quarter":
        return query.filter(created_at_column >= now - timedelta(days=90))
    elif period == "year":
        return query.filter(created_at_column >= now - timedelta(days=365))
    return query

@router.get("/export/orders")
def export_orders_csv(
    period: Optional[str] = "all",
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db)
):
    query = filter_by_period(db.query(models.Order), models.Order.created_at, period)
    orders = query.order_by(models.Order.id.desc()).all()
    lines = ["Mã Đơn,Tên Học Viên,Email,Tổng Tiền (VNĐ),Giảm Giá (VNĐ),Trạng Thái,Ngày Tạo"]
    for o in orders:
        uname = o.user.fullname.replace(",", " ") if o.user else "N/A"
        uemail = o.user.email if o.user else "N/A"
        created = o.created_at.strftime("%Y-%m-%d %H:%M:%S") if o.created_at else ""
        lines.append(f'"{o.id}","{uname}","{uemail}",{o.total_price},{o.discount_applied},"{o.status}","{created}"')
    
    csv_data = "\ufeff" + "\n".join(lines)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=danh_sach_don_hang_{period}_acc.csv"}
    )

@router.get("/export/users")
def export_users_csv(
    period: Optional[str] = "all",
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db)
):
    query = filter_by_period(db.query(models.User), models.User.created_at, period)
    users = query.order_by(models.User.id.desc()).all()
    lines = ["ID,Họ và Tên,Email,Mã Ref,Ví Giảm Giá (VNĐ),Vai Trò,Trạng Thái,Ngày Đăng Ký"]
    for u in users:
        uname = u.fullname.replace(",", " ")
        created = u.created_at.strftime("%Y-%m-%d %H:%M:%S") if u.created_at else ""
        st = "Hoạt động" if u.is_active else "Khoá"
        lines.append(f'"{u.id}","{uname}","{u.email}","{u.referral_code}",{u.store_credit_balance},"{u.role}","{st}","{created}"')

    csv_data = "\ufeff" + "\n".join(lines)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=danh_sach_hoc_vien_{period}_acc.csv"}
    )

@router.get("/export/contacts")
def export_contacts_csv(
    period: Optional[str] = "all",
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db)
):
    query = filter_by_period(db.query(models.Contact), models.Contact.created_at, period)
    contacts = query.order_by(models.Contact.id.desc()).all()
    lines = ["ID,Họ và Tên,Số Điện Thoại,Email,Khóa Học Quan Tâm,Nội Dung Tư Vấn,Trạng Thái,Ngày Gửi"]
    for c in contacts:
        name = (c.fullname or "").replace(",", " ")
        phone = (c.phone or "").replace(",", " ")
        email = (c.email or "").replace(",", " ")
        course = (c.course_name or c.subject or "Tư vấn chung").replace(",", " ")
        msg = (c.message or "").replace('"', '""').replace("\n", " ").replace("\r", "")
        status = "Đã giải quyết" if c.is_resolved else "Chờ phản hồi"
        created = c.created_at.strftime("%Y-%m-%d %H:%M:%S") if c.created_at else ""
        lines.append(f'"{c.id}","{name}","{phone}","{email}","{course}","{msg}","{status}","{created}"')

    csv_data = "\ufeff" + "\n".join(lines)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=danh_sach_tu_van_{period}_acc.csv"}
    )

@router.get("/export/revenue")
def export_revenue_csv(
    period: Optional[str] = "all",
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db)
):
    base_query = db.query(models.Order).filter(models.Order.status == "paid")
    query = filter_by_period(base_query, models.Order.created_at, period)

    paid_orders = query.order_by(models.Order.created_at.desc()).all()
    total_rev = sum(o.total_price for o in paid_orders)
    lines = [f"BÁO CÁO DOANH THU ACC ACADEMY ({period.upper()}),,,Tổng Doanh Thu: {total_rev:,} VNĐ", "Mã Đơn,Tên Học Viên,Email,Doanh Thu Đơn (VNĐ),Ngày Thanh Toán"]
    for o in paid_orders:
        uname = o.user.fullname.replace(",", " ") if o.user else "N/A"
        uemail = o.user.email if o.user else "N/A"
        created = o.created_at.strftime("%Y-%m-%d %H:%M:%S") if o.created_at else ""
        lines.append(f'"{o.id}","{uname}","{uemail}",{o.total_price},"{created}"')

    csv_data = "\ufeff" + "\n".join(lines)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=bao_cao_doanh_thu_{period}_acc.csv"}
    )

