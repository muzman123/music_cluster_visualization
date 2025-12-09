"""
FastAPI Main Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import API_V1_PREFIX, CORS_ORIGINS
from app.database import create_tables
from app.api import upload, songs, cluster


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    print("🚀 Starting SoundScape Backend...")
    
    # Create database tables
    print("📊 Creating database tables...")
    create_tables()
    
    # Load ML model
    print("🤖 Loading ML model...")
    from app.services.predictor import get_predictor
    get_predictor()  # This will load the model
    
    print("✓ Backend ready!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Mujica API",
    description="Music Genre Classification and Cluster Visualization API",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix=f"{API_V1_PREFIX}/upload", tags=["Upload"])
app.include_router(songs.router, prefix=f"{API_V1_PREFIX}/songs", tags=["Songs"])
app.include_router(cluster.router, prefix=f"{API_V1_PREFIX}", tags=["Cluster"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Mujica API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Simple health check"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)