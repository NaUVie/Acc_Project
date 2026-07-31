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
    name: str
    email: str
    course_handle: Optional[str] = ""
    message: str

class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    course_handle: Optional[str]
    message: str
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
