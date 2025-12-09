"""
Pydantic schemas for request/response validation
"""

from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, Field


class GenreProbabilities(BaseModel):
    """Genre probabilities response"""
    blues: float
    classical: float
    country: float
    disco: float
    hiphop: float
    jazz: float
    metal: float
    pop: float
    reggae: float
    rock: float


class Position(BaseModel):
    """2D position coordinates"""
    x: float
    y: float


class SongBase(BaseModel):
    """Base song schema"""
    title: str
    source: str  # 'upload' or 'youtube'
    source_url: Optional[str] = None


class SongCreate(SongBase):
    """Schema for creating a song"""
    pass


class YouTubeUploadRequest(BaseModel):
    """Schema for YouTube URL upload"""
    url: str = Field(..., description="YouTube video URL")


class SongResponse(BaseModel):
    """Schema for song response"""
    id: int
    title: str
    source: str
    source_url: Optional[str] = None
    predicted_genre: str
    confidence: float
    probabilities: GenreProbabilities
    position: Position
    created_at: datetime
    duration: Optional[float] = None
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_orm(cls, song):
        """Convert SQLAlchemy model to Pydantic schema"""
        return cls(
            id=song.id,
            title=song.title,
            source=song.source,
            source_url=song.source_url,
            predicted_genre=song.predicted_genre,
            confidence=song.confidence,
            probabilities=GenreProbabilities(
                blues=song.prob_blues,
                classical=song.prob_classical,
                country=song.prob_country,
                disco=song.prob_disco,
                hiphop=song.prob_hiphop,
                jazz=song.prob_jazz,
                metal=song.prob_metal,
                pop=song.prob_pop,
                reggae=song.prob_reggae,
                rock=song.prob_rock
            ),
            position=Position(
                x=song.cluster_x,
                y=song.cluster_y
            ),
            created_at=song.created_at,
            duration=song.duration
        )


class SongListResponse(BaseModel):
    """Schema for paginated song list"""
    songs: list[SongResponse]
    total: int
    limit: int
    offset: int


class Vertex(BaseModel):
    """Decagon vertex schema"""
    genre: str
    x: float
    y: float
    angle: float
    color: str


class ClusterDataResponse(BaseModel):
    """Schema for cluster visualization data"""
    vertices: list[Vertex]
    songs: list[SongResponse]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    db_connected: bool