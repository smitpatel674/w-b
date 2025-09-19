#!/usr/bin/env python3
"""
Database initialization script for Wealth Genius Backend
Creates sample data for development and testing
"""
import asyncio
from sqlalchemy.orm import Session
from app.database.database import SessionLocal, engine
from app.models.user import User, UserRole, Base
from app.models.course import Course, CourseLevel, CourseCategory, CourseFeature, Lesson, Base as CourseBase
from app.models.content import Testimonial, BlogPost, Base as ContentBase
from app.core.security import get_password_hash
from app.models.enrollment import Base as EnrollmentBase

# Create all tables
Base.metadata.create_all(bind=engine)
CourseBase.metadata.create_all(bind=engine)
ContentBase.metadata.create_all(bind=engine)
EnrollmentBase.metadata.create_all(bind=engine)


def init_db():
    db = SessionLocal()
    
    try:
        # Create admin user
        admin_user = db.query(User).filter(User.email == "admin@marketpro.com").first()
        if not admin_user:
            admin_user = User(
                email="admin@marketpro.com",
                username="admin",
                full_name="Admin User",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.ADMIN,
                is_verified=True,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Admin user created")

        # Create instructor users
        instructor1 = db.query(User).filter(User.email == "michael@marketpro.com").first()
        if not instructor1:
            instructor1 = User(
                email="michael@marketpro.com",
                username="michael_davis",
                full_name="Michael Davis",
                hashed_password=get_password_hash("instructor123"),
                role=UserRole.INSTRUCTOR,
                is_verified=True,
                is_active=True,
                bio="15+ years Wall Street experience, specializing in day trading and options strategies."
            )
            db.add(instructor1)
            db.commit()
            print("✅ Instructor 1 created")

        instructor2 = db.query(User).filter(User.email == "sarah@marketpro.com").first()
        if not instructor2:
            instructor2 = User(
                email="sarah@marketpro.com",
                username="sarah_kim",
                full_name="Sarah Kim",
                hashed_password=get_password_hash("instructor123"),
                role=UserRole.INSTRUCTOR,
                is_verified=True,
                is_active=True,
                bio="12+ years hedge fund experience, expert in fundamental analysis."
            )
            db.add(instructor2)
            db.commit()
            print("✅ Instructor 2 created")

        # Create sample courses
        course1 = db.query(Course).filter(Course.slug == "stock-market-fundamentals").first()
        if not course1:
            course1 = Course(
                title="Stock Market Fundamentals",
                slug="stock-market-fundamentals",
                description="Perfect foundation for beginners. Learn market basics, terminology, and foundational concepts that every trader needs to know.",
                short_description="Perfect for beginners, this course covers market basics, terminology, and foundational concepts.",
                level=CourseLevel.BEGINNER,
                category=CourseCategory.STOCK_MARKET,
                duration_weeks=6,
                price=299.0,
                original_price=399.0,
                is_featured=True,
                is_published=True,
                instructor_id=instructor1.id
            )
            db.add(course1)
            db.commit()
            print("✅ Course 1 created")

            # Add course features
            features = [
                CourseFeature(course_id=course1.id, feature_name="Market Structure", feature_description="Understanding how markets work", order=1),
                CourseFeature(course_id=course1.id, feature_name="Risk Management", feature_description="Protecting your capital", order=2),
                CourseFeature(course_id=course1.id, feature_name="Basic Analysis", feature_description="Fundamental and technical basics", order=3)
            ]
            db.add_all(features)
            db.commit()

            # Add lessons
            lessons = [
                Lesson(course_id=course1.id, title="Introduction to Stock Markets", description="Overview of how stock markets work", order=1, is_free=True),
                Lesson(course_id=course1.id, title="Market Participants", description="Who trades and why", order=2),
                Lesson(course_id=course1.id, title="Basic Terminology", description="Essential trading terms", order=3),
                Lesson(course_id=course1.id, title="Risk Management Basics", description="Protecting your investment", order=4),
                Lesson(course_id=course1.id, title="Your First Trade", description="Practical trading exercise", order=5),
                Lesson(course_id=course1.id, title="Course Review", description="Summary and next steps", order=6)
            ]
            db.add_all(lessons)
            db.commit()

        course2 = db.query(Course).filter(Course.slug == "technical-analysis-mastery").first()
        if not course2:
            course2 = Course(
                title="Technical Analysis Mastery",
                slug="technical-analysis-mastery",
                description="Master chart patterns, indicators, and technical analysis tools used by professional traders.",
                short_description="Master chart patterns, indicators, and technical analysis tools used by professional traders.",
                level=CourseLevel.INTERMEDIATE,
                category=CourseCategory.TECHNICAL_ANALYSIS,
                duration_weeks=8,
                price=599.0,
                original_price=799.0,
                is_featured=True,
                is_published=True,
                instructor_id=instructor2.id
            )
            db.add(course2)
            db.commit()
            print("✅ Course 2 created")

        course3 = db.query(Course).filter(Course.slug == "options-trading-strategies").first()
        if not course3:
            course3 = Course(
                title="Options Trading Strategies",
                slug="options-trading-strategies",
                description="Advanced options strategies for hedging, income generation, and directional plays.",
                short_description="Advanced options strategies for hedging, income generation, and directional plays.",
                level=CourseLevel.ADVANCED,
                category=CourseCategory.OPTIONS_TRADING,
                duration_weeks=10,
                price=899.0,
                original_price=1199.0,
                is_featured=False,
                is_published=True,
                instructor_id=instructor1.id
            )
            db.add(course3)
            db.commit()
            print("✅ Course 3 created")

        # Create sample testimonials
        testimonial1 = db.query(Testimonial).filter(Testimonial.title == "Transformed My Trading").first()
        if not testimonial1:
            testimonial1 = Testimonial(
                user_id=admin_user.id,  # Using admin as placeholder
                title="Transformed My Trading",
                content="Wealth Genius didn't just teach me to trade - they taught me to think like a professional trader. I went from losing money consistently to generating $15K+ monthly profits.",
                rating=5,
                is_featured=True,
                is_approved=True
            )
            db.add(testimonial1)
            db.commit()
            print("✅ Testimonial 1 created")

        testimonial2 = db.query(Testimonial).filter(Testimonial.title == "Risk Management Saved Me").first()
        if not testimonial2:
            testimonial2 = Testimonial(
                user_id=admin_user.id,  # Using admin as placeholder
                title="Risk Management Saved Me",
                content="The risk management principles I learned here saved me from major losses during market volatility. My portfolio is now consistently profitable with controlled risk.",
                rating=5,
                is_featured=True,
                is_approved=True
            )
            db.add(testimonial2)
            db.commit()
            print("✅ Testimonial 2 created")

        # Create sample blog posts
        blog1 = db.query(BlogPost).filter(BlogPost.slug == "getting-started-trading").first()
        if not blog1:
            blog1 = BlogPost(
                title="Getting Started with Trading: A Complete Guide",
                slug="getting-started-trading",
                content="Trading can seem overwhelming at first, but with the right approach, anyone can learn to trade successfully...",
                excerpt="Learn the essential steps to begin your trading journey with confidence.",
                author_id=instructor1.id,
                is_published=True
            )
            db.add(blog1)
            db.commit()
            print("✅ Blog post 1 created")

        print("\n🎉 Database initialization completed successfully!")
        print("\nSample data created:")
        print("- Admin user: admin@marketpro.com / admin123")
        print("- Instructor 1: michael@marketpro.com / instructor123")
        print("- Instructor 2: sarah@marketpro.com / instructor123")
        print("- 3 sample courses")
        print("- 2 sample testimonials")
        print("- 1 sample blog post")

    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
