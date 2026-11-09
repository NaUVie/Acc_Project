import os
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from .database import engine, Base, get_db
from . import models, crud
from .api.api import api_router
from .seed import seed_database

from contextlib import asynccontextmanager

def perform_startup_tasks():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error creating DB tables on startup: {e}")

    # Ensure columns exist for upgraded schemas (safe non-destructive migrations, no DROP TABLE)
    try:
        from sqlalchemy import inspect, text
        inspector = inspect(engine)
        with engine.begin() as conn:
            if inspector.has_table("users"):
                users_cols = [c["name"] for c in inspector.get_columns("users")]
                if "store_credit_balance" not in users_cols:
                    conn.execute(text("ALTER TABLE users ADD COLUMN store_credit_balance INT DEFAULT 0"))
                    print("Added column store_credit_balance to users table.")
                if "phone" not in users_cols:
                    conn.execute(text("ALTER TABLE users ADD COLUMN phone VARCHAR(50) NULL"))
                    print("Added column phone to users table.")

            if inspector.has_table("contacts"):
                contacts_cols = [c["name"] for c in inspector.get_columns("contacts")]
                contact_migrations = [
                    ("first_name", "VARCHAR(100) DEFAULT ''"),
                    ("middle_name", "VARCHAR(100) NULL"),
                    ("last_name", "VARCHAR(100) DEFAULT ''"),
                    ("phone", "VARCHAR(50) DEFAULT ''"),
                    ("course_handle", "VARCHAR(255) NULL"),
                    ("is_resolved", "BOOLEAN DEFAULT FALSE"),
                ]
                for col_name, col_def in contact_migrations:
                    if col_name not in contacts_cols:
                        conn.execute(text(f"ALTER TABLE contacts ADD COLUMN {col_name} {col_def}"))
                        print(f"Added column {col_name} to contacts table.")
            
            if inspector.has_table("courses"):
                courses_cols = [c["name"] for c in inspector.get_columns("courses")]
                if "curriculum_data" not in courses_cols:
                    conn.execute(text("ALTER TABLE courses ADD COLUMN curriculum_data TEXT NULL"))
                    print("Added column curriculum_data to courses table.")
                if "program_id" not in courses_cols:
                    conn.execute(text("ALTER TABLE courses ADD COLUMN program_id INT NULL"))
                    print("Added column program_id to courses table.")
                if "default_commission_percent" not in courses_cols:
                    conn.execute(text("ALTER TABLE courses ADD COLUMN default_commission_percent INT DEFAULT 10"))
                    print("Added column default_commission_percent to courses table.")
                if "outcomes" not in courses_cols:
                    conn.execute(text("ALTER TABLE courses ADD COLUMN outcomes TEXT NULL"))
                    print("Added column outcomes to courses table.")
                if "requirements" not in courses_cols:
                    conn.execute(text("ALTER TABLE courses ADD COLUMN requirements TEXT NULL"))
                    print("Added column requirements to courses table.")
                if "custom_roadmap" not in courses_cols:
                    conn.execute(text("ALTER TABLE courses ADD COLUMN custom_roadmap TEXT NULL"))
                    print("Added column custom_roadmap to courses table.")
                if "lecturer_ids" not in courses_cols:
                    conn.execute(text("ALTER TABLE courses ADD COLUMN lecturer_ids TEXT NULL"))
                    print("Added column lecturer_ids to courses table.")
                if "cover_image" not in courses_cols:
                    conn.execute(text("ALTER TABLE courses ADD COLUMN cover_image VARCHAR(255) NULL"))
                    print("Added column cover_image to courses table.")
                if "status" not in courses_cols:
                    conn.execute(text("ALTER TABLE courses ADD COLUMN status VARCHAR(50) DEFAULT 'ongoing'"))
                    print("Added column status to courses table.")
                if "materials_link" not in courses_cols:
                    conn.execute(text("ALTER TABLE courses ADD COLUMN materials_link VARCHAR(500) NULL"))
                    print("Added column materials_link to courses table.")
                if "photos_link" not in courses_cols:
                    conn.execute(text("ALTER TABLE courses ADD COLUMN photos_link VARCHAR(500) NULL"))
                    print("Added column photos_link to courses table.")
                if "youtube_link" not in courses_cols:
                    conn.execute(text("ALTER TABLE courses ADD COLUMN youtube_link VARCHAR(500) NULL"))
                    print("Added column youtube_link to courses table.")
            
            if inspector.has_table("orders"):
                orders_cols = [c["name"] for c in inspector.get_columns("orders")]
                if "store_credit_used" not in orders_cols:
                    conn.execute(text("ALTER TABLE orders ADD COLUMN store_credit_used INT DEFAULT 0"))
                    print("Added column store_credit_used to orders table.")
                if "coupon_code" not in orders_cols:
                    conn.execute(text("ALTER TABLE orders ADD COLUMN coupon_code VARCHAR(50) NULL"))
                    print("Added column coupon_code to orders table.")

            if inspector.has_table("enrollments"):
                enr_cols = [c["name"] for c in inspector.get_columns("enrollments")]
                if "progress_data" not in enr_cols:
                    conn.execute(text("ALTER TABLE enrollments ADD COLUMN progress_data TEXT NULL"))
                    print("Added column progress_data to enrollments table.")

            if inspector.has_table("testimonials"):
                test_cols = [c["name"] for c in inspector.get_columns("testimonials")]
                testimonial_migrations = [
                    ("company", "VARCHAR(150) NULL"),
                    ("rating", "INT DEFAULT 5"),
                    ("quote", "TEXT NULL"),
                    ("course_name", "VARCHAR(255) NULL"),
                    ("testimonial_type", "VARCHAR(50) DEFAULT 'text'"),
                    ("youtube_id", "VARCHAR(100) NULL"),
                    ("thumbnail", "VARCHAR(500) NULL"),
                    ("video_url", "VARCHAR(500) NULL"),
                    ("course_id", "BIGINT NULL"),
                    ("is_approved", "BOOLEAN DEFAULT TRUE")
                ]
                for col_name, col_def in testimonial_migrations:
                    if col_name not in test_cols:
                        try:
                            conn.execute(text(f"ALTER TABLE testimonials ADD COLUMN {col_name} {col_def}"))
                            print(f"Added column {col_name} to testimonials table.")
                        except Exception as ex:
                            print(f"Migration column error for testimonials.{col_name}: {ex}")
            if inspector.has_table("lecturers"):
                lec_cols = [c["name"] for c in inspector.get_columns("lecturers")]
                if "position" not in lec_cols:
                    conn.execute(text("ALTER TABLE lecturers ADD COLUMN position INT DEFAULT 0"))
                    print("Added column position to lecturers table.")
                if "is_featured" not in lec_cols:
                    conn.execute(text("ALTER TABLE lecturers ADD COLUMN is_featured BOOLEAN DEFAULT FALSE"))
                    print("Added column is_featured to lecturers table.")
                if "major_id" not in lec_cols:
                    conn.execute(text("ALTER TABLE lecturers ADD COLUMN major_id VARCHAR(100) NULL"))
                    print("Added column major_id to lecturers table.")
                if "major_name" not in lec_cols:
                    conn.execute(text("ALTER TABLE lecturers ADD COLUMN major_name VARCHAR(150) NULL"))
                    print("Added column major_name to lecturers table.")
                if "major_ids" not in lec_cols:
                    conn.execute(text("ALTER TABLE lecturers ADD COLUMN major_ids TEXT NULL"))
                    print("Added column major_ids to lecturers table.")
            if inspector.has_table("partners"):
                part_cols = [c["name"] for c in inspector.get_columns("partners")]
                if "row_type" not in part_cols:
                    conn.execute(text("ALTER TABLE partners ADD COLUMN row_type VARCHAR(50) DEFAULT 'marquee'"))
                    print("Added column row_type to partners table.")

            if inspector.has_table("blog_posts"):
                bp_cols = [c["name"] for c in inspector.get_columns("blog_posts")]
                if "course_id" not in bp_cols:
                    try:
                        conn.execute(text("ALTER TABLE blog_posts ADD COLUMN course_id BIGINT NULL"))
                        print("Added column course_id to blog_posts table.")
                    except Exception as ex:
                        print(f"Error adding course_id to blog_posts: {ex}")

            if inspector.has_table("home_intro_settings"):
                intro_cols = [c["name"] for c in inspector.get_columns("home_intro_settings")]
                intro_migrations = [
                    ("bento_title", "VARCHAR(255) DEFAULT 'Năng lực cốt lõi của ACC Academy'"),
                    ("bento_line1", "TEXT NULL"),
                    ("bento_line2", "TEXT NULL"),
                    ("bento_strong", "TEXT NULL"),
                    ("bento_line3", "TEXT NULL"),
                ]
                for col_name, col_def in intro_migrations:
                    if col_name not in intro_cols:
                        try:
                            conn.execute(text(f"ALTER TABLE home_intro_settings ADD COLUMN {col_name} {col_def}"))
                            print(f"Added column {col_name} to home_intro_settings table.")
                        except Exception as ex:
                            print(f"Migration column error for home_intro_settings.{col_name}: {ex}")
    except Exception as e:
        print(f"Error checking/adding migration columns: {e}")

    # Single DB session for contact settings
    try:
        db = next(get_db())
        try:
            # Only seed default settings if needed
            setting_count = db.query(models.ContactSetting).count()
            if setting_count == 0:
                db_setting = models.ContactSetting(
                    address="156 Nam Kỳ Khởi Nghĩa, Quận 1, TP. Hồ Chí Minh",
                    hotline="0938 566 700",
                    email="info@acc-edu.vn",
                    zalo="https://zalo.me/0938566700",
                    viber="https://viber.click/0938566700"
                )
                db.add(db_setting)
                db.commit()
                print("Seeded default contact settings.")

            # Seed default blog categories if empty
            blog_cat_count = db.query(models.BlogCategory).count()
            if blog_cat_count == 0:
                existing_cats = db.query(models.BlogPost.category).distinct().all()
                cat_names = set([c[0] for c in existing_cats if c[0]])
                default_cats = ["AI 2026", "AI Automation", "Công cụ AI", "Làm việc hiệu suất", "Lãnh đạo & Quản lý"]
                for dc in default_cats:
                    cat_names.add(dc)
                
                for name in sorted(cat_names):
                    slug = crud.slugify(name)
                    db_bcat = models.BlogCategory(name=name, slug=slug)
                    db.add(db_bcat)
                db.commit()
                print(f"Seeded {len(cat_names)} initial blog categories.")

            # Seed default board members if empty
            board_count = db.query(models.BoardMember).count()
            if board_count == 0:
                import json
                initial_board = [
                    {
                        "name": "Ông Nguyễn Tiến Điệp",
                        "main_role": "Chủ tịch HĐQT Công ty CP Kết Nối Tri Thức ACC",
                        "role_group": "executive",
                        "avatar": "/images/VeChungToi/TienDiep.webp",
                        "bio_list": json.dumps([
                            "CEO Sadaco Tas",
                            "Chủ tịch HĐQT CTY CP Tập đoàn Sài Gòn Tiến Đoàn",
                            "Chủ tịch Alumni Andrews Việt Nam",
                            "Thạc sĩ QTKD Đại học Andrews (Hoa Kỳ)"
                        ], ensure_ascii=False),
                        "position": 1,
                        "is_active": True
                    },
                    {
                        "name": "Ông Ngô Trí Thủy",
                        "main_role": "Tổng Giám đốc Công ty CP Kết Nối Tri Thức ACC",
                        "role_group": "executive",
                        "avatar": "/images/VeChungToi/NgoTriThuy.webp",
                        "bio_list": json.dumps([
                            "Thành viên sáng lập - Phó Chủ tịch HĐQT Imap Logistics",
                            "Thành viên sáng lập – Thành viên HĐQT Icom Trading",
                            "Phó Chủ tịch Hội Doanh nhân Trẻ TPHCM (Chi Hội Chợ Lớn)",
                            "Nguyên Giám đốc Marketing và Phát triển Sản phẩm các Ngân hàng"
                        ], ensure_ascii=False),
                        "position": 2,
                        "is_active": True
                    },
                    {
                        "name": "Bà Nguyễn Thị Thu Hoà",
                        "main_role": "Thành viên Hội Đồng Quản Trị ACC",
                        "role_group": "executive",
                        "avatar": "/images/VeChungToi/ThuHoa.webp",
                        "bio_list": json.dumps([
                            "Tổng Giám Đốc của ADP Group",
                            "Nguyên Giám Đốc Marketing của Tập Đội BĐS Khang Điền",
                            "Quyền Giám Đốc Nhãn Hàng Tập Đoàn Cà phê Trung Nguyên"
                        ], ensure_ascii=False),
                        "position": 3,
                        "is_active": True
                    },
                    {
                        "name": "Ông Lê Nguyễn Ngọc Sơn",
                        "main_role": "Thành viên HĐQT Công ty CP Kết nối Tri thức ACC",
                        "role_group": "executive",
                        "avatar": "/images/VeChungToi/Ngocson.webp",
                        "bio_list": json.dumps([
                            "Giám Đốc Andrews Alumni Việt Nam",
                            "Phó Giám Đốc Phát Triển Đại Học Andrews Hoa Kỳ tại Việt Nam"
                        ], ensure_ascii=False),
                        "position": 4,
                        "is_active": True
                    },
                    {
                        "name": "TS. Nguyễn Tấn Bình",
                        "main_role": "Cố vấn Cao cấp Công ty CP Kết nối Tri thức ACC",
                        "role_group": "advisor",
                        "avatar": "/images/VeChungToi/ThayBinh.webp",
                        "bio_list": json.dumps([
                            "Viện trưởng Viện nghiên cứu Khoa học Lãnh đạo & Quản trị Doanh nghiệp – Leadman",
                            "Giảng viên cao cấp Andrews University Hoa Kỳ tại Việt Nam",
                            "Giảng viên thỉnh giảng chương trình Fulbright",
                            "Giảng viên cao cấp, tác giả nhiều sách về Tài chính - Kế toán"
                        ], ensure_ascii=False),
                        "position": 5,
                        "is_active": True
                    },
                    {
                        "name": "Bà Nguyễn Thị Kim Anh",
                        "main_role": "Cố vấn Cao cấp Công ty CP Kết nối Tri thức ACC",
                        "role_group": "advisor",
                        "avatar": "/images/VeChungToi/KimAnh.webp",
                        "bio_list": json.dumps([
                            "Thạc sĩ Quản trị Kinh doanh, Andrews University, Hoa Kỳ",
                            "Chủ tịch HĐQT Hệ thống Trường Việt Anh",
                            "Quản lý chuỗi hệ thống 10 trường từ hệ Mầm non đến Trung học Phổ thông chuẩn quốc tế"
                        ], ensure_ascii=False),
                        "position": 6,
                        "is_active": True
                    },
                    {
                        "name": "Bà Nguyễn Thị Mỹ Dung",
                        "main_role": "Co-Founder Công ty CP Kết nối Tri thức ACC",
                        "role_group": "executive",
                        "avatar": "/images/VeChungToi/MYDUNG.webp",
                        "bio_list": json.dumps([
                            "Nguyên Giám đốc chi nhánh Techcombank",
                            "Thạc sĩ QTKD trường Đại học Andrews (ĐH Quốc tế, ĐHQG Tp.HCM)",
                            "Giảng viên Đại học"
                        ], ensure_ascii=False),
                        "position": 7,
                        "is_active": True
                    },
                    {
                        "name": "Bà Ngô Vũ Ngọc Thảo",
                        "main_role": "Co-Founder Công ty CP Kết nối Tri thức ACC",
                        "role_group": "executive",
                        "avatar": "/images/VeChungToi/NgocThao.webp",
                        "bio_list": json.dumps([
                            "Trưởng phòng Cao cấp Tập đoàn L’Oreal Việt Nam",
                            "Trưởng ban Học Thuật – Trường ĐH Andrews (ĐH Quốc tế - ĐHQG Tp.HCM)",
                            "Giảng viên Đại học & Thạc sĩ QTKD Đại học Andrews"
                        ], ensure_ascii=False),
                        "position": 8,
                        "is_active": True
                    }
                ]
                for mb in initial_board:
                    db.add(models.BoardMember(**mb))
                db.commit()
                print(f"Seeded {len(initial_board)} initial board members.")

            # Seed default admission posts if empty or sync default subtitles
            crud.seed_default_admission_posts(db)

            # Clean up any expired pending orders on startup
            crud.cleanup_expired_pending_orders(db, timeout_minutes=30)
        finally:
            db.close()
    except Exception as e:
        print(f"Error during startup DB check/seed: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    perform_startup_tasks()
    yield

# Create FastAPI app
app = FastAPI(
    title="ACC Academy API",
    description="Backend API for ACC Academy course catalog, blogs, contact lead capture, cart checkout, and referral rewards.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
is_production = os.getenv("ENVIRONMENT", "development").lower() == "production"
cors_origins_raw = os.getenv("CORS_ORIGINS", "")
custom_origins = [o.strip() for o in cors_origins_raw.split(",") if o.strip()]
default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "https://acc-academy-demo.vercel.app"
]
origins = list(set(default_origins + custom_origins))

# Compress large JSON responses (blog/course lists carry long HTML content)
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)}
    )

# Register the combined modular API router with a global prefix
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to ACC Academy API!",
        "docs_url": "/docs",
        "status": "active"
    }

import time
from sqlalchemy import text
from fastapi import Depends

@app.get("/health")
@app.get("/api/health")
def health_check(db = Depends(get_db)):
    start_time = time.perf_counter()
    db_status = "ok"
    db_error = None
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        print(f"Healthcheck DB error: {e}")
        db_status = "error"
        db_error = "Database connection error"
    db_latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
    
    return {
        "status": "ok" if db_status == "ok" else "degraded",
        "backend": "online",
        "database": {
            "status": db_status,
            "latency_ms": f"{db_latency_ms} ms",
            "error": db_error
        }
    }

if __name__ == "__main__":
    import uvicorn
    from .config import PORT, HOST
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
