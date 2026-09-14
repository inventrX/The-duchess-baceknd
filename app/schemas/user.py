from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    # This allows Pydantic to read directly from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)