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
    Base.metadata.create_all(bind=engine)
    # Check if we should auto-seed (e.g. if categories table is empty)
    db = next(get_db())
    category_count = db.query(models.Category).count()
    db.close()
    if category_count == 0:
        print("Database is empty. Initiating automatic seeding...")
        seed_database()

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
