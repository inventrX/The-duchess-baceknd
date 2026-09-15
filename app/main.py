from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.routers import auth, contact, posts, gallery, uploads

# Lifespan context manager: Runs once when the server starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensures database tables are created automatically
    Base.metadata.create_all(bind=engine)
    yield

# Initialize the FastAPI App
app = FastAPI(
    title="The Duchess API",
    description="Backend for The Duchess Portfolio & Blog",
    version="1.0.0",
    lifespan=lifespan
)

# Parse comma-separated origins from environment variables for CORS
origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root Health Check Endpoint
@app.get("/", tags=["Health"])
def health_check():
    return {"status": "online", "message": "Welcome to The Duchess API"}

# Register API Routers
app.include_router(auth.router)
app.include_router(contact.router)
app.include_router(posts.router)
app.include_router(gallery.router)
app.include_router(uploads.router)