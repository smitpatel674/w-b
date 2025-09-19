#!/usr/bin/env python3
"""
Rebuild Database Script
Drops all existing tables and recreates them with fresh data
"""
from sqlalchemy import text
from app.database.database import SessionLocal, engine
from app.models.user import User, UserRole, Base
from app.models.course import Course, CourseLevel, CourseCategory, CourseFeature, Lesson, Base as CourseBase
from app.models.content import Testimonial, BlogPost, Base as ContentBase
from app.models.enrollment import Base as EnrollmentBase
from app.core.security import get_password_hash


def drop_all_tables():
    """Drop all tables from the database"""
    try:
        with engine.connect() as connection:
            # Drop tables in correct order (to handle foreign key constraints)
            tables_to_drop = [
                'lesson_progress',
                'enrollments', 
                'course_features',
                'lessons',
                'courses',
                'testimonials',
                'blog_posts',
                'contact_inquiries',
                'users'
            ]
            
            for table in tables_to_drop:
                try:
                    connection.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                    print(f"✅ Dropped table: {table}")
                except Exception as e:
                    print(f"⚠️  Warning dropping {table}: {e}")
            
            connection.commit()
            print("\n🗑️  All tables dropped successfully!")
            
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        raise


def create_fresh_tables():
    """Create all tables with fresh schema"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        CourseBase.metadata.create_all(bind=engine)
        ContentBase.metadata.create_all(bind=engine)
        EnrollmentBase.metadata.create_all(bind=engine)
        print("🏗️  All tables created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise


def seed_fresh_data():
    """Insert fresh seed data for the trading institute website"""
    db = SessionLocal()
    
    try:
        print("\n🌱 Seeding fresh data...")
        
        # Create instructor users (matching the website)
        nainesh = User(
            email="nainesh@wealthgenius.com",
            username="nainesh_patel",
            full_name="Nainesh Patel",
            hashed_password=get_password_hash("instructor123"),
            role=UserRole.INSTRUCTOR,
            is_verified=True,
            is_active=True,
            bio="Founder & CEO with 2+ years institutional experience, specializing in day trading and options strategies.",
            city="Mumbai"
        )
        db.add(nainesh)
        
        kaushal = User(
            email="kaushal@wealthgenius.com",
            username="kaushal_patel",
            full_name="Kaushal Patel",
            hashed_password=get_password_hash("instructor123"),
            role=UserRole.INSTRUCTOR,
            is_verified=True,
            is_active=True,
            bio="Head of Curriculum with 2+ years institutional experience, expert in fundamental analysis.",
            city="Mumbai"
        )
        db.add(kaushal)
        db.commit()
        print("✅ Instructor users created")

        # Create courses matching the frontend
        course1 = Course(
            title="Stock Market Fundamentals",
            slug="stock-market-fundamentals",
            description="Perfect foundation for beginners. Learn market basics, terminology, and foundational concepts that every trader needs to know.",
            short_description="Perfect foundation for beginners",
            level=CourseLevel.BEGINNER,
            category=CourseCategory.STOCK_MARKET,
            duration_weeks=4,
            price=15000.0,
            original_price=20000.0,
            is_featured=True,
            is_published=True,
            instructor_id=nainesh.id
        )
        db.add(course1)
        
        course2 = Course(
            title="Technical + Derivatives Mastery",
            slug="technical-derivatives-mastery",
            description="Advanced chart reading techniques and derivatives trading strategies for intermediate traders.",
            short_description="Advanced chart reading techniques",
            level=CourseLevel.INTERMEDIATE,
            category=CourseCategory.TECHNICAL_ANALYSIS,
            duration_weeks=8,
            price=20000.0,
            original_price=25000.0,
            is_featured=True,
            is_published=True,
            instructor_id=kaushal.id
        )
        db.add(course2)
        
        course3 = Course(
            title="Beginner to Expert",
            slug="beginner-to-expert",
            description="Complete journey from beginner to expert trader with comprehensive curriculum.",
            short_description="Master complex options strategies",
            level=CourseLevel.ADVANCED,
            category=CourseCategory.OPTIONS_TRADING,
            duration_weeks=12,
            price=35000.0,
            original_price=50000.0,
            is_featured=True,
            is_published=True,
            instructor_id=nainesh.id
        )
        db.add(course3)
        db.commit()
        print("✅ Courses created")

        # Create course features for course1
        features1 = [
            CourseFeature(course_id=course1.id, feature_name="Market basics & segments", feature_description="Understanding market structure", order=1),
            CourseFeature(course_id=course1.id, feature_name="Investment planning & risk control", feature_description="Risk management fundamentals", order=2),
            CourseFeature(course_id=course1.id, feature_name="Trader types, IPOs & psychology", feature_description="Market psychology basics", order=3),
            CourseFeature(course_id=course1.id, feature_name="Intro to charting software", feature_description="Technical analysis tools", order=4)
        ]
        
        # Create course features for course2
        features2 = [
            CourseFeature(course_id=course2.id, feature_name="Advanced technical analysis tools", feature_description="Professional trading tools", order=1),
            CourseFeature(course_id=course2.id, feature_name="Sector & index trend trading", feature_description="Market sector analysis", order=2),
            CourseFeature(course_id=course2.id, feature_name="Futures, options & Greeks", feature_description="Derivatives fundamentals", order=3),
            CourseFeature(course_id=course2.id, feature_name="Gap strategies, MCX & intraday", feature_description="Advanced trading strategies", order=4),
            CourseFeature(course_id=course2.id, feature_name="Backtesting, mentorship & certification", feature_description="Professional development", order=5)
        ]
        
        # Create course features for course3
        features3 = [
            CourseFeature(course_id=course3.id, feature_name="Stock Market Fundamentals", feature_description="Complete market basics", order=1),
            CourseFeature(course_id=course3.id, feature_name="Technical analysis", feature_description="Advanced charting techniques", order=2),
            CourseFeature(course_id=course3.id, feature_name="Derivatives", feature_description="Options and futures mastery", order=3)
        ]
        
        db.add_all(features1 + features2 + features3)
        db.commit()
        print("✅ Course features created")

        # Create sample testimonials
        testimonials = [
            Testimonial(
                user_id=nainesh.id,  # Use instructor as testimonial author
                title="Transformed My Trading",
                content="Wealth Genius didn't just teach me to trade - they taught me to think like a professional trader. I went from losing money consistently to generating ₹15K+ monthly profits.",
                rating=5,
                is_featured=True,
                is_approved=True
            ),
            Testimonial(
                user_id=kaushal.id,  # Use instructor as testimonial author
                title="Risk Management Saved Me",
                content="The risk management principles I learned here saved me from major losses during market volatility. My portfolio is now consistently profitable with controlled risk.",
                rating=5,
                is_featured=True,
                is_approved=True
            ),
            Testimonial(
                user_id=nainesh.id,  # Use instructor as testimonial author
                title="Best Investment Ever",
                content="Best investment I've ever made. The knowledge and mentorship I received here have generated returns that paid for the course 50 times over.",
                rating=5,
                is_featured=True,
                is_approved=True
            )
        ]
        
        db.add_all(testimonials)
        db.commit()
        print("✅ Testimonials created")

        print("\n🎉 Database rebuild completed successfully!")
        print("\nFresh data created:")
        print("- Nainesh Patel (Founder): nainesh@wealthgenius.com / instructor123")
        print("- Kaushal Patel (Curriculum Head): kaushal@wealthgenius.com / instructor123")
        print("- 3 courses matching frontend exactly")
        print("- Course features for all courses")
        print("- 3 sample testimonials")
        print("- Ready for student enrollments & contact forms")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def rebuild_database():
    """Complete database rebuild process"""
    print("🚀 Starting database rebuild process...")
    print("⚠️  This will delete ALL existing data!")
    
    try:
        # Step 1: Drop all tables
        print("\n📋 Step 1: Dropping existing tables...")
        drop_all_tables()
        
        # Step 2: Create fresh tables
        print("\n📋 Step 2: Creating fresh tables...")
        create_fresh_tables()
        
        # Step 3: Seed with fresh data
        print("\n📋 Step 3: Seeding fresh data...")
        seed_fresh_data()
        
        print("\n" + "="*60)
        print("🎊 DATABASE REBUILD COMPLETE! 🎊")
        print("="*60)
        print("\nYour trading institute database is now ready with:")
        print("✅ Clean schema optimized for trading education")
        print("✅ Instructor profiles (Nainesh & Kaushal Patel)")
        print("✅ Course data matching your frontend exactly")
        print("✅ Enrollment system ready for students")
        print("✅ Contact form integration ready")
        print("✅ No unnecessary admin accounts")
        
    except Exception as e:
        print(f"\n❌ Database rebuild failed: {e}")
        print("Please check your database connection and try again.")


if __name__ == "__main__":
    rebuild_database()