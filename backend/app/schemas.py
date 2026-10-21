from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Category Schemas
class CategoryBase(BaseModel):
    slug: str
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: str

class CategoryResponse(CategoryBase):
    class Config:
        from_attributes = True

# Tag Schemas
class CourseTagBase(BaseModel):
    tag: str

class CourseTagResponse(CourseTagBase):
    class Config:
        from_attributes = True

# Course Schemas
class CourseBase(BaseModel):
    id: int
    title: str
    category_slug: str
    program_id: Optional[int] = None
    handle: str
    price: int
    original_price: Optional[int] = None
    image: Optional[str] = None
    cover_image: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    level: Optional[str] = None
    default_commission_percent: Optional[int] = 10
    outcomes: Optional[str] = None
    requirements: Optional[str] = None
    custom_roadmap: Optional[str] = None
    lecturer_ids: Optional[str] = None

class CoursePublicResponse(CourseBase):
    tags: List[CourseTagResponse] = []

    class Config:
        from_attributes = True

class CourseStudyResponse(CourseBase):
    curriculum_data: Optional[str] = None
    tags: List[CourseTagResponse] = []

    class Config:
        from_attributes = True

class CourseResponse(CourseStudyResponse):
    pass

# Program Schemas
class ProgramCreate(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None
    course_ids: Optional[List[int]] = None

class ProgramUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    course_ids: Optional[List[int]] = None

class ProgramResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None
    created_at: datetime
    courses: List[CourseResponse] = []

    class Config:
        from_attributes = True

# Bundle Schemas
class BundleCreate(BaseModel):
    title: str
    handle: str
    description: Optional[str] = None
    price: int
    original_price: Optional[int] = None
    image: Optional[str] = None
    course_ids: List[int] = []
    gift_course_ids: List[int] = []

class BundleUpdate(BaseModel):
    title: Optional[str] = None
    handle: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    original_price: Optional[int] = None
    image: Optional[str] = None
    course_ids: Optional[List[int]] = None
    gift_course_ids: Optional[List[int]] = None

class BundleResponse(BaseModel):
    id: int
    title: str
    handle: str
    description: Optional[str] = None
    price: int
    original_price: Optional[int] = None
    image: Optional[str] = None
    created_at: datetime
    courses: List[CourseResponse] = []
    gift_courses: List[CourseResponse] = []

    class Config:
        from_attributes = True

# Blog Schemas
class BlogPostBase(BaseModel):
    id: int
    title: str
    handle: str
    category: str
    excerpt: Optional[str] = None
    image: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = None
    content: Optional[str] = None

class BlogPostCreate(BaseModel):
    title: str
    handle: str
    category: str
    excerpt: Optional[str] = None
    image: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = None
    content: Optional[str] = None

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    handle: Optional[str] = None
    category: Optional[str] = None
    excerpt: Optional[str] = None
    image: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = None
    content: Optional[str] = None

class BlogPostResponse(BlogPostBase):
    class Config:
        from_attributes = True

class BlogPostListResponse(BaseModel):
    id: int
    title: str
    handle: str
    category: str
    excerpt: Optional[str] = None
    image: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = None

    class Config:
        from_attributes = True

# Lecturer Major Schemas
class LecturerMajorBase(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    badge: Optional[str] = None
    position: Optional[int] = 0

class LecturerMajorCreate(LecturerMajorBase):
    pass

class LecturerMajorUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    badge: Optional[str] = None
    position: Optional[int] = None

class LecturerMajorResponse(LecturerMajorBase):
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Lecturer Schemas
class LecturerBase(BaseModel):
    id: str
    name: str
    title: str
    tagline: Optional[str] = None
    avatar: Optional[str] = None
    avatar_drive_link: Optional[str] = None
    drive_profile: Optional[str] = None
    bio_short: Optional[str] = None
    details_html: Optional[str] = None
    major_id: Optional[str] = None
    major_name: Optional[str] = None
    major_ids: Optional[str] = None
    position: Optional[int] = 0
    major_positions: Optional[dict] = None
    is_featured: Optional[bool] = False

class LecturerCreate(LecturerBase):
    pass

class LecturerUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    tagline: Optional[str] = None
    avatar: Optional[str] = None
    avatar_drive_link: Optional[str] = None
    drive_profile: Optional[str] = None
    bio_short: Optional[str] = None
    details_html: Optional[str] = None
    major_id: Optional[str] = None
    major_name: Optional[str] = None
    major_ids: Optional[str] = None
    position: Optional[int] = None
    major_positions: Optional[dict] = None
    is_featured: Optional[bool] = None

class LecturerResponse(LecturerBase):
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class LecturerReorderItem(BaseModel):
    id: str
    position: int

# Project Schemas
class ProjectBase(BaseModel):
    id: str
    category: str
    category_name: str
    title: str
    summary: Optional[str] = None
    image: Optional[str] = None
    date: Optional[str] = None
    client: Optional[str] = None
    drive_profile: Optional[str] = None
    content: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    category: Optional[str] = None
    category_name: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    image: Optional[str] = None
    date: Optional[str] = None
    client: Optional[str] = None
    drive_profile: Optional[str] = None
    content: Optional[str] = None

class ProjectResponse(ProjectBase):
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Contact Schemas
class ContactCreate(BaseModel):
    first_name: str
    middle_name: Optional[str] = ""
    last_name: str
    email: str
    phone: str
    course_handle: Optional[str] = ""
    message: str

class ContactResponse(BaseModel):
    id: int
    first_name: str
    middle_name: Optional[str]
    last_name: str
    email: str
    phone: str
    course_handle: Optional[str]
    message: str
    is_resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True

# User & Auth Schemas
class UserBase(BaseModel):
    fullname: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    referral_code_used: Optional[str] = None # The code of the friend who referred them

class UserUpdateProfile(BaseModel):
    fullname: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    referral_code: str
    role: str
    store_credit_balance: int = 0
    referred_by_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str # OAuth2 password form standard requires 'username' (which is the email)
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Cart Schemas
class CartItemCreate(BaseModel):
    course_id: int

class CartItemResponse(BaseModel):
    id: int
    course: CourseResponse
    created_at: datetime

    class Config:
        from_attributes = True

# Order Schemas
class OrderItemResponse(BaseModel):
    id: int
    course: CourseResponse
    price: int

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    total_price: int
    discount_applied: int
    status: str
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True

# Enrollment Schemas
class EnrollmentResponse(BaseModel):
    id: int
    course: CourseResponse
    enrolled_at: datetime

    class Config:
        from_attributes = True

class EnrollmentCheckResponse(BaseModel):
    enrolled: bool
    course_id: int

# Referral Schemas
class ReferralResponse(BaseModel):
    id: int
    referred_fullname: str
    commission_amount: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class ReferralSummary(BaseModel):
    total_referrals: int
    total_commission_earned: int
    referral_code: str
    referrals_list: List[ReferralResponse]

# Testimonial Schemas
class TestimonialCreate(BaseModel):
    name: str
    role: Optional[str] = None
    company: Optional[str] = None
    text: Optional[str] = None
    image: Optional[str] = None
    rating: Optional[int] = 5
    quote: Optional[str] = None
    course_name: Optional[str] = None
    testimonial_type: Optional[str] = "text"
    youtube_id: Optional[str] = None
    thumbnail: Optional[str] = None
    video_url: Optional[str] = None

class TestimonialUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    company: Optional[str] = None
    text: Optional[str] = None
    image: Optional[str] = None
    rating: Optional[int] = None
    quote: Optional[str] = None
    course_name: Optional[str] = None
    testimonial_type: Optional[str] = None
    youtube_id: Optional[str] = None
    thumbnail: Optional[str] = None
    video_url: Optional[str] = None

class TestimonialResponse(BaseModel):
    id: int
    name: str
    role: Optional[str] = None
    company: Optional[str] = None
    text: Optional[str] = None
    image: Optional[str] = None
    rating: Optional[int] = 5
    quote: Optional[str] = None
    course_name: Optional[str] = None
    testimonial_type: Optional[str] = "text"
    youtube_id: Optional[str] = None
    thumbnail: Optional[str] = None
    video_url: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Admin Schemas
class UserAdminCreate(BaseModel):
    fullname: str
    email: EmailStr
    password: str
    role: str = "student"
    referred_by_id: Optional[int] = None

class UserAdminUpdate(BaseModel):
    fullname: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    referred_by_id: Optional[int] = None

class UserAdminResponse(BaseModel):
    id: int
    fullname: str
    email: EmailStr
    role: str
    referral_code: str
    referred_by_id: Optional[int] = None
    store_credit_balance: int = 0
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class OrderAdminCreate(BaseModel):
    user_id: int
    course_ids: List[int]
    discount_applied: int = 0
    total_price: int
    status: str = "pending"

class OrderAdminUpdate(BaseModel):
    status: Optional[str] = None
    discount_applied: Optional[int] = None
    total_price: Optional[int] = None
    course_ids: Optional[List[int]] = None

class OrderAdminResponse(BaseModel):
    id: int
    user_id: int
    user_fullname: str
    user_email: str
    total_price: int
    discount_applied: int
    status: str
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True

class CourseAdminCreate(BaseModel):
    title: str
    category_slug: str
    program_id: Optional[int] = None
    handle: str
    price: int
    original_price: Optional[int] = None
    image: Optional[str] = None
    cover_image: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    level: Optional[str] = None
    curriculum_data: Optional[str] = None
    outcomes: Optional[str] = None
    requirements: Optional[str] = None
    custom_roadmap: Optional[str] = None
    lecturer_ids: Optional[str] = None

class CourseAdminUpdate(BaseModel):
    title: Optional[str] = None
    category_slug: Optional[str] = None
    program_id: Optional[int] = None
    handle: Optional[str] = None
    price: Optional[int] = None
    original_price: Optional[int] = None
    image: Optional[str] = None
    cover_image: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    level: Optional[str] = None
    curriculum_data: Optional[str] = None
    outcomes: Optional[str] = None
    requirements: Optional[str] = None
    custom_roadmap: Optional[str] = None
    lecturer_ids: Optional[str] = None

class ContactSettingUpdate(BaseModel):
    address: Optional[str] = None
    hotline: Optional[str] = None
    email: Optional[str] = None
    zalo: Optional[str] = None
    viber: Optional[str] = None

class ContactSettingResponse(BaseModel):
    id: int
    address: str
    hotline: str
    email: str
    zalo: str
    viber: str

    class Config:
        from_attributes = True

# Home Intro Settings Schemas
class HomeIntroSettingUpdate(BaseModel):
    title: Optional[str] = None
    desc1: Optional[str] = None
    desc2: Optional[str] = None
    counter_number: Optional[int] = None
    counter_label: Optional[str] = None
    video_url: Optional[str] = None
    poster_url: Optional[str] = None
    btn_label: Optional[str] = None

class HomeIntroSettingResponse(BaseModel):
    id: int
    title: str
    desc1: str
    desc2: str
    counter_number: int
    counter_label: str
    video_url: str
    poster_url: str
    btn_label: str

    class Config:
        from_attributes = True

# Banner Schemas
class BannerBase(BaseModel):
    title: str
    desktop_image: str
    mobile_image: Optional[str] = None
    link: Optional[str] = None
    is_external: Optional[bool] = False
    position: Optional[int] = 0
    is_active: Optional[bool] = True

class BannerCreate(BannerBase):
    pass

class BannerUpdate(BaseModel):
    title: Optional[str] = None
    desktop_image: Optional[str] = None
    mobile_image: Optional[str] = None
    link: Optional[str] = None
    is_external: Optional[bool] = None
    position: Optional[int] = None
    is_active: Optional[bool] = None

class BannerResponse(BannerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Progress Schemas
class CourseProgressUpdate(BaseModel):
    completed_lessons: List[str] = []

class CourseProgressResponse(BaseModel):
    course_id: int
    completed_lessons: List[str] = []

# Review Schemas
class CourseReviewCreate(BaseModel):
    rating: int # 1 to 5
    comment: str

class CourseReviewResponse(BaseModel):
    id: int
    course_id: int
    user_id: int
    user_fullname: str
    rating: int
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True

# Lesson Note Schemas
class LessonNoteCreate(BaseModel):
    course_handle: str
    lesson_id: str
    timestamp_seconds: int = 0
    note_text: str

class LessonNoteResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    lesson_id: str
    timestamp_seconds: int
    note_text: str
    created_at: datetime

    class Config:
        from_attributes = True

# Wishlist Schemas
class WishlistResponse(BaseModel):
    id: int
    course: CourseResponse
    created_at: datetime

    class Config:
        from_attributes = True

# Coupon Schemas
class CouponCreate(BaseModel):
    code: str
    discount_type: str = "percent" # "percent" or "fixed"
    discount_value: int
    min_order_value: Optional[int] = 0
    max_discount_amount: Optional[int] = 0
    usage_limit: Optional[int] = 0
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    is_active: Optional[bool] = True

class CouponResponse(BaseModel):
    id: int
    code: str
    discount_type: str
    discount_value: int
    min_order_value: int
    max_discount_amount: int
    usage_limit: int
    times_used: int
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class CouponApplyRequest(BaseModel):
    code: str
    cart_total: int

class CouponApplyResponse(BaseModel):
    valid: bool
    code: str
    discount_amount: int
    message: str

# Custom Commission Schemas
class UserCourseCommissionCreate(BaseModel):
    user_id: int
    course_id: int
    commission_percent: int

class UserCourseCommissionResponse(BaseModel):
    id: int
    user_id: int
    user_fullname: str
    course_id: int
    course_title: str
    commission_percent: int
    created_at: datetime

    class Config:
        from_attributes = True

# Project Review Schemas
class ProjectReviewCreate(BaseModel):
    author_name: str
    author_email: Optional[str] = None
    rating: int = 5
    comment: str

class ProjectReviewUpdate(BaseModel):
    is_approved: Optional[bool] = None
    rating: Optional[int] = None
    comment: Optional[str] = None

class ProjectReviewResponse(BaseModel):
    id: int
    project_id: str
    author_name: str
    rating: int
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True

class ProjectReviewAdminResponse(BaseModel):
    id: int
    project_id: str
    user_id: Optional[int] = None
    author_name: str
    author_email: Optional[str] = None
    rating: int
    comment: str
    is_approved: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Partner Schemas
class PartnerBase(BaseModel):
    name: str
    src: str
    link: Optional[str] = None
    position: Optional[int] = 0
    row_type: Optional[str] = "marquee" # "top_fixed", "marquee", "bottom_fixed"
    is_active: Optional[bool] = True

class PartnerCreate(PartnerBase):
    pass

class PartnerUpdate(BaseModel):
    name: Optional[str] = None
    src: Optional[str] = None
    link: Optional[str] = None
    position: Optional[int] = None
    row_type: Optional[str] = None
    is_active: Optional[bool] = None


class PartnerResponse(PartnerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

