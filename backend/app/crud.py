import uuid
import json
import re
import unicodedata
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from sqlalchemy import func, or_
from sqlalchemy.orm import Session, selectinload, joinedload, defer
from sqlalchemy.orm.attributes import flag_modified
from . import models, schemas, auth

def slugify(text: str) -> str:
    if not text:
        return ""
    text = text.replace('đ', 'd').replace('Đ', 'd')
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

# --- Category & Course CRUD ---
def get_courses(db: Session, category_slug: str = None, include_details: bool = False):
    query = db.query(models.Course).options(selectinload(models.Course.tags))
    if not include_details:
        query = query.options(
            defer(models.Course.curriculum_data),
            defer(models.Course.custom_roadmap),
            defer(models.Course.outcomes),
            defer(models.Course.requirements)
        )
    if category_slug:
        clean_slug = category_slug.strip().lower()
        query = query.filter(func.lower(models.Course.category_slug) == clean_slug)
    return query.all()

def get_course_by_handle(db: Session, handle: str):
    return db.query(models.Course).options(selectinload(models.Course.tags)).filter(models.Course.handle == handle).first()

def get_categories(db: Session):
    return db.query(models.Category).all()

# --- Blog CRUD ---
def get_blog_posts(db: Session, include_content: bool = False, category: Optional[str] = None):
    query = db.query(models.BlogPost)
    if category:
        query = query.filter(models.BlogPost.category == category)
    if not include_content:
        query = query.options(defer(models.BlogPost.content))
    return query.order_by(models.BlogPost.id.desc()).all()

# --- Blog Category CRUD ---
def get_blog_categories(db: Session):
    cats = db.query(models.BlogCategory).order_by(models.BlogCategory.id.asc()).all()
    result = []
    for c in cats:
        count = db.query(models.BlogPost).filter(models.BlogPost.category == c.name).count()
        result.append({
            "id": c.id,
            "name": c.name,
            "slug": c.slug,
            "description": c.description,
            "post_count": count
        })
    return result

def get_blog_category_by_id(db: Session, cat_id: int):
    return db.query(models.BlogCategory).filter(models.BlogCategory.id == cat_id).first()

def get_blog_category_by_slug_or_name(db: Session, identifier: str):
    return db.query(models.BlogCategory).filter(
        or_(models.BlogCategory.slug == identifier, models.BlogCategory.name == identifier)
    ).first()

def create_blog_category(db: Session, cat_in: schemas.BlogCategoryCreate):
    name = cat_in.name.strip()
    slug = cat_in.slug.strip() if cat_in.slug else slugify(name)
    existing = db.query(models.BlogCategory).filter(
        or_(models.BlogCategory.slug == slug, models.BlogCategory.name == name)
    ).first()
    if existing:
        raise ValueError(f"Chuyên mục '{name}' hoặc slug '{slug}' đã tồn tại!")
    
    db_cat = models.BlogCategory(
        name=name,
        slug=slug,
        description=cat_in.description
    )
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return {
        "id": db_cat.id,
        "name": db_cat.name,
        "slug": db_cat.slug,
        "description": db_cat.description,
        "post_count": 0
    }

def update_blog_category(db: Session, cat_id: int, cat_in: schemas.BlogCategoryUpdate):
    db_cat = db.query(models.BlogCategory).filter(models.BlogCategory.id == cat_id).first()
    if not db_cat:
        return None
    
    old_name = db_cat.name
    update_data = cat_in.model_dump(exclude_unset=True)
    if "name" in update_data and update_data["name"]:
        new_name = update_data["name"].strip()
        dup = db.query(models.BlogCategory).filter(
            models.BlogCategory.name == new_name,
            models.BlogCategory.id != cat_id
        ).first()
        if dup:
            raise ValueError(f"Tên chuyên mục '{new_name}' đã tồn tại!")
        
        # Đồng bộ đổi tên ở tất cả bài viết đang thuộc category cũ
        if old_name != new_name:
            db.query(models.BlogPost).filter(models.BlogPost.category == old_name).update({"category": new_name})
        db_cat.name = new_name

    if "slug" in update_data and update_data["slug"]:
        new_slug = update_data["slug"].strip()
        dup = db.query(models.BlogCategory).filter(
            models.BlogCategory.slug == new_slug,
            models.BlogCategory.id != cat_id
        ).first()
        if dup:
            raise ValueError(f"Mã slug '{new_slug}' đã tồn tại!")
        db_cat.slug = new_slug
    elif "name" in update_data and not update_data.get("slug"):
        db_cat.slug = slugify(db_cat.name)

    if "description" in update_data:
        db_cat.description = update_data["description"]
        
    db.commit()
    db.refresh(db_cat)
    count = db.query(models.BlogPost).filter(models.BlogPost.category == db_cat.name).count()
    return {
        "id": db_cat.id,
        "name": db_cat.name,
        "slug": db_cat.slug,
        "description": db_cat.description,
        "post_count": count
    }

def delete_blog_category(db: Session, cat_id: int):
    db_cat = db.query(models.BlogCategory).filter(models.BlogCategory.id == cat_id).first()
    if not db_cat:
        return False
    post_count = db.query(models.BlogPost).filter(models.BlogPost.category == db_cat.name).count()
    if post_count > 0:
        raise ValueError(f"Không thể xóa chuyên mục '{db_cat.name}' vì đang có {post_count} bài viết liên kết. Vui lòng chuyển các bài viết sang chuyên mục khác trước!")
    
    db.delete(db_cat)
    db.commit()
    return True

