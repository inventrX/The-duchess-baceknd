from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.models import ContactMessage
from app.schemas.schemas import ContactCreate, ContactResponse
from app.database.session import get_db
from app.core.dependencies import get_current_admin
from app.models.models import AdminUser
from app.schemas.contact import ContactResponse, ContactUpdate

# Create the router (Groups all /api/contact routes together)
router = APIRouter(prefix="/api/contact", tags=["Contact"])

@router.post("/", response_model=ContactResponse)
def submit_contact_form(message: ContactCreate, db: Session = Depends(get_db)):
    """PUBLIC: Next.js sends the contact form data here to save to the database."""
    
    # 1. Convert Pydantic schema into a SQLAlchemy database model
    new_message = ContactMessage(
        name=message.name,
        email=message.email,
        message=message.message
    )
    
    # 2. Save it to Postgres
    db.add(new_message)
    db.commit()
    db.refresh(new_message) # Gets the newly generated UUID from the database
    
    return new_message

@router.get("/", response_model=List[ContactResponse])
def get_all_messages(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    """PRIVATE: Fetches all messages. Requires a valid JWT admin token!"""
    
    # Query all messages, ordered by newest first
    messages = db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()
    return messages

@router.patch("/{message_id}", response_model=ContactResponse)
def update_contact_message(
    message_id: UUID,
    update_data: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_admin)
):
    """Update a contact message (e.g., toggle is_read status)."""
    message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(message, key, value)
        
    db.commit()
    db.refresh(message)
    return message

@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact_message(
    message_id: UUID,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    """Permanently delete a contact message."""
    message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
        
    db.delete(message)
    db.commit()
    return