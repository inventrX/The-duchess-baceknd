from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.models import Post
from app.schemas.schemas import PostCreate, PostUpdate, PostResponse

router = APIRouter(prefix="/api/posts", tags=["Posts"])

@router.get("/", response_model=List[PostResponse])
def get_published_posts(db: Session = Depends(get_db)):
    """PUBLIC: Fetches all published blog posts."""
    return db.query(Post).filter(Post.is_published == True).order_by(Post.created_at.desc()).all()

@router.get("/{slug}", response_model=PostResponse)
def get_post_by_slug(slug: str, db: Session = Depends(get_db)):
    """PUBLIC: Fetches a single post by its unique URL slug."""
    post = db.query(Post).filter(Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    """PROTECTED: Creates a new post draft or published article."""
    existing_slug = db.query(Post).filter(Post.slug == post.slug).first()
    if existing_slug:
        raise HTTPException(status_code=400, detail="Slug already exists")

    new_post = Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: UUID, post_data: PostUpdate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    """PROTECTED: Updates an existing post."""
    post_query = db.query(Post).filter(Post.id == post_id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Update only fields sent in the request
    update_data = post_data.model_dump(exclude_unset=True)
    post_query.update(update_data)
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: UUID, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    """PROTECTED: Deletes a post."""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return None