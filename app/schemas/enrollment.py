from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models.enrollment import EnrollmentStatus


class EnrollmentFormCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    city: str
    course_title: str
    course_price: str


class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int
    payment_amount: float
    payment_method: Optional[str] = None


class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    student_name: str
    student_email: str
    student_phone: str
    student_city: str
    course_title: str
    course_price: str
    status: EnrollmentStatus
    enrolled_at: datetime
    payment_amount: float
    payment_method: Optional[str]
    
    class Config:
        from_attributes = True


class EnrollmentFormResponse(BaseModel):
    message: str
    enrollment_id: Optional[int]
    user_created: bool
    
    class Config:
        from_attributes = True