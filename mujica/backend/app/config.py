"""
Configuration settings for the backend application
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
ML_MODELS_DIR = BASE_DIR / "ml_models"
UPLOAD_DIR = BASE_DIR / "uploads"

# Ensure upload directory exists
UPLOAD_DIR.mkdir(exist_ok=True)

# Model settings
MODEL_PATH = ML_MODELS_DIR / "pytorch_genre_classifier_best.pkl"

# File upload settings
MAX_FILE_SIZE = 52428800  # 50MB in bytes
ALLOWED_EXTENSIONS = {".mp3", ".wav"}

# Audio processing settings
AUDIO_DURATION = 3  # seconds
SAMPLE_RATE = 22050  # Hz

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./soundscape.db")

# API settings
API_V1_PREFIX = "/api"
CORS_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

# Genre settings
GENRE_ORDER = ['blues', 'classical', 'country', 'disco', 'hiphop', 
               'jazz', 'metal', 'pop', 'reggae', 'rock']

GENRE_COLORS = {
    'blues': '#4169E1',      # Royal Blue
    'classical': '#DDA0DD',  # Plum
    'country': '#D2691E',    # Chocolate
    'disco': '#FF1493',      # Deep Pink
    'hiphop': '#FF4500',     # Orange Red
    'jazz': '#FFD700',       # Gold
    'metal': '#2F4F4F',      # Dark Slate Gray
    'pop': '#FF69B4',        # Hot Pink
    'reggae': '#32CD32',     # Lime Green
    'rock': '#8B0000'        # Dark Red
}