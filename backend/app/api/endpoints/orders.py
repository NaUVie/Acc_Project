from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ... import models, schemas, crud, auth

router = APIRouter()

# Read-only historical orders endpoint (all checkout/payment endpoints removed)
@router.get("", response_model=List[schemas.OrderResponse])
def read_orders(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of past orders for the current user."""
    return crud.get_user_orders(db, user_id=current_user.id)
