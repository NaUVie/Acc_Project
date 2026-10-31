from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey, Text, DateTime, Boolean, Table, JSON
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
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
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

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
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

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
    cover_image = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    duration = Column(String(50), nullable=True)
    level = Column(String(50), nullable=True)
    curriculum_data = Column(Text, nullable=True)
    default_commission_percent = Column(Integer, default=10)
    outcomes = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    custom_roadmap = Column(Text, nullable=True)
    lecturer_ids = Column(Text, nullable=True)

    category = relationship("Category", back_populates="courses")
    program = relationship("Program", back_populates="courses")
    tags = relationship("CourseTag", back_populates="course", cascade="all, delete-orphan", passive_deletes=True)
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan", passive_deletes=True)
    reviews = relationship("CourseReview", back_populates="course", cascade="all, delete-orphan", passive_deletes=True)
    notes = relationship("LessonNote", back_populates="course", cascade="all, delete-orphan", passive_deletes=True)
    wishlists = relationship("Wishlist", back_populates="course", cascade="all, delete-orphan", passive_deletes=True)
    custom_commissions = relationship("UserCourseCommission", back_populates="course", cascade="all, delete-orphan", passive_deletes=True)
    cart_items = relationship("CartItem", back_populates="course", cascade="all, delete-orphan", passive_deletes=True)

class CourseTag(Base):
    __tablename__ = "course_tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(BigInteger, ForeignKey("courses.id"), nullable=False)
    tag = Column(String(100), nullable=False)

    course = relationship("Course", back_populates="tags")

class BlogCategory(Base):
    __tablename__ = "blog_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)

class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    handle = Column(String(100), nullable=False, unique=True, index=True)
    category = Column(String(100), nullable=False)
    excerpt = Column(Text().with_variant(LONGTEXT, "mysql"), nullable=True)
    image = Column(String(1000), nullable=True)
    date = Column(String(50), nullable=True)
    link = Column(String(255), nullable=True)
    content = Column(Text().with_variant(LONGTEXT, "mysql"), nullable=True)

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
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    referral_code = Column(String(50), unique=True, index=True, nullable=False)
    referred_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    role = Column(String(50), default="student") # student, admin
    store_credit_balance = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    orders = relationship("Order", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Integer, nullable=False)
    discount_applied = Column(Integer, default=0)
    status = Column(String(50), default="pending") # pending, paid, cancelled
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

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
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(BigInteger, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="cart_items")
    course = relationship("Course", back_populates="cart_items")

class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    referred_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    commission_amount = Column(Integer, default=0)
    status = Column(String(50), default="pending") # pending, completed (paid out)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    referrer = relationship("User", foreign_keys=[referrer_id])
    referred = relationship("User", foreign_keys=[referred_id])

class Testimonial(Base):
    __tablename__ = "testimonials"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    role = Column(String(150), nullable=True)
    company = Column(String(150), nullable=True)
    text = Column(Text, nullable=True)
    image = Column(String(500), nullable=True)
    rating = Column(Integer, default=5)
    quote = Column(Text, nullable=True)
    course_name = Column(String(255), nullable=True)
    testimonial_type = Column(String(50), default="text") # "text", "photo", "video"
    youtube_id = Column(String(100), nullable=True)
    thumbnail = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class LecturerMajor(Base):
    __tablename__ = "lecturer_majors"

    id = Column(String(100), primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)
    badge = Column(String(150), nullable=True)
    position = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    lecturers = relationship("Lecturer", back_populates="major")

