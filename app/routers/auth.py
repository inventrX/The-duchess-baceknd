from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.models.models import AdminUser
from app.schemas.schemas import Token
from app.core.dependencies import get_current_user
from app.schemas.user import UserResponse
from app.models.users import User

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Logs in an admin and returns a JWT token."""
    
    # 1. Find the user by email (OAuth2PasswordRequestForm uses 'username' for the email field)
    admin = db.query(AdminUser).filter(AdminUser.email == form_data.username).first()
    
    # 2. Check if user exists AND password is correct
    if not admin or not verify_password(form_data.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Generate the token
    access_token = create_access_token(data={"sub": admin.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user."""
    return current_user