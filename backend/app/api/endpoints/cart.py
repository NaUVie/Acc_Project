from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ... import models, schemas, crud, auth

router = APIRouter()

@router.get("", response_model=List[schemas.CartItemResponse])
def read_cart(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_cart_items(db, user_id=current_user.id)

@router.post("", response_model=schemas.CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_item_to_cart(
    cart_in: schemas.CartItemCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Verify course exists
    course = db.query(models.Course).filter(models.Course.id == cart_in.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return crud.add_to_cart(db, user_id=current_user.id, course_id=cart_in.course_id)

@router.delete("/{course_id}", status_code=status.HTTP_200_OK)
def delete_item_from_cart(
    course_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    success = crud.remove_from_cart(db, user_id=current_user.id, course_id=course_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in cart"
        )
    return {"message": "Item removed from cart successfully"}