class Lecturer(Base):
    __tablename__ = "lecturers"

    id = Column(String(100), primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    title = Column(String(255), nullable=False)
    tagline = Column(Text, nullable=True)
    avatar = Column(String(500), nullable=True)
    avatar_drive_link = Column(String(500), nullable=True)
    drive_profile = Column(String(500), nullable=True)
    bio_short = Column(Text().with_variant(LONGTEXT, "mysql"), nullable=True)
    details_html = Column(Text().with_variant(LONGTEXT, "mysql"), nullable=True)
    major_id = Column(String(100), ForeignKey("lecturer_majors.id", ondelete="SET NULL"), nullable=True)
    major_name = Column(String(150), nullable=True)
    major_ids = Column(Text, nullable=True)
    position = Column(Integer, default=0)
    major_positions = Column(JSON, nullable=True)
    is_featured = Column(Boolean, default=False)
    show_detail_btn = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    major = relationship("LecturerMajor", back_populates="lecturers")

class Project(Base):
    __tablename__ = "projects"

    id = Column(String(100), primary_key=True, index=True)
    category = Column(String(100), nullable=False)
    category_name = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=True)
    image = Column(String(500), nullable=True)
    date = Column(String(100), nullable=True)
    client = Column(String(150), nullable=True)
    drive_profile = Column(String(500), nullable=True)
    content = Column(Text().with_variant(LONGTEXT, "mysql"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    reviews = relationship("ProjectReview", back_populates="project", cascade="all, delete-orphan")


class ProjectReview(Base):
    __tablename__ = "project_reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String(100), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    author_name = Column(String(150), nullable=False)
    author_email = Column(String(150), nullable=True)
    rating = Column(Integer, default=5) # 1 to 5
    comment = Column(Text, nullable=False)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    project = relationship("Project", back_populates="reviews")
    user = relationship("User", backref="project_reviews")

class Enrollment(Base):
    """Tracks which user has access to which course (after payment)."""
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(BigInteger, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="SET NULL"), nullable=True)
    enrolled_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    progress_data = Column(Text, nullable=True) # JSON list of completed lesson IDs

    user = relationship("User", backref="enrollments")
    course = relationship("Course", back_populates="enrollments")
    order = relationship("Order", backref="enrollments")

class ContactSetting(Base):
    __tablename__ = "contact_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(255), default="Tòa nhà ACC, 123 Đường Điện Biên Phủ, Quận Bình Thạnh, TP. Hồ Chí Minh")
    hotline = Column(String(50), default="090 123 4567")
    email = Column(String(150), default="support@accacademy.vn")
    zalo = Column(String(150), default="https://zalo.me/0901234567")
    viber = Column(String(150), default="https://viber.click/0901234567")

class Banner(Base):
    __tablename__ = "banners"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    desktop_image = Column(String(500), nullable=False)
    mobile_image = Column(String(500), nullable=True)
    link = Column(String(500), nullable=True)
    is_external = Column(Boolean, default=False)
    position = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class HomeIntroSetting(Base):
    __tablename__ = "home_intro_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), default="Kiến tạo năng lực – Dẫn dắt chuyển đổi bền vững")
    desc1 = Column(Text, default="ACC Academy đồng hành cùng cá nhân, doanh nghiệp và tổ chức trong hành trình nâng cao năng lực, ứng dụng AI và chuyển đổi số vào thực tiễn.")
    desc2 = Column(Text, default="Chúng tôi kết hợp Đào tạo – Tư vấn – Công nghệ – Chiến lược, giúp đội ngũ không chỉ hiểu công nghệ mà còn biết cách ứng dụng hiệu quả vào công việc, tối ưu quy trình và tạo ra giá trị tăng trưởng bền vững.")
    counter_number = Column(Integer, default=500)
    counter_label = Column(String(255), default="CHƯƠNG TRÌNH & DỰ ÁN ĐÀO TẠO – TƯ VẤN ĐÃ TRIỂN KHAI")
    video_url = Column(String(500), default="/videos/intro.mp4")
    poster_url = Column(String(500), default="/images/CoE-Thumb.png")
    btn_label = Column(String(255), default="XEM VIDEO GIỚI THIỆU ACC ACADEMY")


class CourseReview(Base):
    __tablename__ = "course_reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(BigInteger, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False) # 1 to 5
    comment = Column(Text, nullable=False)
    is_approved = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="reviews")
    course = relationship("Course", back_populates="reviews")

class LessonNote(Base):
    __tablename__ = "lesson_notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(BigInteger, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(String(100), nullable=False)
    timestamp_seconds = Column(Integer, default=0)
    note_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="notes")
    course = relationship("Course", back_populates="notes")

class Wishlist(Base):
    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(BigInteger, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="wishlists")
    course = relationship("Course", back_populates="wishlists")

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    discount_type = Column(String(20), default="percent") # "percent" or "fixed"
    discount_value = Column(Integer, nullable=False)
    min_order_value = Column(Integer, default=0)
    max_discount_amount = Column(Integer, default=0) # 0 means no cap
    usage_limit = Column(Integer, default=0) # 0 means unlimited
    times_used = Column(Integer, default=0)
    valid_from = Column(DateTime, nullable=True)
    valid_to = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class UserCourseCommission(Base):
    """Custom commission rate per user and course (overrides Course.default_commission_percent)."""
    __tablename__ = "user_course_commissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(BigInteger, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    commission_percent = Column(Integer, nullable=False) # e.g. 15 for 15%
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="custom_commissions")
    course = relationship("Course", back_populates="custom_commissions")

class Partner(Base):
    """Business Partner Logos displayed on Home page"""
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    src = Column(String(500), nullable=False)
    link = Column(String(500), nullable=True)
    position = Column(Integer, default=0)
    row_type = Column(String(50), default="marquee") # "top_fixed", "marquee", "bottom_fixed"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))





