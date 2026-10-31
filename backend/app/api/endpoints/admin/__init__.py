from fastapi import APIRouter, Depends
from .... import auth
from . import users, orders, reports, contacts, courses, marketing, lecturers, projects, blogs

router = APIRouter(dependencies=[Depends(auth.get_current_admin)])

router.include_router(users.router)
router.include_router(orders.router)
router.include_router(reports.router)
router.include_router(contacts.router)
router.include_router(courses.router)
router.include_router(marketing.router)
router.include_router(lecturers.router)
router.include_router(projects.router)
router.include_router(blogs.router)

