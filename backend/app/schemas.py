from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Category Schemas
class CategoryBase(BaseModel):
    slug: str
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
    handle: str
    price: int
    original_price: Optional[int] = None
    image: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    level: Optional[str] = None
    curriculum_data: Optional[str] = None

class CourseResponse(CourseBase):
    tags: List[CourseTagResponse] = []

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

class BlogPostResponse(BlogPostBase):
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

class UserResponse(UserBase):
    id: int
    referral_code: str
    role: str
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
class TestimonialResponse(BaseModel):
    id: int
    name: str
    role: str
    text: str
    image: Optional[str] = None
    video_url: Optional[str] = None

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
    handle: str
    price: int
    original_price: Optional[int] = None
    image: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    level: Optional[str] = None
    curriculum_data: Optional[str] = None

class CourseAdminUpdate(BaseModel):
    title: Optional[str] = None
    category_slug: Optional[str] = None
    handle: Optional[str] = None
    price: Optional[int] = None
    original_price: Optional[int] = None
    image: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    level: Optional[str] = None
    curriculum_data: Optional[str] = None

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

