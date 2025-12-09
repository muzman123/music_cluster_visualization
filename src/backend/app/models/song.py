"""
SQLAlchemy database models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class Song(Base):
    """
    Song model for storing uploaded songs and their predictions
    """
    __tablename__ = "songs"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Metadata
    title = Column(String(255), nullable=False)
    source = Column(String(20), nullable=False)  # 'upload' or 'youtube'
    source_url = Column(Text, nullable=True)  # YouTube URL if applicable
    file_path = Column(Text, nullable=True)  # Path to stored audio file
    duration = Column(Float, nullable=True)  # Song duration in seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Model Predictions
    predicted_genre = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    
    # Genre Probabilities (0.0 to 1.0)
    prob_blues = Column(Float, nullable=False)
    prob_classical = Column(Float, nullable=False)
    prob_country = Column(Float, nullable=False)
    prob_disco = Column(Float, nullable=False)
    prob_hiphop = Column(Float, nullable=False)
    prob_jazz = Column(Float, nullable=False)
    prob_metal = Column(Float, nullable=False)
    prob_pop = Column(Float, nullable=False)
    prob_reggae = Column(Float, nullable=False)
    prob_rock = Column(Float, nullable=False)
    
    # Visualization Coordinates
    cluster_x = Column(Float, nullable=False)
    cluster_y = Column(Float, nullable=False)
    
    # Status
    processing_status = Column(String(20), default='completed')
    error_message = Column(Text, nullable=True)