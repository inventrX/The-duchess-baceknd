from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.routers import auth, contact
from app.routers import auth, contact, posts, gallery, uploads

# Lifespan context manager: Runs once when the server starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensures database tables are created automatically
    Base.metadata.create_all(bind=engine)
    yield
    # (Anything after yield runs when the server shuts down)

# Initialize the FastAPI App
app = FastAPI(
    title="The Duchess API",
    description="Backend for The Duchess Portfolio & Blog",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows your Next.js frontend to talk to this Python backend without being blocked.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allows all headers
)

#. Root Health Check Endpoint
@app.get("/", tags=["Health"])
def health_check():
    return {"status": "online", "message": "Welcome to The Duchess API"}

app.include_router(auth.router)
app.include_router(contact.router)
app.include_router(posts.router)
app.include_router(gallery.router)
app.include_router(uploads.router)