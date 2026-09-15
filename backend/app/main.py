import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
            
            if inspector.has_table("enrollments"):
                enr_cols = [c["name"] for c in inspector.get_columns("enrollments")]
                if "progress_data" not in enr_cols:
                    conn.execute(text("ALTER TABLE enrollments ADD COLUMN progress_data TEXT NULL"))
                    print("Added column progress_data to enrollments table.")
    except Exception as e:
        print(f"Error checking/adding migration columns: {e}")

    # Single DB session for initial seed and contact settings
    try:
        db = next(get_db())
        try:
            course_count = db.query(models.Course).count()
            if course_count == 0:
                print("Database is empty. Running initial seed...")
                seed_database()
            
            setting_count = db.query(models.ContactSetting).count()
            if setting_count == 0:
                db_setting = models.ContactSetting(
                    address="Tòa nhà ACC, 123 Đường Điện Biên Phủ, Quận Bình Thạnh, TP. Hồ Chí Minh",
                    hotline="090 123 4567",
                    email="support@accacademy.vn",
                    zalo="https://zalo.me/0901234567",
                    viber="https://viber.click/0901234567"
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

if __name__ == "__main__":
    import uvicorn
    from .config import PORT, HOST
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
