from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ... import schemas, crud

router = APIRouter()

@router.get("", response_model=List[schemas.BlogPostResponse])
def read_blogs(db: Session = Depends(get_db)):
    blogs = crud.get_blog_posts(db)
    return blogs
