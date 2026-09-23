import uuid
import json
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from . import models, schemas, auth

# --- Category & Course CRUD ---
def get_courses(db: Session, category_slug: str = None):
    query = db.query(models.Course)
    if category_slug:
        clean_slug = category_slug.strip().lower()
        query = query.filter(func.lower(models.Course.category_slug) == clean_slug)
    return query.all()

def get_course_by_handle(db: Session, handle: str):
    return db.query(models.Course).filter(models.Course.handle == handle).first()

def get_categories(db: Session):
    return db.query(models.Category).all()

# --- Blog CRUD ---
def get_blog_posts(db: Session):
    return db.query(models.BlogPost).all()

# --- Contact CRUD ---
def create_contact(db: Session, contact_in: schemas.ContactCreate):
    db_contact = models.Contact(
        first_name=contact_in.first_name,
        middle_name=contact_in.middle_name,
        last_name=contact_in.last_name,
        email=contact_in.email,
        phone=contact_in.phone,
        course_handle=contact_in.course_handle,
        message=contact_in.message
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
    # Check if a referral code was used
    referred_by_id = None
    if user_in.referral_code_used:
        clean_code = user_in.referral_code_used.strip().upper()
        if clean_code:
            referrer = db.query(models.User).filter(func.upper(models.User.referral_code) == clean_code).first()
            if referrer:
                referred_by_id = referrer.id

    # Generate a unique referral code for the new user (e.g. ACC-XXXXXX)
    unique_ref = f"ACC-{uuid.uuid4().hex[:6].upper()}"
    
    hashed_pwd = auth.get_password_hash(user_in.password)
    db_user = models.User(
        fullname=user_in.fullname,
        email=user_in.email.strip().lower(),
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
    return db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()

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
        models.CartItem.course_id == course_id
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
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()

def checkout_cart(db: Session, user_id: int):
    cart_items = get_cart_items(db, user_id=user_id)
    if not cart_items:
        return None

    # Filter out items user is already enrolled in
    valid_cart_items = []
    has_removed = False
    for item in cart_items:
        if check_enrollment(db, user_id=user_id, course_id=item.course_id):
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
        db.delete(item) # Remove from cart online

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
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order or db_order.status != "pending":
        return db_order

    # Transition order status to paid
    db_order.status = "paid"
    
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
    
    # Check for referral reward
    user = get_user_by_id(db, db_order.user_id)
    if user and user.referred_by_id:
        referrer = db.query(models.User).filter(models.User.id == user.referred_by_id).first()
        if referrer:
            existing_referral = db.query(models.Referral).filter(
                models.Referral.referred_id == user.id
            ).first()
            
            # Calculate total custom/default commission for each item in the order
            total_earned = 0
            for item in db_order.items:
                comm_pct = get_commission_percent_for_user_course(db, referrer.id, item.course_id)
                total_earned += int(item.price * (comm_pct / 100.0))
                
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
def get_testimonials(db: Session):
    return db.query(models.Testimonial).all()

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

    return db.query(models.Enrollment).filter(models.Enrollment.user_id == user_id).all()

def check_enrollment(db: Session, user_id: int, course_id: int) -> bool:
    existing = db.query(models.Enrollment).filter(
        models.Enrollment.user_id == user_id,
        models.Enrollment.course_id == course_id
    ).first()
    if existing:
        return True

    # Fallback to paid order items check
    paid_order_item = db.query(models.OrderItem).join(models.Order).filter(
        models.Order.user_id == user_id,
        models.Order.status == "paid",
        models.OrderItem.course_id == course_id
    ).first()
    if paid_order_item:
        auto_enr = models.Enrollment(user_id=user_id, course_id=course_id, order_id=paid_order_item.order_id)
        db.add(auto_enr)
        db.commit()
        return True

    return False

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
def checkout_cart_with_options(db: Session, user_id: int, coupon_code: Optional[str] = None, use_store_credit: bool = False):
    cart_items = get_cart_items(db, user_id=user_id)
    if not cart_items:
        return None

    # Filter out items user is already enrolled in
    valid_cart_items = []
    has_removed = False
    for item in cart_items:
        if check_enrollment(db, user_id=user_id, course_id=item.course_id):
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

    # 1. Referral discount for first purchase if referred
    user = get_user_by_id(db, user_id)
    if user.referred_by_id:
        previous_paid_orders = db.query(models.Order).filter(
            models.Order.user_id == user_id,
            models.Order.status == "paid"
        ).count()
        if previous_paid_orders == 0:
            discount_applied += int(total_price * 0.10)

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
        coupon.times_used += 1

    # 3. Store Credit Discount
    if use_store_credit and user.store_credit_balance > 0:
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
        db.delete(item)

    db.commit()
    db.refresh(db_order)
    return db_order

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


# --- Lecturer CRUD ---
def get_lecturers(db: Session):
    return db.query(models.Lecturer).all()

def get_lecturer_by_id(db: Session, lecturer_id: str):
    return db.query(models.Lecturer).filter(models.Lecturer.id == lecturer_id).first()

def create_lecturer(db: Session, lecturer_in: schemas.LecturerCreate):
    db_lecturer = models.Lecturer(**lecturer_in.model_dump())
    db.add(db_lecturer)
    db.commit()
    db.refresh(db_lecturer)
    return db_lecturer

def update_lecturer(db: Session, lecturer_id: str, lecturer_in: schemas.LecturerUpdate):
    db_lecturer = db.query(models.Lecturer).filter(models.Lecturer.id == lecturer_id).first()
    if not db_lecturer:
        return None
    for key, value in lecturer_in.model_dump(exclude_unset=True).items():
        setattr(db_lecturer, key, value)
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


