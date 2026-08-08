from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey, Text, DateTime, Boolean, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Category(Base):
    __tablename__ = "categories"

    slug = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    courses = relationship("Course", back_populates="category")

# Junction Table for Bundles <-> Courses
bundle_courses = Table(
    'bundle_courses',
    Base.metadata,
    Column('bundle_id', Integer, ForeignKey('bundles.id', ondelete="CASCADE"), primary_key=True),
    Column('course_id', BigInteger, ForeignKey('courses.id', ondelete="CASCADE"), primary_key=True)
)

# Junction Table for Bundles <-> Gift Courses
bundle_gift_courses = Table(
    'bundle_gift_courses',
    Base.metadata,
    Column('bundle_id', Integer, ForeignKey('bundles.id', ondelete="CASCADE"), primary_key=True),
    Column('course_id', BigInteger, ForeignKey('courses.id', ondelete="CASCADE"), primary_key=True)
)

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    image = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    courses = relationship("Course", back_populates="program")

class Bundle(Base):
    __tablename__ = "bundles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    handle = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)
    original_price = Column(Integer, nullable=True)
    image = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    courses = relationship("Course", secondary=bundle_courses, backref="bundles")
    gift_courses = relationship("Course", secondary=bundle_gift_courses, backref="gift_bundles")

class Course(Base):
    __tablename__ = "courses"

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category_slug = Column(String(50), ForeignKey("categories.slug"), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=True)
    handle = Column(String(100), nullable=False, unique=True, index=True)
    price = Column(Integer, nullable=False)
    original_price = Column(Integer, nullable=True)
    image = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    duration = Column(String(50), nullable=True)
    level = Column(String(50), nullable=True)
    curriculum_data = Column(Text, nullable=True)

    category = relationship("Category", back_populates="courses")
    program = relationship("Program", back_populates="courses")
    tags = relationship("CourseTag", back_populates="course", cascade="all, delete-orphan")

class CourseTag(Base):
    __tablename__ = "course_tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(BigInteger, ForeignKey("courses.id"), nullable=False)
    tag = Column(String(100), nullable=False)

    course = relationship("Course", back_populates="tags")

class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    handle = Column(String(100), nullable=False, unique=True, index=True)
    category = Column(String(100), nullable=False)
    excerpt = Column(Text, nullable=True)
    image = Column(String(255), nullable=True)
    date = Column(String(50), nullable=True)
    link = Column(String(255), nullable=True)

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(50), nullable=False)
    course_handle = Column(String(100), nullable=True)
    message = Column(Text, nullable=False)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    referral_code = Column(String(50), unique=True, index=True, nullable=False)
    referred_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    role = Column(String(50), default="student") # student, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Integer, nullable=False)
    discount_applied = Column(Integer, default=0)
    status = Column(String(50), default="pending") # pending, paid, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    course_id = Column(BigInteger, ForeignKey("courses.id"), nullable=False)
    price = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    course = relationship("Course")

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(BigInteger, ForeignKey("courses.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="cart_items")
    course = relationship("Course")

class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    referred_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    commission_amount = Column(Integer, default=0)
    status = Column(String(50), default="pending") # pending, completed (paid out)
    created_at = Column(DateTime, default=datetime.utcnow)

    referrer = relationship("User", foreign_keys=[referrer_id])
    referred = relationship("User", foreign_keys=[referred_id])

class Testimonial(Base):
    __tablename__ = "testimonials"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    role = Column(String(150), nullable=False)
    text = Column(Text, nullable=False)
    image = Column(String(255), nullable=True)
    video_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Enrollment(Base):
    """Tracks which user has access to which course (after payment)."""
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(BigInteger, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="SET NULL"), nullable=True)
    enrolled_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="enrollments")
    course = relationship("Course", backref="enrollments")
    order = relationship("Order", backref="enrollments")

class ContactSetting(Base):
    __tablename__ = "contact_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(255), default="Tòa nhà ACC, 123 Đường Điện Biên Phủ, Quận Bình Thạnh, TP. Hồ Chí Minh")
    hotline = Column(String(50), default="090 123 4567")
    email = Column(String(150), default="support@accacademy.vn")
    zalo = Column(String(150), default="https://zalo.me/0901234567")
    viber = Column(String(150), default="https://viber.click/0901234567")

