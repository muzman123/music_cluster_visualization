"""
Song management API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
import os

from app.database import get_db
from app.models.song import Song
from app.schemas.song import SongResponse, SongListResponse, ClusterDataResponse, Vertex
from app.services.cluster_calculator import get_vertex_positions

router = APIRouter()


@router.get("", response_model=SongListResponse)
async def get_songs(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    genre: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get paginated list of songs with optional genre filter
    """
    query = db.query(Song)
    
    # Apply genre filter if provided
    if genre:
        query = query.filter(Song.predicted_genre == genre)
    
    # Get total count
    total = query.count()
    
    # Apply pagination and ordering
    songs = query.order_by(Song.created_at.desc()).offset(offset).limit(limit).all()
    
    # Convert to response format
    song_responses = [SongResponse.from_orm(song) for song in songs]
    
    return SongListResponse(
        songs=song_responses,
        total=total,
        limit=limit,
        offset=offset
    )


@router.get("/{song_id}", response_model=SongResponse)
async def get_song(
    song_id: int,
    db: Session = Depends(get_db)
):
    """
    Get specific song by ID
    """
    song = db.query(Song).filter(Song.id == song_id).first()
    
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    return SongResponse.from_orm(song)


@router.delete("/{song_id}")
async def delete_song(
    song_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a song by ID
    """
    song = db.query(Song).filter(Song.id == song_id).first()
    
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    # Delete audio file if it exists
    if song.file_path and os.path.exists(song.file_path):
        try:
            os.remove(song.file_path)
        except:
            pass  # Continue even if file deletion fails
    
    # Delete from database
    db.delete(song)
    db.commit()
    
    return {"success": True, "message": "Song deleted successfully"}


@router.get("/cluster-data", response_model=ClusterDataResponse, include_in_schema=False)
async def get_cluster_data(db: Session = Depends(get_db)):
    """
    Get all data needed for cluster visualization
    (This endpoint is at /api/songs/cluster-data due to prefix)
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