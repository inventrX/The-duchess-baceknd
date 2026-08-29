from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

# --- Auth Schemas ---
class Token(BaseModel):
    """Schema for the JWT login response"""
    access_token: str
    token_type: str = "bearer"

# --- Contact Message Schemas ---
class ContactCreate(BaseModel):
    """Schema for incoming contact form submissions"""
    name: str
    email: str
    message: str

class ContactResponse(BaseModel):
    """Schema for outgoing contact messages sent back to the admin dashboard"""
    id: UUID
    name: str
    email: str
    message: str
    is_read: bool
    created_at: datetime
    
    # Tells Pydantic to read data directly from the SQLAlchemy database models
    model_config = ConfigDict(from_attributes=True)

# --- Post (Blog) Schemas ---
class PostCreate(BaseModel):
    title: str
    slug: str
    content: str
    is_published: bool = False

class PostUpdate(BaseModel):
    # Optional means the user doesn't have to update every field at once
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None

class PostResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    content: str
    is_published: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Gallery Schemas ---
class GalleryCreate(BaseModel):
    image_url: str
    caption: Optional[str] = None

class GalleryResponse(BaseModel):
    id: UUID
    image_url: str
    caption: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)