# --- Contact CRUD ---
def create_contact(db: Session, contact_in: schemas.ContactCreate):
    db_contact = models.Contact(
        first_name=contact_in.first_name,
        middle_name=contact_in.middle_name or "",
        last_name=contact_in.last_name or "",
        email=contact_in.email,
        phone=contact_in.phone,
        course_handle=contact_in.course_handle or "",
        message=contact_in.message or "Đăng ký tư vấn thông tin từ website ACC Academy"
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# --- User & Auth CRUD ---
def get_user_by_email(db: Session, email: str):
    clean_email = email.strip().lower() if email else ""
    return db.query(models.User).filter(func.lower(models.User.email) == clean_email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user_in: schemas.UserCreate):
    clean_user_email = user_in.email.strip().lower()
    # Check if a referral code was used
    referred_by_id = None
    if user_in.referral_code_used:
        clean_code = user_in.referral_code_used.strip().upper()
        if clean_code:
            referrer = db.query(models.User).filter(func.upper(models.User.referral_code) == clean_code).first()
            if referrer and referrer.email.strip().lower() != clean_user_email:
                referred_by_id = referrer.id

    # Generate a unique referral code for the new user (e.g. ACC-XXXXXX)
    unique_ref = f"ACC-{uuid.uuid4().hex[:6].upper()}"
    
    hashed_pwd = auth.get_password_hash(user_in.password)
    clean_phone = user_in.phone.strip() if user_in.phone and user_in.phone.strip() else None
    db_user = models.User(
        fullname=user_in.fullname,
        email=clean_user_email,
        phone=clean_phone,
        hashed_password=hashed_pwd,
        referral_code=unique_ref,
        referred_by_id=referred_by_id,
        role="student",
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Cart CRUD ---
def get_cart_items(db: Session, user_id: int):
    return db.query(models.CartItem).options(
        joinedload(models.CartItem.course).selectinload(models.Course.tags)
    ).filter(models.CartItem.user_id == user_id).all()

def add_to_cart(db: Session, user_id: int, course_id: int):
    # Check if course is already in the cart
    existing = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id,
        models.CartItem.course_id == course_id
    ).first()
    if existing:
        return existing
        
    db_cart = models.CartItem(user_id=user_id, course_id=course_id)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def remove_from_cart(db: Session, user_id: int, course_id: int):
    db_cart = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id,
        (models.CartItem.course_id == course_id) | (models.CartItem.id == course_id)
    ).first()
    if db_cart:
        db.delete(db_cart)
        db.commit()
        return True
    return False

def clear_cart(db: Session, user_id: int):
    db.query(models.CartItem).filter(models.CartItem.user_id == user_id).delete()
    db.commit()
    return True


# --- Order & Checkout CRUD ---
def get_user_orders(db: Session, user_id: int):
    return db.query(models.Order).options(
        selectinload(models.Order.items).joinedload(models.OrderItem.course)
    ).filter(models.Order.user_id == user_id).all()

def checkout_cart(db: Session, user_id: int):
    # Clean up expired pending orders and any abandoned pending order of this user
    cleanup_expired_pending_orders(db, timeout_minutes=30, cancel_user_pending_id=user_id)

    cart_items = get_cart_items(db, user_id=user_id)
    if not cart_items:
        return None

    # Filter out items user is already enrolled in using batch query
    cart_course_ids = [item.course_id for item in cart_items if item.course_id]
    enrolled_course_ids = get_user_enrolled_course_ids(db, user_id, cart_course_ids)
    
    valid_cart_items = []
    has_removed = False
    for item in cart_items:
        if item.course_id in enrolled_course_ids:
            db.delete(item)
            has_removed = True
        else:
            valid_cart_items.append(item)
            
    if has_removed:
        db.commit()

    if not valid_cart_items:
        return None

    cart_items = valid_cart_items

    # Calculate total standard price
    total_price = sum(item.course.price for item in cart_items)
    
    # Calculate referral discount
    # Friends get a 10% discount on checkout total, capped at 14,500,000 VND
    discount_applied = 0
    user = get_user_by_id(db, user_id)
    if user.referred_by_id:
        # Check if they have any paid orders
        previous_paid_orders = db.query(models.Order).filter(
            models.Order.user_id == user_id,
            models.Order.status == "paid"
        ).count()
        
        # Apply discount only on the first purchase
        if previous_paid_orders == 0:
            potential_discount = int(total_price * 0.10)
            # Capped at 14,500,000 VND
            discount_applied = min(potential_discount, 14500000)

    final_price = total_price - discount_applied

    # Create Order
    db_order = models.Order(
        user_id=user_id,
        total_price=final_price,
        discount_applied=discount_applied,
        status="pending"
    )
    db.add(db_order)
    db.flush() # Persist order to get ID

    # Create Order Items
    for item in cart_items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            course_id=item.course_id,
            price=item.course.price
        )
        db.add(db_item)
        # Giữ lại sản phẩm trong giỏ hàng, chỉ xóa khi đơn hàng đã thanh toán thành công (pay_order)

    db.commit()
    db.refresh(db_order)
    return db_order

def get_commission_percent_for_user_course(db: Session, user_id: int, course_id: int) -> int:
    custom = db.query(models.UserCourseCommission).filter(
        models.UserCourseCommission.user_id == user_id,
        models.UserCourseCommission.course_id == course_id
    ).first()
    if custom:
        return custom.commission_percent
    
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if course and course.default_commission_percent is not None:
        return course.default_commission_percent
        
    return 10

