from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....database import get_db
from .... import schemas, crud

router = APIRouter()

# ==================== BLOG POST MANAGEMENT ====================

# --- Blog Categories Admin ---
@router.get("/blogs/categories", response_model=List[schemas.BlogCategoryResponse])
def get_all_blog_categories_admin(db: Session = Depends(get_db)):
    return crud.get_blog_categories(db)

@router.post("/blogs/categories", response_model=schemas.BlogCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_blog_category_admin(cat_in: schemas.BlogCategoryCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_blog_category(db, cat_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/blogs/categories/{id}", response_model=schemas.BlogCategoryResponse)
def update_blog_category_admin(id: int, cat_in: schemas.BlogCategoryUpdate, db: Session = Depends(get_db)):
    try:
        updated = crud.update_blog_category(db, id, cat_in)
        if not updated:
            raise HTTPException(status_code=404, detail="Chuyên mục không tồn tại")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/blogs/categories/{id}", status_code=status.HTTP_200_OK)
def delete_blog_category_admin(id: int, db: Session = Depends(get_db)):
    try:
        success = crud.delete_blog_category(db, id)
        if not success:
            raise HTTPException(status_code=404, detail="Chuyên mục không tồn tại")
        return {"message": "Đã xóa chuyên mục thành công"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/blogs", response_model=List[schemas.BlogPostListResponse])
def get_all_blogs_admin(db: Session = Depends(get_db)):
    return crud.get_blog_posts(db, include_content=False)

@router.get("/blogs/{id}", response_model=schemas.BlogPostResponse)
def get_blog_admin_by_id(id: int, db: Session = Depends(get_db)):
    blog = crud.get_blog_by_id_or_handle(db, str(id))
    if not blog:
        raise HTTPException(status_code=404, detail="Bài viết không tồn tại")
    return blog

@router.post("/blogs", response_model=schemas.BlogPostResponse, status_code=status.HTTP_201_CREATED)
def create_blog_admin(blog_in: schemas.BlogPostCreate, db: Session = Depends(get_db)):
    existing = crud.get_blog_by_id_or_handle(db, blog_in.handle)
    if existing:
        raise HTTPException(status_code=400, detail="Handle bài viết đã tồn tại!")
    return crud.create_blog_post(db, blog_in)

@router.put("/blogs/{id}", response_model=schemas.BlogPostResponse)
def update_blog_admin(id: int, blog_in: schemas.BlogPostUpdate, db: Session = Depends(get_db)):
    updated = crud.update_blog_post(db, id, blog_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Bài viết không tồn tại")
    return updated

@router.delete("/blogs/{id}", status_code=status.HTTP_200_OK)
def delete_blog_admin(id: int, db: Session = Depends(get_db)):
    success = crud.delete_blog_post(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Bài viết không tồn tại")
    return {"message": "Đã xóa bài viết thành công"}

