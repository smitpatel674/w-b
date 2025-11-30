from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.database.database import engine
from app.models import user, course, enrollment, content, consultation

# Create database tables
user.Base.metadata.create_all(bind=engine)
course.Base.metadata.create_all(bind=engine)
enrollment.Base.metadata.create_all(bind=engine)
content.Base.metadata.create_all(bind=engine)
consultation.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.project_name,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    # If no origins are configured (empty list), fall back to allowing all origins
    # This helps avoid preflight failures if the environment variable isn't parsed
    # correctly by the deployed environment. For production, narrow this down.
    allow_origins=settings.cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(f"Configured CORS origins: {settings.cors_origins}")

# Include API router
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Wealth Genius Trading Education Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
