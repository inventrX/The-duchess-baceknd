from pydantic import BaseModel
from typing import Optional

class GalleryUpdate(BaseModel):
    caption: Optional[str] = None
    # Add any other modifiable fields here, e.g., is_featured: Optional[bool] = None