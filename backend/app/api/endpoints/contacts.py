from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...database import get_db
from ... import schemas, crud

router = APIRouter()

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
