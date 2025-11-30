# Wealth Genius Trading Education Platform - Backend

A comprehensive Python FastAPI backend for the Wealth Genius trading education platform, providing robust APIs for course management, user authentication, and content delivery.

## Features

- **User Management**: Student, instructor, and admin roles with JWT authentication
- **Course Management**: Complete CRUD operations for courses, lessons, and features
- **Enrollment System**: Track student progress and course enrollments
- **Content Management**: Testimonials, blog posts, and contact inquiries
- **Security**: JWT tokens, password hashing, and role-based access control
- **Database**: PostgreSQL with SQLAlchemy ORM and Alembic migrations
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT with Python-Jose
- **Password Hashing**: Passlib with bcrypt
- **Migrations**: Alembic
- **Validation**: Pydantic
- **Documentation**: OpenAPI/Swagger

## Project Structure

```
Backend/
├── app/
│   ├── api/
│   │   ├── deps.py                 # API dependencies
│   │   └── v1/
│   │       ├── api.py              # Main API router
│   │       └── endpoints/
│   │           ├── auth.py         # Authentication endpoints
│   │           ├── courses.py      # Course management
│   │           ├── contact.py      # Contact inquiries
│   │           └── testimonials.py # Testimonials
│   ├── core/
│   │   ├── config.py               # Application settings
│   │   └── security.py             # Security utilities
│   ├── database/
│   │   └── database.py             # Database configuration
│   ├── models/
│   │   ├── user.py                 # User model
│   │   ├── course.py               # Course models
│   │   ├── enrollment.py           # Enrollment models
│   │   └── content.py              # Content models
│   ├── schemas/
│   │   ├── user.py                 # User schemas
│   │   ├── course.py               # Course schemas
│   │   └── content.py              # Content schemas
│   └── main.py                     # FastAPI application
├── alembic/                        # Database migrations
├── requirements.txt                 # Python dependencies
├── env.example                      # Environment variables template
├── alembic.ini                     # Alembic configuration
└── README.md                       # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL and Email (Recommended)**
   ```bash
   # Run the setup script for guided installation
   python setup_database.py
   ```

5. **Manual Setup (Alternative)**

   **PostgreSQL Setup:**
   ```bash
   # Windows: Download from https://www.postgresql.org/download/windows/
   # Mac: brew install postgresql && brew services start postgresql
   # Linux: sudo apt-get install postgresql postgresql-contrib
   
   # Create database
   createdb -U postgres marketpro_db
   ```

   **Environment Variables:**
   ```bash
   cp env.example .env
   # Edit .env with your PostgreSQL password and Gmail credentials
   ```

6. **Initialize database with sample data**
   ```bash
   python init_db.py
   ```

7. **Test email configuration (Optional)**
   ```bash
   python test_email.py
   ```

8. **Run the application**
   ```bash
   python start.py
   # or
   uvicorn app.main:app --reload
   ```

## Environment Variables

Copy `env.example` to `.env` and configure the following variables:

### Required Variables:
- `DATABASE_URL`: PostgreSQL connection string (e.g., `postgresql://postgres:password@localhost:5432/marketpro_db`)
- `SECRET_KEY`: JWT secret key (generate a long random string)
- `SMTP_USER`: Your Gmail address
- `SMTP_PASSWORD`: Gmail app password (16-character password from Google Account settings)

### Optional Variables:
- `SMTP_HOST`: SMTP server (default: `smtp.gmail.com`)
- `SMTP_PORT`: SMTP port (default: `587`)
- `REDIS_URL`: Redis connection string
- `AWS_*`: AWS S3 configuration (for file uploads)
- `STRIPE_*`: Stripe payment configuration

### Gmail Setup:
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password: Google Account → Security → 2-Step Verification → App passwords
3. Use the 16-character app password in `SMTP_PASSWORD`

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token

### Courses
- `GET /api/v1/courses/` - Get all courses
- `GET /api/v1/courses/{course_id}` - Get specific course
- `POST /api/v1/courses/` - Create course (instructors only)
- `PUT /api/v1/courses/{course_id}` - Update course
- `DELETE /api/v1/courses/{course_id}` - Delete course

### Contact
- `POST /api/v1/contact/` - Submit contact inquiry
- `GET /api/v1/contact/` - Get inquiries (admin only)

### Testimonials
- `GET /api/v1/testimonials/` - Get testimonials
- `POST /api/v1/testimonials/` - Create testimonial
- `PUT /api/v1/testimonials/{id}/approve` - Approve testimonial (admin)

## Database Models

### Users
- Students, instructors, and administrators
- JWT authentication
- Role-based permissions

### Courses
- Course information and metadata
- Lessons and course features
- Instructor assignments

### Enrollments
- Student course enrollments
- Progress tracking
- Payment information

### Content
- Testimonials from students
- Blog posts
- Contact inquiries

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Code Formatting
```bash
# Install black
pip install black

# Format code
black app/
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Deployment

### Production Setup
1. Set `ENVIRONMENT=production` in `.env`
2. Configure production database
3. Set up reverse proxy (nginx)
4. Use gunicorn for production server
5. Set up SSL certificates

### Docker Deployment
```bash
# Build image
docker build -t marketpro-backend .

# Run container
docker run -p 8000:8000 marketpro-backend
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

# Wealth Genius Backend

After setting, restart the backend.