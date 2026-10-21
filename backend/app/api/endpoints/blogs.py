from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ... import schemas, crud

router = APIRouter()

@router.get("", response_model=List[schemas.BlogPostListResponse])
def read_blogs(response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "public, max-age=120, stale-while-revalidate=60"
    blogs = crud.get_blog_posts(db)
    return blogs

@router.get("/{id_or_handle}", response_model=schemas.BlogPostResponse)
def read_blog_by_identifier(id_or_handle: str, response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "public, max-age=60, stale-while-revalidate=30"
    blog = crud.get_blog_by_id_or_handle(db, id_or_handle)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy bài viết"
        )
    return blog
