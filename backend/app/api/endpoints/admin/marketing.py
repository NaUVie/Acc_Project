from typing import List, Optional
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, status
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
    if settings_in.bento_title is not None:
        settings.bento_title = settings_in.bento_title
    if settings_in.bento_line1 is not None:
        settings.bento_line1 = settings_in.bento_line1
    if settings_in.bento_line2 is not None:
        settings.bento_line2 = settings_in.bento_line2
    if settings_in.bento_strong is not None:
        settings.bento_strong = settings_in.bento_strong
    if settings_in.bento_line3 is not None:
        settings.bento_line3 = settings_in.bento_line3

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

def cleanup_expired_spam_testimonials(db: Session, days: int = 30) -> int:
    """
    Tự động dọn dẹp và xóa vĩnh viễn các nhận xét rác/spam đã tồn tại quá số ngày quy định (mặc định 30 ngày).
    """
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        deleted = db.query(models.Testimonial).filter(
            models.Testimonial.testimonial_type == "spam",
            models.Testimonial.created_at < cutoff
        ).delete(synchronize_session=False)
        if deleted > 0:
            db.commit()
        return deleted
    except Exception:
        db.rollback()
        return 0

@router.get("/testimonials", response_model=List[schemas.TestimonialResponse])
def get_all_testimonials_admin(db: Session = Depends(get_db)):
    # Tự động dọn dẹp các nhận xét spam cũ hơn 30 ngày
    cleanup_expired_spam_testimonials(db, days=30)
    return crud.get_testimonials(db, only_approved=False)

@router.post("/testimonials", response_model=schemas.TestimonialResponse, status_code=status.HTTP_201_CREATED)
def create_testimonial_admin(test_in: schemas.TestimonialCreate, db: Session = Depends(get_db)):
    return crud.create_testimonial(db, test_in)

@router.delete("/testimonials/cleanup-spam", status_code=status.HTTP_200_OK)
def purge_spam_testimonials_admin(
    days: int = Query(0, description="Xóa các nhận xét spam cũ hơn số ngày này (0 = xóa toàn bộ nhận xét spam hiện tại)"),
    db: Session = Depends(get_db)
):
    """
    Chủ động dọn sạch các nhận xét rác/spam.
    days = 0: Xóa toàn bộ nhận xét spam ngay lập tức.
    days > 0: Chỉ xóa nhận xét spam đã lưu quá số ngày chỉ định.
    """
    query = db.query(models.Testimonial).filter(models.Testimonial.testimonial_type == "spam")
    if days > 0:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        query = query.filter(models.Testimonial.created_at < cutoff)

    deleted_count = query.delete(synchronize_session=False)
    db.commit()
    return {
        "message": f"Đã dọn dẹp thành công {deleted_count} nhận xét rác/spam",
        "deleted_count": deleted_count
    }

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

# ==================== BOARD MEMBER MANAGEMENT ====================

@router.get("/board-members", response_model=List[schemas.BoardMemberResponse])
def get_all_board_members_admin(role_group: str = None, db: Session = Depends(get_db)):
    return crud.get_board_members(db, active_only=False, role_group=role_group)

@router.post("/board-members", response_model=schemas.BoardMemberResponse, status_code=status.HTTP_201_CREATED)
def create_board_member_admin(member_in: schemas.BoardMemberCreate, db: Session = Depends(get_db)):
    return crud.create_board_member(db, member_in)

@router.put("/board-members/{id}", response_model=schemas.BoardMemberResponse)
def update_board_member_admin(id: int, member_in: schemas.BoardMemberUpdate, db: Session = Depends(get_db)):
    updated = crud.update_board_member(db, id, member_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Thành viên ban điều hành không tồn tại")
    return updated

@router.delete("/board-members/{id}", status_code=status.HTTP_200_OK)
def delete_board_member_admin(id: int, db: Session = Depends(get_db)):
    success = crud.delete_board_member(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Thành viên ban điều hành không tồn tại")
    return {"message": "Đã xóa thành viên thành công"}

# ==================== ADMISSION POST MANAGEMENT ====================

@router.get("/admissions", response_model=List[schemas.AdmissionPostResponse])
def get_all_admission_posts_admin(db: Session = Depends(get_db)):
    return crud.get_admission_posts(db, active_only=False)

@router.post("/admissions/seed-defaults", response_model=List[schemas.AdmissionPostResponse])
def seed_admissions_defaults_admin(db: Session = Depends(get_db)):
    crud.seed_default_admission_posts(db, force_sync=True)
    return crud.get_admission_posts(db, active_only=False)

@router.post("/admissions", response_model=schemas.AdmissionPostResponse, status_code=status.HTTP_201_CREATED)
def create_admission_post_admin(post_in: schemas.AdmissionPostCreate, db: Session = Depends(get_db)):
    existing = crud.get_admission_post_by_slug(db, post_in.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Đường dẫn tĩnh (slug) này đã tồn tại.")
    return crud.create_admission_post(db, post_in)

@router.put("/admissions/{id}", response_model=schemas.AdmissionPostResponse)
def update_admission_post_admin(id: int, post_in: schemas.AdmissionPostUpdate, db: Session = Depends(get_db)):
    if post_in.slug:
        existing = crud.get_admission_post_by_slug(db, post_in.slug)
        if existing and existing.id != id:
            raise HTTPException(status_code=400, detail="Đường dẫn tĩnh (slug) này đã tồn tại ở bài viết khác.")
    updated = crud.update_admission_post(db, id, post_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Bài viết tuyển sinh không tồn tại")
    return updated

@router.delete("/admissions/{id}", status_code=status.HTTP_200_OK)
def delete_admission_post_admin(id: int, db: Session = Depends(get_db)):
    success = crud.delete_admission_post(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Bài viết tuyển sinh không tồn tại")
    return {"message": "Đã xóa bài viết tuyển sinh thành công"}

