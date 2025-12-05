"""
Cluster visualization API endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.song import Song
from app.schemas.song import SongResponse, ClusterDataResponse, Vertex
from app.services.cluster_calculator import get_vertex_positions

router = APIRouter()


@router.get("/cluster-data", response_model=ClusterDataResponse)
async def get_cluster_data(db: Session = Depends(get_db)):
    """
    Get all data needed for cluster visualization
    """
    # Get all songs
    songs = db.query(Song).order_by(Song.created_at.desc()).all()
    song_responses = [SongResponse.from_orm(song) for song in songs]
    
    # Get vertex positions
    vertices = get_vertex_positions()
    vertex_responses = [Vertex(**v) for v in vertices]
    
    return ClusterDataResponse(
        vertices=vertex_responses,
        songs=song_responses
    )


@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint
    """
    from app.services.predictor import get_predictor
    
    # Check if model is loaded
    try:
        predictor = get_predictor()
        model_loaded = predictor.model is not None
    except:
        model_loaded = False
    
    # Check database connection
    try:
        db.execute("SELECT 1")
        db_connected = True
    except:
        db_connected = False
    
    return {
        "status": "ok" if (model_loaded and db_connected) else "degraded",
        "model_loaded": model_loaded,
        "db_connected": db_connected
    }