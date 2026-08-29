from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.models import ContactMessage
from app.schemas.schemas import ContactCreate, ContactResponse

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