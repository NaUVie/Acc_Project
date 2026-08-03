from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...database import get_db
from ... import schemas, crud, models

router = APIRouter()

@router.get("/settings", response_model=schemas.ContactSettingResponse)
def get_contact_settings(db: Session = Depends(get_db)):
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

@router.post("", response_model=schemas.ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact_inquiry(
    contact_in: schemas.ContactCreate,
    db: Session = Depends(get_db)
):
    try:
        contact = crud.create_contact(db, contact_in=contact_in)
        return contact
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save contact inquiry: {str(e)}"
        )
