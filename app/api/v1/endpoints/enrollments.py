from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
import hashlib
import secrets

from app.api.deps import get_db
from app.schemas.enrollment import EnrollmentFormCreate, EnrollmentFormResponse, EnrollmentCreate, EnrollmentResponse
from app.models.user import User, UserRole
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.core.security import get_password_hash
from app.utils.email import send_enrollment_confirmation_email


router = APIRouter()


@router.post("/form", response_model=EnrollmentFormResponse)
def submit_enrollment_form(
    form_data: EnrollmentFormCreate,
    db: Session = Depends(get_db)
):
    """
    Submit enrollment form with user details and course information.
    Creates user if doesn't exist and creates enrollment record.
    """
    try:
        # Check if user exists by email
        existing_user = db.query(User).filter(User.email == form_data.email).first()
        user_created = False
        
        if not existing_user:
            # Create username from email
            username = form_data.email.split('@')[0]
            
            # Check if username already exists, if so append random string
            while db.query(User).filter(User.username == username).first():
                username = f"{form_data.email.split('@')[0]}_{secrets.token_hex(4)}"
            
            # Create temporary password (user will need to reset)
            temp_password = secrets.token_urlsafe(12)
            
            # Create new user
            new_user = User(
                email=form_data.email,
                username=username,
                full_name=form_data.name,
                phone=form_data.phone,
                city=form_data.city,
                hashed_password=get_password_hash(temp_password),
                role=UserRole.STUDENT,
                is_active=True,
                is_verified=False
            )
            
            db.add(new_user)
            db.flush()  # Get the user ID without committing
            user = new_user
            user_created = True
        else:
            # Update existing user with new information if provided
            if form_data.name and not existing_user.full_name:
                existing_user.full_name = form_data.name
            if form_data.phone and not existing_user.phone:
                existing_user.phone = form_data.phone
            if form_data.city and not existing_user.city:
                existing_user.city = form_data.city
            
            user = existing_user
        
        # Find course by title
        course = db.query(Course).filter(Course.title == form_data.course_title).first()
        if not course:
            # If course doesn't exist, create a basic record
            # Extract price number from course_price string (e.g., "₹15,000" -> 15000)
            price_str = form_data.course_price.replace('₹', '').replace(',', '')
            try:
                price = float(price_str)
            except ValueError:
                price = 0.0
            
            # Import required enums
            from app.models.course import CourseLevel, CourseCategory
            
            # Create a slug from title
            slug = form_data.course_title.lower().replace(' ', '-').replace('+', '-plus')
            
            # Get or create a default instructor (admin user)
            default_instructor = db.query(User).filter(User.role == UserRole.ADMIN).first()
            if not default_instructor:
                # If no admin exists, get first instructor or create a default
                default_instructor = db.query(User).filter(User.role == UserRole.INSTRUCTOR).first()
                if not default_instructor:
                    # Create a default instructor user if none exists
                    default_instructor = User(
                        email="instructor@wealthgenius.com",
                        username="default_instructor",
                        full_name="Default Instructor",
                        hashed_password=get_password_hash("default_password"),
                        role=UserRole.INSTRUCTOR,
                        is_active=True
                    )
                    db.add(default_instructor)
                    db.flush()
                
            course = Course(
                title=form_data.course_title,
                slug=slug,
                description=f"Course enrollment for {form_data.course_title}",
                level=CourseLevel.BEGINNER,
                category=CourseCategory.STOCK_MARKET,
                duration_weeks=4,
                price=price,
                is_published=True,
                instructor_id=default_instructor.id
            )
            db.add(course)
            db.flush()
        
        # Check if enrollment already exists
        existing_enrollment = db.query(Enrollment).filter(
            Enrollment.user_id == user.id,
            Enrollment.course_id == course.id
        ).first()
        
        if existing_enrollment:
            db.commit()
            return EnrollmentFormResponse(
                message=f"You are already enrolled in {course.title}",
                enrollment_id=existing_enrollment.id,
                user_created=user_created
            )
        
        # Create enrollment with form data
        enrollment = Enrollment(
            user_id=user.id,
            course_id=course.id,
            student_name=form_data.name,
            student_email=form_data.email,
            student_phone=form_data.phone,
            student_city=form_data.city,
            course_title=form_data.course_title,
            course_price=form_data.course_price,
            payment_amount=course.price,
            payment_method="pending"  # Will be updated when payment is processed
        )
        
        db.add(enrollment)
        db.commit()
        
        # Send confirmation email to customer
        try:
            email_sent = send_enrollment_confirmation_email(
                student_name=form_data.name,
                student_email=form_data.email,
                course_title=form_data.course_title,
                course_price=form_data.course_price,
                enrollment_id=enrollment.id
            )
            if not email_sent:
                print(f"Warning: Failed to send enrollment confirmation email to {form_data.email}")
        except Exception as e:
            print(f"Error sending enrollment confirmation email: {e}")
            # Don't fail the enrollment if email fails
        
        return EnrollmentFormResponse(
            message=f"Enrollment request submitted successfully for {course.title}! We will contact you soon.",
            enrollment_id=enrollment.id,
            user_created=user_created
        )
        
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating enrollment. Please try again."
        )
    except Exception as e:
        # Rollback and log the full exception to stdout so it appears in host logs
        db.rollback()
        import traceback
        print("Exception in submit_enrollment_form:", str(e))
        traceback.print_exc()
        # Re-raise a generic HTTPException for the client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while processing enrollment."
        )


@router.get("/user/{user_id}", response_model=list[EnrollmentResponse])
def get_user_enrollments(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all enrollments for a specific user"""
    enrollments = db.query(Enrollment).filter(Enrollment.user_id == user_id).all()
    return enrollments


@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
def get_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):
    """Get specific enrollment details"""
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    return enrollment