def pay_order(db: Session, order_id: int):
    db_order = (
        db.query(models.Order)
        .filter(models.Order.id == order_id)
        .with_for_update()
        .first()
    )
    if not db_order or db_order.status != "pending":
        return db_order

    # Transition order status to paid
    db_order.status = "paid"
    
    # Track coupon usage upon real payment
    if getattr(db_order, "coupon_code", None):
        coupon_obj = get_coupon_by_code(db, db_order.coupon_code)
        if coupon_obj:
            coupon_obj.times_used += 1
    
    # Xóa các khóa học đã thanh toán thành công khỏi giỏ hàng của user
    paid_course_ids = [item.course_id for item in db_order.items if item.course_id]
    if paid_course_ids:
        db.query(models.CartItem).filter(
            models.CartItem.user_id == db_order.user_id,
            models.CartItem.course_id.in_(paid_course_ids)
        ).delete(synchronize_session=False)

    # Create Enrollment records for each course in this order
    for item in db_order.items:
        existing_enrollment = db.query(models.Enrollment).filter(
            models.Enrollment.user_id == db_order.user_id,
            models.Enrollment.course_id == item.course_id
        ).first()
        if not existing_enrollment:
            db.add(models.Enrollment(
                user_id=db_order.user_id,
                course_id=item.course_id,
                order_id=order_id
            ))

        # Check if item is a Bundle and auto-enroll user into all courses in that bundle
        if item.course:
            bundle = db.query(models.Bundle).filter(
                (models.Bundle.handle == item.course.handle) | (models.Bundle.title == item.course.title)
            ).first()
            if bundle:
                for sub_c in bundle.courses:
                    sub_enr = db.query(models.Enrollment).filter(
                        models.Enrollment.user_id == db_order.user_id,
                        models.Enrollment.course_id == sub_c.id
                    ).first()
                    if not sub_enr:
                        db.add(models.Enrollment(
                            user_id=db_order.user_id,
                            course_id=sub_c.id,
                            order_id=order_id
                        ))
    
    # Check for referral reward (only when actual cash paid > 0, proportional to amount paid)
    if db_order.total_price > 0:
        user = get_user_by_id(db, db_order.user_id)
        if user and user.referred_by_id:
            referrer = (
                db.query(models.User)
                .filter(models.User.id == user.referred_by_id)
                .with_for_update()
                .first()
            )
            if referrer and referrer.id != user.id and referrer.email.strip().lower() != user.email.strip().lower():
                gross_total = sum(item.price for item in db_order.items if item.price and item.price > 0)
                paid_ratio = min(1.0, db_order.total_price / gross_total) if gross_total > 0 else 0.0

                total_earned = 0
                for item in db_order.items:
                    comm_pct = get_commission_percent_for_user_course(db, referrer.id, item.course_id)
                    total_earned += int(item.price * paid_ratio * (comm_pct / 100.0))

                if total_earned > 0:
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

                    # Accumulate store credit balance to referrer for discount on future purchases
                    referrer.store_credit_balance += total_earned

    db.commit()
    db.refresh(db_order)
    return db_order

# --- Referral CRUD ---
def get_referral_summary(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
        
    # Query all users who registered using this referrer's code
    referred_users = db.query(models.User).filter(models.User.referred_by_id == user_id).all()
    
    # Query completed/paid referral rewards for this referrer
    referrals_query = db.query(models.Referral).filter(models.Referral.referrer_id == user_id).all()
    referrals_map = {ref.referred_id: ref for ref in referrals_query}
    
    total_commission = sum(ref.commission_amount for ref in referrals_query if ref.status == "completed")
    
    referrals_list = []
    for ref_user in referred_users:
        ref_record = referrals_map.get(ref_user.id)
        if ref_record:
            rec_id = ref_record.id
            commission = ref_record.commission_amount
            status = ref_record.status
            created_at = ref_record.created_at
        else:
            rec_id = ref_user.id
            commission = 0
            status = "pending"
            created_at = ref_user.created_at
            
        referrals_list.append(schemas.ReferralResponse(
            id=rec_id,
            referred_fullname=ref_user.fullname,
            commission_amount=commission,
            status=status,
            created_at=created_at
        ))
        
    return schemas.ReferralSummary(
        total_referrals=len(referrals_list),
        total_commission_earned=total_commission,
        referral_code=user.referral_code,
        referrals_list=referrals_list
    )

# --- Banner CRUD ---
def get_banners(db: Session, active_only: bool = False):
    query = db.query(models.Banner)
    if active_only:
        query = query.filter(models.Banner.is_active == True)
    return query.order_by(models.Banner.position.asc(), models.Banner.id.asc()).all()

def create_banner(db: Session, banner_in: schemas.BannerCreate):
    db_banner = models.Banner(**banner_in.model_dump())
    db.add(db_banner)
    db.commit()
    db.refresh(db_banner)
    return db_banner

def update_banner(db: Session, banner_id: int, banner_in: schemas.BannerUpdate):
    db_banner = db.query(models.Banner).filter(models.Banner.id == banner_id).first()
    if not db_banner:
        return None
    update_data = banner_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_banner, key, value)
    db.commit()
    db.refresh(db_banner)
    return db_banner

def delete_banner(db: Session, banner_id: int):
    db_banner = db.query(models.Banner).filter(models.Banner.id == banner_id).first()
    if db_banner:
        db.delete(db_banner)
        db.commit()
        return True
    return False


