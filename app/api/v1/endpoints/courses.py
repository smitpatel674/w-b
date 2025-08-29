from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.database import get_db
from app.api.deps import get_current_user, get_current_instructor, get_current_admin
from app.models.user import User
from app.models.course import Course, CourseFeature, Lesson, CourseLevel, CourseCategory
from app.schemas.course import (
    Course as CourseSchema, CourseCreate, CourseUpdate, CourseWithStats,
    CourseFeature as CourseFeatureSchema, CourseFeatureCreate,
    Lesson as LessonSchema, LessonCreate
)

router = APIRouter()


@router.get("/", response_model=List[CourseWithStats])
def get_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    level: Optional[CourseLevel] = None,
    category: Optional[CourseCategory] = None,
    featured: Optional[bool] = None,
    published: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    """Get all courses with optional filtering"""
    query = db.query(Course)
    
    if level:
        query = query.filter(Course.level == level)
    if category:
        query = query.filter(Course.category == category)
    if featured is not None:
        query = query.filter(Course.is_featured == featured)
    if published is not None:
        query = query.filter(Course.is_published == published)
    
    courses = query.offset(skip).limit(limit).all()
    
    # Add stats to each course
    result = []
    for course in courses:
        course_dict = CourseWithStats.from_orm(course)
        
        # Get enrollment count
        enrollment_count = db.query(func.count(course.enrollments)).scalar()
        course_dict.enrollment_count = enrollment_count
        
        # Get total lessons
        total_lessons = db.query(func.count(course.lessons)).scalar()
        course_dict.total_lessons = total_lessons
        
        # Get average rating (from testimonials)
        # This would need to be implemented based on your rating system
        
        result.append(course_dict)
    
    return result


@router.get("/{course_id}", response_model=CourseSchema)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Get a specific course by ID"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return course


@router.post("/", response_model=CourseSchema)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor)
):
    """Create a new course (instructors only)"""
    # Check if slug already exists
    existing_course = db.query(Course).filter(Course.slug == course_data.slug).first()
    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course with this slug already exists"
        )
    
    db_course = Course(**course_data.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@router.put("/{course_id}", response_model=CourseSchema)
def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor)
):
    """Update a course (instructors only)"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if user is the instructor or admin
    if course.instructor_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    update_data = course_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)
    
    db.commit()
    db.refresh(course)
    return course


@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor)
):
    """Delete a course (instructors only)"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if user is the instructor or admin
    if course.instructor_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}


# Course Features endpoints
@router.post("/{course_id}/features", response_model=CourseFeatureSchema)
def add_course_feature(
    course_id: int,
    feature_data: CourseFeatureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor)
):
    """Add a feature to a course"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if course.instructor_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db_feature = CourseFeature(**feature_data.dict(), course_id=course_id)
    db.add(db_feature)
    db.commit()
    db.refresh(db_feature)
    return db_feature


# Lessons endpoints
@router.post("/{course_id}/lessons", response_model=LessonSchema)
def add_lesson(
    course_id: int,
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor)
):
    """Add a lesson to a course"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if course.instructor_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db_lesson = Lesson(**lesson_data.dict(), course_id=course_id)
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson
