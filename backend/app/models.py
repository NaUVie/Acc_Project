from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Category(Base):
    __tablename__ = "categories"

    slug = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    courses = relationship("Course", back_populates="category")

class Course(Base):
    __tablename__ = "courses"

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category_slug = Column(String(50), ForeignKey("categories.slug"), nullable=False)
    handle = Column(String(100), nullable=False, unique=True, index=True)
    price = Column(Integer, nullable=False)
    original_price = Column(Integer, nullable=True)
    image = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    duration = Column(String(50), nullable=True)
    level = Column(String(50), nullable=True)

    category = relationship("Category", back_populates="courses")
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
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    course_handle = Column(String(100), nullable=True)
    message = Column(Text, nullable=False)
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