# --- Testimonial CRUD ---
def get_testimonials(db: Session, only_approved: bool = False, course_id: Optional[int] = None):
    query = db.query(models.Testimonial)
    if only_approved:
        query = query.filter(models.Testimonial.is_approved == True)
    if course_id:
        course = db.query(models.Course).filter(models.Course.id == course_id).first()
        if course and course.title:
            from sqlalchemy import or_
            query = query.filter(
                or_(
                    models.Testimonial.course_id == course_id,
                    models.Testimonial.course_name == course.title
                )
            )
        else:
            query = query.filter(models.Testimonial.course_id == course_id)
    return query.order_by(models.Testimonial.id.desc()).all()

# --- Enrollment & Progress CRUD ---
def get_user_enrollments(db: Session, user_id: int):
    # Batch sync missing paid order courses into enrollments table efficiently
    enrolled_course_ids = {
        e.course_id for e in db.query(models.Enrollment.course_id).filter(models.Enrollment.user_id == user_id).all()
    }
    
    paid_items = db.query(models.OrderItem).join(models.Order).filter(
        models.Order.user_id == user_id,
        models.Order.status == "paid"
    ).all()
    
    new_enrollments = []
    for item in paid_items:
        if item.course_id and item.course_id not in enrolled_course_ids:
            new_enrollments.append(models.Enrollment(
                user_id=user_id,
                course_id=item.course_id,
                order_id=item.order_id
            ))
            enrolled_course_ids.add(item.course_id)
            
    if new_enrollments:
        db.add_all(new_enrollments)
        db.commit()

    return db.query(models.Enrollment).options(
        joinedload(models.Enrollment.course).selectinload(models.Course.tags)
    ).filter(models.Enrollment.user_id == user_id).all()

def get_user_enrolled_course_ids(db: Session, user_id: int, course_ids: Optional[List[int]] = None) -> set:
    """Batch retrieves set of enrolled course IDs for a user with minimal queries"""
    q_enr = db.query(models.Enrollment.course_id).filter(models.Enrollment.user_id == user_id)
    if course_ids:
        q_enr = q_enr.filter(models.Enrollment.course_id.in_(course_ids))
    enrolled = {r[0] for r in q_enr.all()}

    # Check paid orders fallback for any courses not yet in Enrollment table
    q_paid = db.query(models.OrderItem.course_id, models.OrderItem.order_id).join(models.Order).filter(
        models.Order.user_id == user_id,
        models.Order.status == "paid"
    )
    if course_ids:
        q_paid = q_paid.filter(models.OrderItem.course_id.in_(course_ids))
    
    missing_enr = []
    for c_id, o_id in q_paid.all():
        if c_id and c_id not in enrolled:
            enrolled.add(c_id)
            missing_enr.append(models.Enrollment(user_id=user_id, course_id=c_id, order_id=o_id))
    
    if missing_enr:
        db.add_all(missing_enr)
        db.commit()

    return enrolled

def check_enrollment(db: Session, user_id: int, course_id: int) -> bool:
    enrolled_ids = get_user_enrolled_course_ids(db, user_id, [course_id])
    return course_id in enrolled_ids

def enroll_user_in_course(db: Session, user_id: int, course_id: int, order_id: Optional[int] = None):
    existing = db.query(models.Enrollment).filter(
        models.Enrollment.user_id == user_id,
        models.Enrollment.course_id == course_id
    ).first()
    if existing:
        db.refresh(existing)
        return existing
    new_enr = models.Enrollment(
        user_id=user_id,
        course_id=course_id,
        order_id=order_id
    )
    db.add(new_enr)
    db.commit()
    db.refresh(new_enr)
    return new_enr

def get_user_course_progress(db: Session, user_id: int, course_id: int) -> list:
    enr = db.query(models.Enrollment).filter(
        models.Enrollment.user_id == user_id,
        models.Enrollment.course_id == course_id
    ).first()
    if enr and enr.progress_data:
        try:
            return json.loads(enr.progress_data)
        except Exception:
            return []
    return []

def update_user_course_progress(db: Session, user_id: int, course_id: int, completed_lessons: list):
    enr = db.query(models.Enrollment).filter(
        models.Enrollment.user_id == user_id,
        models.Enrollment.course_id == course_id
    ).first()
    if not enr:
        enr = models.Enrollment(user_id=user_id, course_id=course_id)
        db.add(enr)
    enr.progress_data = json.dumps(completed_lessons)
    db.commit()
    return completed_lessons

