import uuid
import json
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
    
    # Check for referral reward
    user = get_user_by_id(db, db_order.user_id)
    if user and user.referred_by_id:
        referrer_exists = db.query(models.User).filter(models.User.id == user.referred_by_id).first()
        if referrer_exists:
            existing_referral = db.query(models.Referral).filter(
                models.Referral.referred_id == user.id
            ).first()
            
            if not existing_referral:
                commission = int(db_order.total_price * 0.10)
                commission_capped = min(commission, 29000000)
                
                db_referral = models.Referral(
                    referrer_id=user.referred_by_id,
                    referred_id=user.id,
                    commission_amount=commission_capped,
                    status="completed"
                )
                db.add(db_referral)

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
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user and user.role == "admin":
        return True
    
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
