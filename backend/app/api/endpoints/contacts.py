from fastapi import APIRouter, Depends, HTTPException, Response, status, BackgroundTasks
from sqlalchemy.orm import Session
from ...database import get_db
from ... import schemas, crud, models
from ...rate_limit import rate_limit
from ...email_service import send_admin_contact_notification, resolve_admin_recipient

router = APIRouter()

@router.get("/settings", response_model=schemas.ContactSettingResponse)
def get_contact_settings(response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "public, max-age=180, stale-while-revalidate=60"
    settings = db.query(models.ContactSetting).first()
    if not settings:
        settings = models.ContactSetting(
            address="Tòa nhà ACC, 123 Đường Điện Biên Phủ, Quận Bình Thạnh, TP. Hồ Chí Minh",
            hotline="090 123 4567",
            email="support@accacademy.vn",
            zalo="https://zalo.me/0901234567",
            viber="https://viber.click/0901234567"
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

@router.get("/home-intro", response_model=schemas.HomeIntroSettingResponse)
def get_public_home_intro_settings(response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    settings = db.query(models.HomeIntroSetting).first()
    if not settings:
        settings = models.HomeIntroSetting()
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@router.post(
    "",
    response_model=schemas.ContactResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit(max_requests=3, window_seconds=60, scope="contact_submit"))]
)
def create_contact_inquiry(
    contact_in: schemas.ContactCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # LỚP 1: HONEYPOT CHECK (Bẫy Bot vô hình)
    # Người dùng thật không bao giờ điền trường này vì bị ẩn CSS.
    # Spambot tự động quét DOM và điền giá trị -> Chặn âm thầm, không lưu DB, không bắn email.
    if contact_in.honeypot and contact_in.honeypot.strip():
        logger.warning(f"[ANTI-SPAM] Honeypot triggered. Dummy success returned. Value={contact_in.honeypot[:30]}")
        return schemas.ContactResponse(
            id=0,
            first_name=contact_in.first_name,
            middle_name=contact_in.middle_name or "",
            last_name=contact_in.last_name or "",
            email=contact_in.email,
            phone=contact_in.phone,
            course_handle=contact_in.course_handle or "",
            message=contact_in.message or "",
            is_resolved=True,
            created_at=datetime.utcnow()
        )

    # LỚP 2: CHỐNG SPAM TRÙNG LẶP (Duplicate detection theo SĐT hoặc Email trong 3 phút)
    # Ngăn người dùng hoặc tool bấm spam liên tục vào cùng 1 thông tin
    three_minutes_ago = datetime.utcnow() - timedelta(minutes=3)
    recent_contact = db.query(models.Contact).filter(
        models.Contact.created_at >= three_minutes_ago,
        (models.Contact.phone == contact_in.phone) | (models.Contact.email == contact_in.email)
    ).first()

    if recent_contact:
        logger.info(f"[ANTI-SPAM] Duplicate contact attempt blocked for phone={contact_in.phone}, email={contact_in.email}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Hệ thống đã nhận được yêu cầu tư vấn từ bạn trước đó ít phút. Chuyên viên ACC Academy sẽ liên hệ bạn sớm nhất!"
        )

    try:
        contact = crud.create_contact(db, contact_in=contact_in)
        recipient_email = resolve_admin_recipient(db)
        background_tasks.add_task(send_admin_contact_notification, contact, recipient_email)
        return contact
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save contact inquiry: {str(e)}"
        )
