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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins in local dev mode
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto-create tables and trigger seeding on startup
@app.on_event("startup")
def on_startup():
    # Schema migration check for contacts table before creating tables
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            # SQLite check table columns
            cursor = conn.execute(text("PRAGMA table_info(contacts)"))
            columns = [row[1] for row in cursor.fetchall()]
            if columns and "phone" not in columns:
                conn.execute(text("DROP TABLE contacts"))
                print("Dropped old contacts table to migrate to new layout.")
    except Exception as e:
        print(f"Migration check error: {e}")

    Base.metadata.create_all(bind=engine)
    
    # Ensure is_resolved column exists in contacts table
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            # Check contacts table
            result = conn.execute(text("SHOW COLUMNS FROM contacts LIKE 'is_resolved'")).fetchone()
            if not result:
                conn.execute(text("ALTER TABLE contacts ADD COLUMN is_resolved BOOLEAN DEFAULT FALSE"))
                print("Added column is_resolved to contacts table.")
            
            # Check courses table
            result_curr = conn.execute(text("SHOW COLUMNS FROM courses LIKE 'curriculum_data'")).fetchone()
            if not result_curr:
                conn.execute(text("ALTER TABLE courses ADD COLUMN curriculum_data TEXT NULL"))
                print("Added column curriculum_data to courses table.")
    except Exception as e:
        print(f"Error checking/adding migration columns: {e}")
    # Check if we should auto-seed (e.g. if categories table is empty)
    db = next(get_db())
    category_count = db.query(models.Category).count()
    if category_count == 0:
        print("Database is empty. Initiating automatic seeding...")
        seed_database()
    
    # Seed default contact settings if empty
    try:
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
    except Exception as e:
        print(f"Error seeding default contact settings: {e}")
    db.close()

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
