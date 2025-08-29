from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.course import CourseLevel, CourseCategory


class CourseFeatureBase(BaseModel):
    feature_name: str
    feature_description: Optional[str] = None
    icon: Optional[str] = None
    order: int = 0


class CourseFeatureCreate(CourseFeatureBase):
    pass


class CourseFeature(CourseFeatureBase):
    id: int
    course_id: int

    class Config:
        from_attributes = True


class LessonBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    video_url: Optional[str] = None
    duration_minutes: Optional[int] = None
    order: int
    is_free: bool = False


class LessonCreate(LessonBase):
    pass


class Lesson(LessonBase):
    id: int
    course_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    title: str
    slug: str
    description: str
    short_description: Optional[str] = None
    level: CourseLevel
    category: CourseCategory
    duration_weeks: int
    price: float
    original_price: Optional[float] = None
    is_featured: bool = False
    is_published: bool = False
    thumbnail_url: Optional[str] = None
    video_intro_url: Optional[str] = None


class CourseCreate(CourseBase):
    instructor_id: int


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    level: Optional[CourseLevel] = None
    category: Optional[CourseCategory] = None
    duration_weeks: Optional[int] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    is_featured: Optional[bool] = None
    is_published: Optional[bool] = None
    thumbnail_url: Optional[str] = None
    video_intro_url: Optional[str] = None


class Course(CourseBase):
    id: int
    instructor_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    instructor: Optional[dict] = None
    lessons: List[Lesson] = []
    course_features: List[CourseFeature] = []

    class Config:
        from_attributes = True


class CourseWithStats(Course):
    enrollment_count: int = 0
    average_rating: float = 0.0
    total_lessons: int = 0
