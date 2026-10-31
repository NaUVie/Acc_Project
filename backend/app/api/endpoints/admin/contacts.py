from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....database import get_db
from .... import models, schemas

router = APIRouter()

# ==================== CONTACT LEAD MANAGEMENT ====================

@router.get("/contacts", response_model=List[schemas.ContactResponse])
def get_all_contacts(db: Session = Depends(get_db)):
    return db.query(models.Contact).all()

@router.put("/contacts/{id}/resolve", response_model=schemas.ContactResponse)
def toggle_contact_resolved(id: int, db: Session = Depends(get_db)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == id).first()
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lời nhắn liên hệ không tồn tại"
        )
    db_contact.is_resolved = not db_contact.is_resolved
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.delete("/contacts/{id}", status_code=status.HTTP_200_OK)
def delete_contact_admin(id: int, db: Session = Depends(get_db)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == id).first()
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lời nhắn liên hệ không tồn tại"
        )
    db.delete(db_contact)
    db.commit()
    return {"message": "Đã xóa tin nhắn liên hệ thành công"}

@router.put("/contact-settings", response_model=schemas.ContactSettingResponse)
def update_contact_settings(
    settings_in: schemas.ContactSettingUpdate,
    db: Session = Depends(get_db)
):
    db_settings = db.query(models.ContactSetting).first()
    if not db_settings:
        db_settings = models.ContactSetting()
        db.add(db_settings)
        db.commit()
        db.refresh(db_settings)
    
    if settings_in.address is not None:
        db_settings.address = settings_in.address
    if settings_in.hotline is not None:
        db_settings.hotline = settings_in.hotline
    if settings_in.email is not None:
        db_settings.email = settings_in.email
    if settings_in.zalo is not None:
        db_settings.zalo = settings_in.zalo
    if settings_in.viber is not None:
        db_settings.viber = settings_in.viber
        
    db.commit()
    db.refresh(db_settings)
    return db_settings

