from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload, selectinload, defer

from ....database import get_db
from .... import models, schemas, crud

router = APIRouter()

# ==================== ORDER MANAGEMENT (ĐƠN HÀNG) ====================

@router.get("/orders", response_model=List[schemas.OrderAdminResponse])
def get_all_orders(db: Session = Depends(get_db)):
    orders = (
        db.query(models.Order)
        .options(
            joinedload(models.Order.user),
            selectinload(models.Order.items)
            .joinedload(models.OrderItem.course)
            .options(
                defer(models.Course.curriculum_data),
                defer(models.Course.outcomes),
                defer(models.Course.requirements),
                defer(models.Course.custom_roadmap),
                defer(models.Course.description),
            )
        )
        .order_by(models.Order.id.desc())
        .all()
    )
    res = []
    for o in orders:
        res.append({
            "id": o.id,
            "user_id": o.user_id,
            "user_fullname": o.user.fullname if o.user else "Unknown User",
            "user_email": o.user.email if o.user else "unknown@domain.com",
            "total_price": o.total_price,
            "discount_applied": o.discount_applied,
            "status": o.status,
            "created_at": o.created_at,
            "items": o.items
        })
    return res

@router.post("/orders", response_model=schemas.OrderAdminResponse, status_code=status.HTTP_201_CREATED)
def create_order_admin(order_in: schemas.OrderAdminCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == order_in.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Học viên không tồn tại"
        )
        
    db_order = models.Order(
        user_id=order_in.user_id,
        total_price=order_in.total_price,
        discount_applied=order_in.discount_applied,
        status=order_in.status
    )
    db.add(db_order)
    db.flush()
    
    for cid in order_in.course_ids:
        course = db.query(models.Course).filter(models.Course.id == cid).first()
        if course:
            db_item = models.OrderItem(
                order_id=db_order.id,
                course_id=cid,
                price=course.price
            )
            db.add(db_item)
            
    db.commit()
    db.refresh(db_order)
    
    # Return formatted order response
    return {
        "id": db_order.id,
        "user_id": db_order.user_id,
        "user_fullname": user.fullname,
        "user_email": user.email,
        "total_price": db_order.total_price,
        "discount_applied": db_order.discount_applied,
        "status": db_order.status,
        "created_at": db_order.created_at,
        "items": db_order.items
    }

@router.put("/orders/{id}", response_model=schemas.OrderAdminResponse)
def update_order_admin(id: int, order_in: schemas.OrderAdminUpdate, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == id).first()
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Đơn hàng không tồn tại"
        )
        
    if order_in.status is not None:
        # Handle referral reward when transitioning to paid
        if order_in.status == "paid" and db_order.status != "paid":
            user = db_order.user
            if user and user.referred_by_id:
                referrer = db.query(models.User).filter(models.User.id == user.referred_by_id).first()
                if referrer:
                    total_earned = 0
                    for item in db_order.items:
                        comm_pct = crud.get_commission_percent_for_user_course(db, referrer.id, item.course_id)
                        total_earned += int(item.price * (comm_pct / 100.0))

                    existing_referral = db.query(models.Referral).filter(
                        models.Referral.referred_id == user.id
                    ).first()

                    if not existing_referral:
                        db_referral = models.Referral(
                            referrer_id=referrer.id,
                            referred_id=user.id,
                            commission_amount=total_earned,
                            status="completed"
                        )
                        db.add(db_referral)
                    else:
                        existing_referral.commission_amount += total_earned

                    referrer.store_credit_balance += total_earned

        db_order.status = order_in.status
        
    if order_in.discount_applied is not None:
        db_order.discount_applied = order_in.discount_applied
    if order_in.total_price is not None:
        db_order.total_price = order_in.total_price
        
    if order_in.course_ids is not None:
        # Recreate order items
        db.query(models.OrderItem).filter(models.OrderItem.order_id == id).delete()
        for cid in order_in.course_ids:
            course = db.query(models.Course).filter(models.Course.id == cid).first()
            if course:
                db_item = models.OrderItem(
                    order_id=id,
                    course_id=cid,
                    price=course.price
                )
                db.add(db_item)
                
    db.commit()
    db.refresh(db_order)
    
    return {
        "id": db_order.id,
        "user_id": db_order.user_id,
        "user_fullname": db_order.user.fullname if db_order.user else "Unknown User",
        "user_email": db_order.user.email if db_order.user else "unknown@domain.com",
        "total_price": db_order.total_price,
        "discount_applied": db_order.discount_applied,
        "status": db_order.status,
        "created_at": db_order.created_at,
        "items": db_order.items
    }

@router.delete("/orders/{id}", status_code=status.HTTP_200_OK)
def delete_order_admin(id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == id).first()
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Đơn hàng không tồn tại"
        )
    db.delete(db_order)
    db.commit()
    return {"message": "Đã xóa đơn hàng thành công"}

