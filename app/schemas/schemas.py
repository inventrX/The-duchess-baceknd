from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

# --- Auth & Admin User Schemas ---
class Token(BaseModel):
    """Schema for the JWT login response"""
    access_token: str
    token_type: str = "bearer"

class AdminUserResponse(BaseModel):
    """Schema for returning current authenticated admin details via GET /api/auth/me"""
    id: UUID
    email: str
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# --- Contact Message Schemas ---
class ContactCreate(BaseModel):
    """Schema for incoming contact form submissions"""
    name: str
    email: str
    message: str

class ContactUpdate(BaseModel):
    """Schema for updating contact message status (PATCH /api/contact/{message_id})"""
    is_read: Optional[bool] = None

class ContactResponse(BaseModel):
    """Schema for outgoing contact messages sent back to the admin dashboard"""
    id: UUID
    name: str
    email: str
    message: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Post (Blog) Schemas ---
class PostCreate(BaseModel):
    title: str
    slug: str
    content: str
    is_published: bool = False

class PostUpdate(BaseModel):
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

class GalleryUpdate(BaseModel):
    """Schema for updating gallery items (PUT /api/gallery/{item_id})"""
    caption: Optional[str] = None
    image_url: Optional[str] = None

class GalleryResponse(BaseModel):
    id: UUID
    image_url: str
    caption: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)