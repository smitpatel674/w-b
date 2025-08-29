from fastapi import APIRouter
from app.api.v1.endpoints import auth, courses, contact, testimonials

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(contact.router, prefix="/contact", tags=["contact"])
api_router.include_router(testimonials.router, prefix="/testimonials", tags=["testimonials"])