# --- Checkout with Coupon & Store Credit CRUD ---
def cleanup_expired_pending_orders(
    db: Session,
    timeout_minutes: int = 30,
    cancel_user_pending_id: Optional[int] = None
) -> int:
    """
    Cancels pending orders that have exceeded timeout_minutes, and optionally cancels
    any existing pending orders of cancel_user_pending_id so store credit & coupon usage
    are refunded before a new checkout.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=timeout_minutes)
    pending_orders = db.query(models.Order).filter(models.Order.status == "pending").all()
    cancelled_count = 0

    for o in pending_orders:
        is_user_recheckout = cancel_user_pending_id is not None and o.user_id == cancel_user_pending_id
        order_time = o.created_at
        if order_time is not None and order_time.tzinfo is None:
            order_time = order_time.replace(tzinfo=timezone.utc)
        is_expired = order_time is not None and order_time < cutoff

        if is_user_recheckout or is_expired:
            cancel_order(db, o.id)
            cancelled_count += 1

    return cancelled_count


def checkout_cart_with_options(db: Session, user_id: int, coupon_code: Optional[str] = None, use_store_credit: bool = False):
    # Clean up expired pending orders and refund any previous abandoned pending order of this user
    cleanup_expired_pending_orders(db, timeout_minutes=30, cancel_user_pending_id=user_id)

    cart_items = get_cart_items(db, user_id=user_id)
    if not cart_items:
        return None

    # Filter out items user is already enrolled in using batch query
    cart_course_ids = [item.course_id for item in cart_items if item.course_id]
    enrolled_course_ids = get_user_enrolled_course_ids(db, user_id, cart_course_ids)
    
    valid_cart_items = []
    has_removed = False
    for item in cart_items:
        if item.course_id in enrolled_course_ids:
            db.delete(item)
            has_removed = True
        else:
            valid_cart_items.append(item)
            
    if has_removed:
        db.commit()

    if not valid_cart_items:
        return None

    total_price = sum(item.course.price for item in valid_cart_items)
    discount_applied = 0

    # 1. Referral discount for first purchase if referred (capped at 14,500,000 VND)
    user = db.query(models.User).filter(models.User.id == user_id).with_for_update().first()
    if user and user.referred_by_id:
        previous_paid_orders = db.query(models.Order).filter(
            models.Order.user_id == user_id,
            models.Order.status == "paid"
        ).count()
        if previous_paid_orders == 0:
            discount_applied += min(int(total_price * 0.10), 14500000)

    # 2. Coupon Discount
    if coupon_code:
        coupon = get_coupon_by_code(db, coupon_code)
        now = datetime.now(timezone.utc)
        if not coupon or not coupon.is_active:
            raise ValueError("Mã giảm giá không hợp lệ hoặc đã ngừng hoạt động!")
        if coupon.usage_limit > 0 and coupon.times_used >= coupon.usage_limit:
            raise ValueError("Mã giảm giá đã hết lượt sử dụng!")
        if coupon.valid_from:
            v_from = coupon.valid_from.replace(tzinfo=timezone.utc) if coupon.valid_from.tzinfo is None else coupon.valid_from
            if now < v_from:
                raise ValueError("Mã giảm giá chưa đến thời hạn áp dụng!")
        if coupon.valid_to:
            v_to = coupon.valid_to.replace(tzinfo=timezone.utc) if coupon.valid_to.tzinfo is None else coupon.valid_to
            if now > v_to:
                raise ValueError("Mã giảm giá đã quá hạn sử dụng!")
        if total_price < coupon.min_order_value:
            raise ValueError(f"Đơn hàng phải đạt từ {coupon.min_order_value:,} VNĐ mới áp dụng được mã này!")

        if coupon.discount_type == "percent":
            c_disc = int(total_price * (coupon.discount_value / 100.0))
            if coupon.max_discount_amount > 0:
                c_disc = min(c_disc, coupon.max_discount_amount)
        else:
            c_disc = coupon.discount_value
        
        c_disc = min(c_disc, max(0, total_price - discount_applied))
        discount_applied += c_disc

    # 3. Store Credit Discount
    credit_to_use = 0
    if use_store_credit and user and user.store_credit_balance > 0:
        remaining_payable = max(0, total_price - discount_applied)
        credit_to_use = min(user.store_credit_balance, remaining_payable)
        discount_applied += credit_to_use
        user.store_credit_balance -= credit_to_use

    final_price = max(0, total_price - discount_applied)

    # Create Order
    db_order = models.Order(
        user_id=user_id,
        total_price=final_price,
        discount_applied=discount_applied,
        store_credit_used=credit_to_use,
        coupon_code=coupon.code if (coupon_code and 'coupon' in locals() and coupon) else None,
        status="pending"
    )
    db.add(db_order)
    db.flush()

    for item in valid_cart_items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            course_id=item.course_id,
            price=item.course.price
        )
        db.add(db_item)
        # Giữ lại sản phẩm trong giỏ hàng, chỉ xóa khi đơn hàng đã thanh toán thành công (pay_order)

    db.commit()
    db.refresh(db_order)
    return db_order

def cancel_order(db: Session, order_id: int):
    """Safely cancels a pending order and refunds store credit & coupon usage."""
    order = (
        db.query(models.Order)
        .filter(models.Order.id == order_id)
        .with_for_update()
        .first()
    )
    if not order or order.status != "pending":
        return order

    # Refund store credit
    if getattr(order, "store_credit_used", 0) and order.store_credit_used > 0:
        user = (
            db.query(models.User)
            .filter(models.User.id == order.user_id)
            .with_for_update()
            .first()
        )
        if user:
            user.store_credit_balance += order.store_credit_used
        order.store_credit_used = 0

    # Revert coupon usage
    if getattr(order, "coupon_code", None):
        coupon = get_coupon_by_code(db, order.coupon_code)
        if coupon and coupon.times_used > 0:
            coupon.times_used -= 1

    order.status = "cancelled"
    db.commit()
    db.refresh(order)
    return order

# --- Review CRUD ---
def get_course_reviews(db: Session, course_id: int):
    return db.query(models.CourseReview).filter(
        models.CourseReview.course_id == course_id,
        models.CourseReview.is_approved == True
    ).order_by(models.CourseReview.created_at.desc()).all()

def create_course_review(db: Session, user_id: int, course_id: int, rating: int, comment: str):
    review = models.CourseReview(
        user_id=user_id,
        course_id=course_id,
        rating=max(1, min(5, rating)),
        comment=comment,
        is_approved=True
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

# --- Lesson Note CRUD ---
def get_user_lesson_notes(db: Session, user_id: int, course_id: int):
    return db.query(models.LessonNote).filter(
        models.LessonNote.user_id == user_id,
        models.LessonNote.course_id == course_id
    ).order_by(models.LessonNote.timestamp_seconds.asc()).all()

def create_lesson_note(db: Session, user_id: int, course_id: int, lesson_id: str, timestamp_seconds: int, note_text: str):
    note = models.LessonNote(
        user_id=user_id,
        course_id=course_id,
        lesson_id=lesson_id,
        timestamp_seconds=timestamp_seconds,
        note_text=note_text
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def delete_lesson_note(db: Session, user_id: int, note_id: int):
    note = db.query(models.LessonNote).filter(
        models.LessonNote.id == note_id,
        models.LessonNote.user_id == user_id
    ).first()
    if note:
        db.delete(note)
        db.commit()
        return True
    return False

# --- Wishlist CRUD ---
def get_user_wishlists(db: Session, user_id: int):
    return db.query(models.Wishlist).filter(models.Wishlist.user_id == user_id).all()

def toggle_wishlist(db: Session, user_id: int, course_id: int):
    existing = db.query(models.Wishlist).filter(
        models.Wishlist.user_id == user_id,
        models.Wishlist.course_id == course_id
    ).first()
    if existing:
        db.delete(existing)
        db.commit()
        return False # Removed from wishlist
    else:
        new_item = models.Wishlist(user_id=user_id, course_id=course_id)
        db.add(new_item)
        db.commit()
        return True # Added to wishlist

# --- Coupon CRUD ---
def get_coupon_by_code(db: Session, code: str):
    clean_code = code.strip().upper() if code else ""
    return db.query(models.Coupon).filter(func.upper(models.Coupon.code) == clean_code).first()

def get_all_coupons(db: Session):
    return db.query(models.Coupon).order_by(models.Coupon.id.desc()).all()

def create_coupon(db: Session, coupon_in: schemas.CouponCreate):
    coupon = models.Coupon(
        code=coupon_in.code.strip().upper(),
        discount_type=coupon_in.discount_type,
        discount_value=coupon_in.discount_value,
        min_order_value=coupon_in.min_order_value or 0,
        max_discount_amount=coupon_in.max_discount_amount or 0,
        usage_limit=coupon_in.usage_limit or 0,
        valid_from=coupon_in.valid_from,
        valid_to=coupon_in.valid_to,
        is_active=coupon_in.is_active if coupon_in.is_active is not None else True
    )
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon

def delete_coupon(db: Session, coupon_id: int):
    coupon = db.query(models.Coupon).filter(models.Coupon.id == coupon_id).first()
    if coupon:
        db.delete(coupon)
        db.commit()
        return True
    return False

# --- Custom Commission CRUD ---
def get_custom_commissions(db: Session):
    return db.query(models.UserCourseCommission).all()

def set_custom_commission(db: Session, user_id: int, course_id: int, commission_percent: int):
    existing = db.query(models.UserCourseCommission).filter(
        models.UserCourseCommission.user_id == user_id,
        models.UserCourseCommission.course_id == course_id
    ).first()
    if existing:
        existing.commission_percent = commission_percent
        db.commit()
        db.refresh(existing)
        return existing
    else:
        new_comm = models.UserCourseCommission(
            user_id=user_id,
            course_id=course_id,
            commission_percent=commission_percent
        )
        db.add(new_comm)
        db.commit()
        db.refresh(new_comm)
        return new_comm


# --- Blog Post Extended CRUD ---
def get_blog_by_id_or_handle(db: Session, identifier: str):
    if identifier.isdigit():
        blog = db.query(models.BlogPost).filter(models.BlogPost.id == int(identifier)).first()
        if blog:
            return blog
    return db.query(models.BlogPost).filter(models.BlogPost.handle == identifier).first()

def create_blog_post(db: Session, blog_in: schemas.BlogPostCreate):
    db_blog = models.BlogPost(**blog_in.model_dump())
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def update_blog_post(db: Session, blog_id: int, blog_in: schemas.BlogPostUpdate):
    db_blog = db.query(models.BlogPost).filter(models.BlogPost.id == blog_id).first()
    if not db_blog:
        return None
    for key, value in blog_in.model_dump(exclude_unset=True).items():
        setattr(db_blog, key, value)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def delete_blog_post(db: Session, blog_id: int):
    db_blog = db.query(models.BlogPost).filter(models.BlogPost.id == blog_id).first()
    if db_blog:
        db.delete(db_blog)
        db.commit()
        return True
    return False


# --- Testimonial Extended CRUD ---
def get_testimonial_by_id(db: Session, testimonial_id: int):
    return db.query(models.Testimonial).filter(models.Testimonial.id == testimonial_id).first()

def create_testimonial(db: Session, test_in: schemas.TestimonialCreate):
    db_test = models.Testimonial(**test_in.model_dump())
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

def update_testimonial(db: Session, testimonial_id: int, test_in: schemas.TestimonialUpdate):
    db_test = db.query(models.Testimonial).filter(models.Testimonial.id == testimonial_id).first()
    if not db_test:
        return None
    for key, value in test_in.model_dump(exclude_unset=True).items():
        setattr(db_test, key, value)
    db.commit()
    db.refresh(db_test)
    return db_test

def delete_testimonial(db: Session, testimonial_id: int):
    db_test = db.query(models.Testimonial).filter(models.Testimonial.id == testimonial_id).first()
    if db_test:
        db.delete(db_test)
        db.commit()
        return True
    return False


# --- Lecturer Major CRUD ---
def get_lecturer_majors(db: Session):
    return db.query(models.LecturerMajor).order_by(models.LecturerMajor.position.asc(), models.LecturerMajor.id.asc()).all()

def get_lecturer_major_by_id(db: Session, major_id: str):
    return db.query(models.LecturerMajor).filter(models.LecturerMajor.id == major_id).first()

def create_lecturer_major(db: Session, major_in: schemas.LecturerMajorCreate):
    db_major = models.LecturerMajor(**major_in.model_dump())
    db.add(db_major)
    db.commit()
    db.refresh(db_major)
    return db_major

def update_lecturer_major(db: Session, major_id: str, major_in: schemas.LecturerMajorUpdate):
    db_major = db.query(models.LecturerMajor).filter(models.LecturerMajor.id == major_id).first()
    if not db_major:
        return None
    for key, value in major_in.model_dump(exclude_unset=True).items():
        setattr(db_major, key, value)
    db.commit()
    db.refresh(db_major)
    return db_major

def delete_lecturer_major(db: Session, major_id: str):
    db_major = db.query(models.LecturerMajor).filter(models.LecturerMajor.id == major_id).first()
    if db_major:
        # Nullify major_id for lecturers assigned to this major
        db.query(models.Lecturer).filter(models.Lecturer.major_id == major_id).update({"major_id": None, "major_name": None})
        db.delete(db_major)
        db.commit()
        return True
    return False

# --- Lecturer CRUD ---
def get_lecturers(db: Session, featured_only: bool = False, include_details: bool = False):
    query = db.query(models.Lecturer)
    if not include_details:
        query = query.options(defer(models.Lecturer.details_html))
    if featured_only:
        query = query.filter(models.Lecturer.is_featured == True)
    return query.order_by(models.Lecturer.position.asc(), models.Lecturer.name.asc()).all()

def get_lecturer_by_id(db: Session, lecturer_id: str):
    return db.query(models.Lecturer).filter(models.Lecturer.id == lecturer_id).first()

def create_lecturer(db: Session, lecturer_in: schemas.LecturerCreate):
    data = lecturer_in.model_dump()
    if data.get("major_id") and not data.get("major_name"):
        m = get_lecturer_major_by_id(db, data["major_id"])
        if m:
            data["major_name"] = m.name
    db_lecturer = models.Lecturer(**data)
    db.add(db_lecturer)
    db.commit()
    db.refresh(db_lecturer)
    return db_lecturer

def update_lecturer(db: Session, lecturer_id: str, lecturer_in: schemas.LecturerUpdate):
    db_lecturer = db.query(models.Lecturer).filter(models.Lecturer.id == lecturer_id).first()
    if not db_lecturer:
        return None
    
    # Check max 4 featured limit if trying to set is_featured = True
    update_data = lecturer_in.model_dump(exclude_unset=True)
    if update_data.get("is_featured") is True and not db_lecturer.is_featured:
        current_featured_count = db.query(models.Lecturer).filter(models.Lecturer.is_featured == True).count()
        if current_featured_count >= 4:
            raise ValueError("Đã đạt giới hạn tối đa 4 Giảng viên ưu tiên ngoài Trang chủ!")

    if "major_id" in update_data and update_data["major_id"]:
        m = get_lecturer_major_by_id(db, update_data["major_id"])
        if m:
            update_data["major_name"] = m.name

    for key, value in update_data.items():
        setattr(db_lecturer, key, value)
    db.commit()
    db.refresh(db_lecturer)
    return db_lecturer

def reorder_lecturers(db: Session, items: list, major_id: Optional[str] = None):
    for item in items:
        lec_id = item.id if hasattr(item, 'id') else item.get('id')
        pos = item.position if hasattr(item, 'position') else item.get('position')
        db_lec = db.query(models.Lecturer).filter(models.Lecturer.id == lec_id).first()
        if db_lec:
            if major_id and major_id != 'all':
                current_positions = dict(db_lec.major_positions or {})
                current_positions[major_id] = pos
                db_lec.major_positions = current_positions
                flag_modified(db_lec, "major_positions")
            else:
                db_lec.position = pos
    db.commit()
    return True

def toggle_lecturer_featured(db: Session, lecturer_id: str):
    db_lecturer = db.query(models.Lecturer).filter(models.Lecturer.id == lecturer_id).first()
    if not db_lecturer:
        return None
    if not db_lecturer.is_featured:
        current_featured_count = db.query(models.Lecturer).filter(models.Lecturer.is_featured == True).count()
        if current_featured_count >= 4:
            raise ValueError("Đã đạt giới hạn tối đa 4 Giảng viên ưu tiên ngoài Trang chủ!")
        db_lecturer.is_featured = True
    else:
        db_lecturer.is_featured = False
    db.commit()
    db.refresh(db_lecturer)
    return db_lecturer

def delete_lecturer(db: Session, lecturer_id: str):
    db_lecturer = db.query(models.Lecturer).filter(models.Lecturer.id == lecturer_id).first()
    if db_lecturer:
        db.delete(db_lecturer)
        db.commit()
        return True
    return False


# --- Project CRUD ---
def get_projects(db: Session, category: Optional[str] = None):
    query = db.query(models.Project)
    if category:
        query = query.filter(models.Project.category == category)
    return query.all()

def get_project_by_id(db: Session, project_id: str):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def create_project(db: Session, project_in: schemas.ProjectCreate):
    db_project = models.Project(**project_in.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, project_id: str, project_in: schemas.ProjectUpdate):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        return None
    for key, value in project_in.model_dump(exclude_unset=True).items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: str):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project:
        db.delete(db_project)
        db.commit()
        return True
    return False

# --- Project Review CRUD ---
def get_project_reviews(db: Session, project_id: str):
    return db.query(models.ProjectReview).filter(
        models.ProjectReview.project_id == project_id,
        models.ProjectReview.is_approved == True
    ).order_by(models.ProjectReview.created_at.desc()).all()

def create_project_review(
    db: Session,
    project_id: str,
    author_name: str,
    author_email: Optional[str],
    rating: int,
    comment: str,
    user_id: Optional[int] = None
):
    review = models.ProjectReview(
        project_id=project_id,
        user_id=user_id,
        author_name=author_name,
        author_email=author_email,
        rating=max(1, min(5, rating)),
        comment=comment,
        is_approved=False # Requires admin approval
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_all_project_reviews_admin(db: Session, project_id: Optional[str] = None):
    query = db.query(models.ProjectReview)
    if project_id:
        query = query.filter(models.ProjectReview.project_id == project_id)
    return query.order_by(models.ProjectReview.created_at.desc()).all()

def update_project_review(db: Session, review_id: int, review_in: schemas.ProjectReviewUpdate):
    review = db.query(models.ProjectReview).filter(models.ProjectReview.id == review_id).first()
    if not review:
        return None
    for key, value in review_in.model_dump(exclude_unset=True).items():
        setattr(review, key, value)
    db.commit()
    db.refresh(review)
    return review

def delete_project_review(db: Session, review_id: int):
    review = db.query(models.ProjectReview).filter(models.ProjectReview.id == review_id).first()
    if review:
        db.delete(review)
        db.commit()
        return True
    return False

# --- Partner CRUD ---
def get_partners(db: Session, active_only: bool = False):
    query = db.query(models.Partner)
    if active_only:
        query = query.filter(models.Partner.is_active == True)
    return query.order_by(models.Partner.position.asc(), models.Partner.id.asc()).all()

def get_partner_by_id(db: Session, partner_id: int):
    return db.query(models.Partner).filter(models.Partner.id == partner_id).first()

def create_partner(db: Session, partner_in: schemas.PartnerCreate):
    partner = models.Partner(
        name=partner_in.name,
        src=partner_in.src,
        link=partner_in.link,
        position=partner_in.position or 0,
        row_type=partner_in.row_type or "marquee",
        is_active=partner_in.is_active if partner_in.is_active is not None else True
    )
    db.add(partner)
    db.commit()
    db.refresh(partner)
    return partner

def update_partner(db: Session, partner_id: int, partner_in: schemas.PartnerUpdate):
    partner = get_partner_by_id(db, partner_id)
    if not partner:
        return None
    for key, value in partner_in.model_dump(exclude_unset=True).items():
        setattr(partner, key, value)
    db.commit()
    db.refresh(partner)
    return partner

def delete_partner(db: Session, partner_id: int):
    partner = get_partner_by_id(db, partner_id)
    if partner:
        db.delete(partner)
        db.commit()
        return True
    return False

# --- Board Member CRUD ---
def get_board_members(db: Session, active_only: bool = False, role_group: str = None):
    query = db.query(models.BoardMember)
    if active_only:
        query = query.filter(models.BoardMember.is_active == True)
    if role_group:
        query = query.filter(models.BoardMember.role_group == role_group)
    return query.order_by(models.BoardMember.position.asc(), models.BoardMember.id.asc()).all()

def get_board_member_by_id(db: Session, member_id: int):
    return db.query(models.BoardMember).filter(models.BoardMember.id == member_id).first()

def create_board_member(db: Session, member_in: schemas.BoardMemberCreate):
    member = models.BoardMember(
        name=member_in.name,
        main_role=member_in.main_role,
        role_group=member_in.role_group or 'executive',
        avatar=member_in.avatar,
        bio_list=member_in.bio_list,
        position=member_in.position or 0,
        is_active=member_in.is_active if member_in.is_active is not None else True
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

def update_board_member(db: Session, member_id: int, member_in: schemas.BoardMemberUpdate):
    member = get_board_member_by_id(db, member_id)
    if not member:
        return None
    for key, value in member_in.model_dump(exclude_unset=True).items():
        setattr(member, key, value)
    db.commit()
    db.refresh(member)
    return member

def delete_board_member(db: Session, member_id: int):
    member = get_board_member_by_id(db, member_id)
    if member:
        db.delete(member)
        db.commit()
        return True
    return False

# --- Admission Post CRUD ---
def get_admission_posts(db: Session, active_only: bool = False):
    query = db.query(models.AdmissionPost)
    if active_only:
        query = query.filter(models.AdmissionPost.is_active == True)
    return query.order_by(models.AdmissionPost.position.asc(), models.AdmissionPost.id.asc()).all()

def get_admission_post_by_id(db: Session, post_id: int):
    return db.query(models.AdmissionPost).filter(models.AdmissionPost.id == post_id).first()

def get_admission_post_by_slug(db: Session, slug: str, active_only: bool = False):
    query = db.query(models.AdmissionPost).filter(models.AdmissionPost.slug == slug)
    if active_only:
        query = query.filter(models.AdmissionPost.is_active == True)
    return query.first()

def create_admission_post(db: Session, post_in: schemas.AdmissionPostCreate):
    post = models.AdmissionPost(
        slug=post_in.slug,
        title=post_in.title,
        subtitle=post_in.subtitle,
        category=post_in.category,
        tag=post_in.tag,
        image=post_in.image,
        highlights=post_in.highlights,
        content=post_in.content,
        position=post_in.position or 0,
        is_active=post_in.is_active if post_in.is_active is not None else True
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def update_admission_post(db: Session, post_id: int, post_in: schemas.AdmissionPostUpdate):
    post = get_admission_post_by_id(db, post_id)
    if not post:
        return None
    for key, value in post_in.model_dump(exclude_unset=True).items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post

def delete_admission_post(db: Session, post_id: int):
    post = get_admission_post_by_id(db, post_id)
    if post:
        db.delete(post)
        db.commit()
        return True
    return False

