from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class TestimonialBase(BaseModel):
    title: str
    content: str
    rating: int  # 1-5 stars


class TestimonialCreate(TestimonialBase):
    pass


class TestimonialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    rating: Optional[int] = None
    is_featured: Optional[bool] = None
    is_approved: Optional[bool] = None


class Testimonial(TestimonialBase):
    id: int
    user_id: int
    is_featured: bool
    is_approved: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: Optional[dict] = None

    class Config:
        from_attributes = True


class BlogPostBase(BaseModel):
    title: str
    slug: str
    content: str
    excerpt: Optional[str] = None
    featured_image_url: Optional[str] = None
    is_published: bool = False


class BlogPostCreate(BlogPostBase):
    author_id: int


class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    featured_image_url: Optional[str] = None
    is_published: Optional[bool] = None


class BlogPost(BlogPostBase):
    id: int
    author_id: int
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: Optional[dict] = None

    class Config:
        from_attributes = True


class ContactInquiryBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: str
    message: str
    course_interest: Optional[str] = None


class ContactInquiryCreate(ContactInquiryBase):
    pass


class ContactInquiryUpdate(BaseModel):
    is_resolved: Optional[bool] = None
    resolved_at: Optional[datetime] = None


class ContactInquiry(ContactInquiryBase):
    id: int
    user_id: Optional[int] = None
    is_resolved: bool
    resolved_at: Optional[datetime] = None
    created_at: datetime
    user: Optional[dict] = None

    class Config:
        from_attributes = True
