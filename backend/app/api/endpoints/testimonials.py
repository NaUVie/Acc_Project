from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
from ...database import get_db
from ... import models, schemas, crud
from ...profanity import check_profanity, detect_spam
from ...rate_limit import rate_limit

router = APIRouter()

@router.get("", response_model=List[schemas.TestimonialResponse])
def read_testimonials(
    response: Response, 
    course_id: Optional[int] = Query(None, description="Lọc cảm nhận theo ID khóa học"),
    db: Session = Depends(get_db)
):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    items = crud.get_testimonials(db, only_approved=True, course_id=course_id)
    return [t for t in items if t.testimonial_type != "spam"]

@router.post(
    "",
    response_model=schemas.TestimonialResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit(max_requests=5, window_seconds=60, scope="submit_testimonial"))]
)
def submit_testimonial_public(test_in: schemas.TestimonialCreate, db: Session = Depends(get_db)):
    """
    Học viên gửi nhận xét / cảm nhận kèm ảnh (không cần đăng nhập).
    - Tích hợp kiểm tra từ ngữ tục tĩu, chửi bậy (Profanity filter).
    - Tích hợp Honeypot chống bot spam.
    - Mặc định is_approved = False để chờ Admin duyệt hiển thị.
    """
    # 1. Bẫy Bot Honeypot
    if test_in.honeypot and test_in.honeypot.strip():
        # Trả về đối tượng giả lập, không lưu DB
        return schemas.TestimonialResponse(
            id=0,
            name=test_in.name,
            role=test_in.role or "",
            company=test_in.company or "",
            text=test_in.text or "",
            quote=test_in.quote or test_in.text or "",
            rating=test_in.rating or 5,
            image=test_in.image,
            course_id=test_in.course_id,
            course_name=test_in.course_name,
            testimonial_type="text",
            is_approved=False,
            created_at=datetime.now(timezone.utc)
        )

    # 2. Kiểm tra từ ngữ thô tục, chửi thề
    fields_to_check = [
        ("Nội dung nhận xét", test_in.text or ""),
        ("Trích dẫn", test_in.quote or ""),
        ("Họ và tên", test_in.name or ""),
        ("Chức vụ / Đơn vị", test_in.role or "")
    ]

    for label, val in fields_to_check:
        has_profanity, term = check_profanity(val)
        if has_profanity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{label} chứa từ ngữ không phù hợp hoặc vi phạm chuẩn mực văn hóa (phát hiện từ: '{term}'). Vui lòng sử dụng ngôn từ lịch sự, tôn trọng!"
            )

    data = test_in.model_dump()
    data.pop("honeypot", None)
    data["is_approved"] = False
    
    # 3. Tự động kiểm tra nghi ngờ spam (link quảng cáo, số điện thoại, từ khóa cờ bạc...)
    is_spam, spam_reason = detect_spam(test_in.text, test_in.quote, test_in.name, test_in.role)
    if is_spam:
        # Tự động gán trạng thái nghi ngờ spam để cảnh báo Quản trị viên
        data["testimonial_type"] = "spam"
    elif data.get("image") and data.get("testimonial_type") == "text":
        data["testimonial_type"] = "photo"
    else:
        data["testimonial_type"] = data.get("testimonial_type") or "text"

    if not data.get("quote"):
        data["quote"] = data.get("text")

    db_test = models.Testimonial(**data)
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

@router.get("/{id}", response_model=schemas.TestimonialResponse)
def read_testimonial_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    testimonial = crud.get_testimonial_by_id(db, id)
    if not testimonial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy đánh giá"
        )
    return testimonial
