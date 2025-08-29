from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.models.user import User
from app.models.content import Testimonial
from app.schemas.content import Testimonial as TestimonialSchema, TestimonialCreate, TestimonialUpdate

router = APIRouter()


@router.get("/", response_model=List[TestimonialSchema])
def get_testimonials(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    featured: bool = Query(None),
    approved: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get all testimonials with optional filtering"""
    query = db.query(Testimonial)
    
    if featured is not None:
        query = query.filter(Testimonial.is_featured == featured)
    if approved is not None:
        query = query.filter(Testimonial.is_approved == approved)
    
    testimonials = query.order_by(Testimonial.created_at.desc()).offset(skip).limit(limit).all()
    return testimonials


@router.get("/{testimonial_id}", response_model=TestimonialSchema)
def get_testimonial(testimonial_id: int, db: Session = Depends(get_db)):
    """Get a specific testimonial by ID"""
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not testimonial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testimonial not found"
        )
    return testimonial


@router.post("/", response_model=TestimonialSchema)
def create_testimonial(
    testimonial_data: TestimonialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new testimonial"""
    db_testimonial = Testimonial(
        **testimonial_data.dict(),
        user_id=current_user.id
    )
    db.add(db_testimonial)
    db.commit()
    db.refresh(db_testimonial)
    return db_testimonial


@router.put("/{testimonial_id}", response_model=TestimonialSchema)
def update_testimonial(
    testimonial_id: int,
    testimonial_data: TestimonialUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a testimonial (owner or admin only)"""
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not testimonial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testimonial not found"
        )
    
    # Check if user is the owner or admin
    if testimonial.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    update_data = testimonial_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(testimonial, field, value)
    
    db.commit()
    db.refresh(testimonial)
    return testimonial


@router.delete("/{testimonial_id}")
def delete_testimonial(
    testimonial_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a testimonial (owner or admin only)"""
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not testimonial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testimonial not found"
        )
    
    # Check if user is the owner or admin
    if testimonial.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db.delete(testimonial)
    db.commit()
    return {"message": "Testimonial deleted successfully"}


@router.put("/{testimonial_id}/approve")
def approve_testimonial(
    testimonial_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Approve a testimonial (admin only)"""
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not testimonial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testimonial not found"
        )
    
    testimonial.is_approved = True
    db.commit()
    return {"message": "Testimonial approved successfully"}


@router.put("/{testimonial_id}/feature")
def feature_testimonial(
    testimonial_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Feature/unfeature a testimonial (admin only)"""
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not testimonial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testimonial not found"
        )
    
    testimonial.is_featured = not testimonial.is_featured
    db.commit()
    return {"message": f"Testimonial {'featured' if testimonial.is_featured else 'unfeatured'} successfully"}
