from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.api.deps import get_current_admin, get_current_user
from typing import Optional
from app.models.user import User
from app.models.content import ContactInquiry
from app.schemas.content import ContactInquiry as ContactInquirySchema, ContactInquiryCreate, ContactInquiryUpdate

router = APIRouter()


@router.post("/", response_model=ContactInquirySchema)
def create_contact_inquiry(
    inquiry_data: ContactInquiryCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Create a new contact inquiry"""
    db_inquiry = ContactInquiry(
        **inquiry_data.dict(),
        user_id=current_user.id if current_user else None
    )
    db.add(db_inquiry)
    db.commit()
    db.refresh(db_inquiry)
    
    # TODO: Send email notification to admin
    # send_contact_notification_email(db_inquiry)
    
    return db_inquiry


@router.get("/", response_model=List[ContactInquirySchema])
def get_contact_inquiries(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    resolved: bool = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Get all contact inquiries (admin only)"""
    query = db.query(ContactInquiry)
    
    if resolved is not None:
        query = query.filter(ContactInquiry.is_resolved == resolved)
    
    inquiries = query.order_by(ContactInquiry.created_at.desc()).offset(skip).limit(limit).all()
    return inquiries


@router.get("/{inquiry_id}", response_model=ContactInquirySchema)
def get_contact_inquiry(
    inquiry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Get a specific contact inquiry (admin only)"""
    inquiry = db.query(ContactInquiry).filter(ContactInquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact inquiry not found"
        )
    return inquiry


@router.put("/{inquiry_id}", response_model=ContactInquirySchema)
def update_contact_inquiry(
    inquiry_id: int,
    inquiry_data: ContactInquiryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Update a contact inquiry (admin only)"""
    inquiry = db.query(ContactInquiry).filter(ContactInquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact inquiry not found"
        )
    
    update_data = inquiry_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(inquiry, field, value)
    
    db.commit()
    db.refresh(inquiry)
    return inquiry


@router.delete("/{inquiry_id}")
def delete_contact_inquiry(
    inquiry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete a contact inquiry (admin only)"""
    inquiry = db.query(ContactInquiry).filter(ContactInquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact inquiry not found"
        )
    
    db.delete(inquiry)
    db.commit()
    return {"message": "Contact inquiry deleted successfully"}
