import time
import cloudinary.utils
from fastapi import APIRouter, Depends
from app.core.config import settings
from app.core.dependencies import get_current_admin
from app.models.models import AdminUser

router = APIRouter(prefix="/uploads", tags=["uploads"])

@router.post("/cloudinary-signature")
def get_cloudinary_signature(current_admin: AdminUser = Depends(get_current_admin)):
    """
    Generate a secure signature for client-side uploads to Cloudinary.
    Protected endpoint: only authenticated admins can request this.
    """
    timestamp = int(time.time())
    
    # Optional: You can specify a designated folder in Cloudinary here
    params_to_sign = {
        "timestamp": timestamp,
        "folder": "the_duchess"
    }
    
    signature = cloudinary.utils.api_sign_request(
        params_to_sign,
        settings.CLOUDINARY_API_SECRET
    )
    
    return {
        "timestamp": timestamp,
        "signature": signature,
        "api_key": settings.CLOUDINARY_API_KEY,
        "cloud_name": settings.CLOUDINARY_CLOUD_NAME,
        "folder": "the_duchess"
    }