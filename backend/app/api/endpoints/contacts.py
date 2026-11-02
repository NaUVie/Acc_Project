from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from ...database import get_db
from ... import schemas, crud, models
from ...rate_limit import rate_limit

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
    response.headers["Cache-Control"] = "public, max-age=180, stale-while-revalidate=60"
    settings = db.query(models.HomeIntroSetting).first()
    if not settings:
        settings = models.HomeIntroSetting()
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


@router.post(
    "",
    response_model=schemas.ContactResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit(max_requests=5, window_seconds=60, scope="contact_submit"))]
)
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
