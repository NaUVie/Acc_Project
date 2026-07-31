from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ... import models, schemas, crud, auth

router = APIRouter()

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
    # Verify order belongs to current user
    order = db.query(models.Order).filter(
        models.Order.id == id,
        models.Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
        
    if order.status == "paid":
        return order
        
    updated_order = crud.pay_order(db, order_id=id)
    return updated_order
