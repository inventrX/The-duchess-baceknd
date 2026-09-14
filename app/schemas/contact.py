from pydantic import BaseModel
from typing import Optional

class ContactUpdate(BaseModel):
    is_read: Optional[bool] = None