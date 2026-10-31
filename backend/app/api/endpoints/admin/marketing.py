from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....database import get_db
from .... import models, schemas, crud

router = APIRouter()

# ==================== HOME INTRO SETTINGS ====================

@router.get("/home-intro", response_model=schemas.HomeIntroSettingResponse)
def get_home_intro_settings_admin(db: Session = Depends(get_db)):
    settings = db.query(models.HomeIntroSetting).first()
    if not settings:
        settings = models.HomeIntroSetting()
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

@router.put("/home-intro", response_model=schemas.HomeIntroSettingResponse)
def update_home_intro_settings_admin(
    settings_in: schemas.HomeIntroSettingUpdate,
    db: Session = Depends(get_db)
):
    settings = db.query(models.HomeIntroSetting).first()
    if not settings:
        settings = models.HomeIntroSetting()
        db.add(settings)
        db.commit()
        db.refresh(settings)

    if settings_in.title is not None:
        settings.title = settings_in.title
    if settings_in.desc1 is not None:
        settings.desc1 = settings_in.desc1
    if settings_in.desc2 is not None:
        settings.desc2 = settings_in.desc2
    if settings_in.counter_number is not None:
        settings.counter_number = settings_in.counter_number
    if settings_in.counter_label is not None:
        settings.counter_label = settings_in.counter_label
    if settings_in.video_url is not None:
        settings.video_url = settings_in.video_url
    if settings_in.poster_url is not None:
        settings.poster_url = settings_in.poster_url
    if settings_in.btn_label is not None:
        settings.btn_label = settings_in.btn_label

    db.commit()
    db.refresh(settings)
    return settings


# ==================== BANNER MANAGEMENT ====================

@router.get("/banners", response_model=List[schemas.BannerResponse])
def get_all_banners_admin(db: Session = Depends(get_db)):
    return crud.get_banners(db, active_only=False)

@router.post("/banners", response_model=schemas.BannerResponse, status_code=status.HTTP_201_CREATED)
def create_banner_admin(banner_in: schemas.BannerCreate, db: Session = Depends(get_db)):
    return crud.create_banner(db, banner_in)

@router.put("/banners/{id}", response_model=schemas.BannerResponse)
def update_banner_admin(id: int, banner_in: schemas.BannerUpdate, db: Session = Depends(get_db)):
    updated = crud.update_banner(db, id, banner_in)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner không tồn tại"
        )
    return updated

@router.delete("/banners/{id}", status_code=status.HTTP_200_OK)
def delete_banner_admin(id: int, db: Session = Depends(get_db)):
    success = crud.delete_banner(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner không tồn tại"
        )
    return {"message": "Đã xóa banner thành công"}


# ==================== TESTIMONIAL MANAGEMENT ====================

@router.get("/testimonials", response_model=List[schemas.TestimonialResponse])
def get_all_testimonials_admin(db: Session = Depends(get_db)):
    return crud.get_testimonials(db)

@router.post("/testimonials", response_model=schemas.TestimonialResponse, status_code=status.HTTP_201_CREATED)
def create_testimonial_admin(test_in: schemas.TestimonialCreate, db: Session = Depends(get_db)):
    return crud.create_testimonial(db, test_in)

@router.put("/testimonials/{id}", response_model=schemas.TestimonialResponse)
def update_testimonial_admin(id: int, test_in: schemas.TestimonialUpdate, db: Session = Depends(get_db)):
    updated = crud.update_testimonial(db, id, test_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Đánh giá không tồn tại")
    return updated

@router.delete("/testimonials/{id}", status_code=status.HTTP_200_OK)
def delete_testimonial_admin(id: int, db: Session = Depends(get_db)):
    success = crud.delete_testimonial(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Đánh giá không tồn tại")
    return {"message": "Đã xóa đánh giá thành công"}


# ==================== PARTNER MANAGEMENT ====================

@router.get("/partners", response_model=List[schemas.PartnerResponse])
def get_all_partners_admin(db: Session = Depends(get_db)):
    return crud.get_partners(db, active_only=False)

@router.post("/partners", response_model=schemas.PartnerResponse, status_code=status.HTTP_201_CREATED)
def create_partner_admin(partner_in: schemas.PartnerCreate, db: Session = Depends(get_db)):
    return crud.create_partner(db, partner_in)

@router.put("/partners/{id}", response_model=schemas.PartnerResponse)
def update_partner_admin(id: int, partner_in: schemas.PartnerUpdate, db: Session = Depends(get_db)):
    updated = crud.update_partner(db, id, partner_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Đối tác không tồn tại")
    return updated

@router.delete("/partners/{id}", status_code=status.HTTP_200_OK)
def delete_partner_admin(id: int, db: Session = Depends(get_db)):
    success = crud.delete_partner(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Đối tác không tồn tại")
    return {"message": "Đã xóa đối tác thành công"}

