import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, get_db
from . import models
from .api.api import api_router
from .seed import seed_database

# Create FastAPI app
app = FastAPI(
    title="ACC Academy API",
    description="Backend API for ACC Academy course catalog, blogs, contact lead capture, cart checkout, and referral rewards.",
    version="1.0.0"
)

# CORS configuration
cors_origins_raw = os.getenv("CORS_ORIGINS", "*")
origins = [o.strip() for o in cors_origins_raw.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto-create tables and trigger seeding on startup
@app.on_event("startup")
def on_startup():
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

    # Ensure is_resolved & curriculum_data columns exist
    try:
        from sqlalchemy import inspect, text
        inspector = inspect(engine)
        with engine.begin() as conn:
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
    except Exception as e:
        print(f"Error checking/adding migration columns: {e}")

    # Run seed_database only if database is brand new / empty
    try:
        db = next(get_db())
        course_count = db.query(models.Course).count()
        if course_count == 0:
            print("Database is empty. Running initial seed...")
            seed_database()
        db.close()
    except Exception as e:
        print(f"Error during startup seed check: {e}")

    # Seed default contact settings if empty
    try:
        db = next(get_db())
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
        db.close()
    except Exception as e:
        print(f"Error seeding default contact settings: {e}")

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
