import uuid
from sqlalchemy.orm import Session
from . import models, schemas, auth

# --- Category & Course CRUD ---
def get_courses(db: Session, category_slug: str = None):
    query = db.query(models.Course)
    if category_slug:
        query = query.filter(models.Course.category_slug == category_slug)
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
        name=contact_in.name,
        email=contact_in.email,
        course_handle=contact_in.course_handle,
        message=contact_in.message
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# --- User & Auth CRUD ---
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user_in: schemas.UserCreate):
    # Check if a referral code was used
    referred_by_id = None
    if user_in.referral_code_used:
        referrer = db.query(models.User).filter(models.User.referral_code == user_in.referral_code_used).first()
        if referrer:
            referred_by_id = referrer.id

    # Generate a unique referral code for the new user (e.g. ACC-XXXXXX)
    unique_ref = f"ACC-{uuid.uuid4().hex[:6].upper()}"
    
    hashed_pwd = auth.get_password_hash(user_in.password)
    db_user = models.User(
        fullname=user_in.fullname,
        email=user_in.email,
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

# --- Order & Checkout CRUD ---
def get_user_orders(db: Session, user_id: int):
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()

def checkout_cart(db: Session, user_id: int):
    cart_items = get_cart_items(db, user_id=user_id)
    if not cart_items:
        return None

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
    
    # Check for referral reward
    # If the user was referred by someone, award the referrer commission
    user = get_user_by_id(db, db_order.user_id)
    if user.referred_by_id:
        # Check if a referral reward record has already been logged for this pair
        existing_referral = db.query(models.Referral).filter(
            models.Referral.referred_id == user.id
        ).first()
        
        if not existing_referral:
            # Referrer gets 10% commission on the paid order amount, capped at 29,000,000 VND
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
        
    referrals_query = db.query(models.Referral).filter(models.Referral.referrer_id == user_id).all()
    
    total_commission = sum(ref.commission_amount for ref in referrals_query if ref.status == "completed")
    
    referrals_list = []
    for ref in referrals_query:
        referred_user = get_user_by_id(db, ref.referred_id)
        referrals_list.append(schemas.ReferralResponse(
            id=ref.id,
            referred_fullname=referred_user.fullname if referred_user else "Unknown Friend",
            commission_amount=ref.commission_amount,
            status=ref.status,
            created_at=ref.created_at
        ))
        
    return schemas.ReferralSummary(
        total_referrals=len(referrals_list),
        total_commission_earned=total_commission,
        referral_code=user.referral_code,
        referrals_list=referrals_list
    )
