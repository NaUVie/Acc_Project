from fastapi import APIRouter
from .endpoints import auth, courses, cart, orders, blogs, contacts, testimonials, admin, upload, enrollments, engagement, marketing

api_router = APIRouter()

# Register sub-routers with prefixes and Swagger tags
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication & Referrals"])
api_router.include_router(courses.router, prefix="/courses", tags=["Course Catalog"])
api_router.include_router(cart.router, prefix="/cart", tags=["Shopping Cart"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders & Checkout"])
api_router.include_router(enrollments.router, prefix="/enrollments", tags=["Enrollments"])
api_router.include_router(blogs.router, prefix="/blogs", tags=["Blog Posts"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["Contact Forms"])
api_router.include_router(testimonials.router, prefix="/testimonials", tags=["Student Testimonials"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin Operations"])
api_router.include_router(upload.router, prefix="/upload", tags=["Media Uploads"])
api_router.include_router(engagement.router, prefix="/engagement", tags=["User Engagement"])
api_router.include_router(marketing.router, prefix="/marketing", tags=["Marketing & Promotions"])

