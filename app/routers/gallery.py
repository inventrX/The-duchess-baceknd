from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.models import Gallery
from app.schemas.schemas import GalleryCreate, GalleryResponse
from app.database.session import get_db
from app.core.dependencies import get_current_admin
from app.models.models import AdminUser
from app.models.gallery import GalleryItem
from app.schemas.gallery import GalleryResponse, GalleryUpdate
router = APIRouter(prefix="/api/gallery", tags=["Gallery"])

@router.get("/", response_model=List[GalleryResponse])
def get_gallery_items(db: Session = Depends(get_db)):
    """PUBLIC: Fetches all gallery items."""
    return db.query(Gallery).order_by(Gallery.created_at.desc()).all()

@router.post("/", response_model=GalleryResponse)
def add_gallery_item(item: GalleryCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    """PROTECTED: Adds a new image entry to the gallery."""
    new_item = Gallery(**item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gallery_item(item_id: UUID, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    """PROTECTED: Removes an image entry from the gallery."""
    gallery_item = db.query(Gallery).filter(Gallery.id == item_id).first()
    if not gallery_item:
        raise HTTPException(status_code=404, detail="Gallery item not found")

    db.delete(gallery_item)
    db.commit()
    return None

@router.put("/{item_id}", response_model=GalleryResponse)
def update_gallery_item(
    item_id: UUID,
    update_data: GalleryUpdate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    """Update gallery item metadata (e.g., caption)."""
    item = db.query(GalleryItem).filter(GalleryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")
        
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(item, key, value)
        
    db.commit()
    db.refresh(item)
    return item