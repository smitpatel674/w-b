from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base
import enum


class CourseLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class CourseCategory(str, enum.Enum):
    STOCK_MARKET = "stock_market"
    TECHNICAL_ANALYSIS = "technical_analysis"
    OPTIONS_TRADING = "options_trading"
    DAY_TRADING = "day_trading"
    PORTFOLIO_MANAGEMENT = "portfolio_management"
    ALGORITHMIC_TRADING = "algorithmic_trading"


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    short_description = Column(String, nullable=True)
    level = Column(Enum(CourseLevel), nullable=False)
    category = Column(Enum(CourseCategory), nullable=False)
    duration_weeks = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    original_price = Column(Float, nullable=True)
    is_featured = Column(Boolean, default=False)
    is_published = Column(Boolean, default=False)
    thumbnail_url = Column(String, nullable=True)
    video_intro_url = Column(String, nullable=True)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    instructor = relationship("User", back_populates="instructor_courses")
    enrollments = relationship("Enrollment", back_populates="course")
    lessons = relationship("Lesson", back_populates="course")
    course_features = relationship("CourseFeature", back_populates="course")


class CourseFeature(Base):
    __tablename__ = "course_features"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    feature_name = Column(String, nullable=False)
    feature_description = Column(String, nullable=True)
    icon = Column(String, nullable=True)
    order = Column(Integer, default=0)

    # Relationships
    course = relationship("Course", back_populates="course_features")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    video_url = Column(String, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    order = Column(Integer, nullable=False)
    is_free = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    course = relationship("Course", back_populates="lessons")
