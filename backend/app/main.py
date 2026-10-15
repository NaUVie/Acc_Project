import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from .database import engine, Base, get_db
from . import models
from .api.api import api_router
from .seed import seed_database

from contextlib import asynccontextmanager

def perform_startup_tasks():
    try:
        from sqlalchemy import inspect, text
        inspector = inspect(engine)
        if inspector.has_table("contacts"):
            columns = [c["name"] for c in inspector.get_columns("contacts")]
            if "phone" not in columns:
                with engine.begin() as conn:
                    conn.execute(text("DROP TABLE contacts"))
                print("Dropped old contacts table to migrate to new layout.")
    except Exception as e:
        print(f"Migration check error: {e}")

    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error creating DB tables on startup: {e}")

    # Ensure columns exist for upgraded schemas
    try:
        from sqlalchemy import inspect, text
        inspector = inspect(engine)
        with engine.begin() as conn:
            if inspector.has_table("users"):
                users_cols = [c["name"] for c in inspector.get_columns("users")]
                if "store_credit_balance" not in users_cols:
                    conn.execute(text("ALTER TABLE users ADD COLUMN store_credit_balance INT DEFAULT 0"))
                    print("Added column store_credit_balance to users table.")

            if inspector.has_table("contacts"):
                contacts_cols = [c["name"] for c in inspector.get_columns("contacts")]
                if "is_resolved" not in contacts_cols:
                    conn.execute(text("ALTER TABLE contacts ADD COLUMN is_resolved BOOLEAN DEFAULT FALSE"))
                    print("Added column is_resolved to contacts table.")
            
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
                    ("video_url", "VARCHAR(500) NULL")
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
    allow_origins=origins if os.getenv("ENVIRONMENT") == "production" else ["*"],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        db_status = "error"
        db_error = str(e)
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
