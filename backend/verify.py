import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app import models

db = SessionLocal()
try:
    categories = db.query(models.Category).all()
    print(f"Categories count: {len(categories)}")
    for cat in categories:
        c_count = db.query(models.Course).filter(models.Course.category_slug == cat.slug).count()
        print(f" - [{cat.slug}] {cat.name}: {c_count} courses")

finally:
    db.close()
