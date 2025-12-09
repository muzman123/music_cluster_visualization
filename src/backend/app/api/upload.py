"""
Upload API endpoints for MP3 files and YouTube URLs
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
import os

from app.database import get_db
from app.models.song import Song
from app.schemas.song import SongResponse, YouTubeUploadRequest
from app.services.audio_processor import extract_features, get_audio_duration
from app.services.predictor import get_predictor
from app.services.cluster_calculator import calculate_decagon_position
from app.services.youtube_downloader import download_youtube_audio, validate_youtube_url
from app.config import UPLOAD_DIR, MAX_FILE_SIZE, ALLOWED_EXTENSIONS

router = APIRouter()


@router.post("/mp3", response_model=SongResponse)
async def upload_mp3(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and process an MP3 file
    """
    try:
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Validate file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get audio duration
        try:
            duration = get_audio_duration(str(file_path))
        except:
            duration = None
        
        # Predict genre using multi-segment analysis (10 segments for better accuracy)
        predictor = get_predictor()
        predicted_genre, confidence, probabilities = predictor.predict_multi_segment(
            str(file_path),
            num_segments=5
        )
        
        # Calculate position
        cluster_x, cluster_y = calculate_decagon_position(probabilities)
        
        # Get probability dict
        prob_dict = predictor.get_probabilities_dict(probabilities)
        
        # Create database entry
        song = Song(
            title=Path(file.filename).stem,
            source='upload',
            file_path=str(file_path),
            duration=duration,
            predicted_genre=predicted_genre,
            confidence=confidence,
            prob_blues=prob_dict['blues'],
            prob_classical=prob_dict['classical'],
            prob_country=prob_dict['country'],
            prob_disco=prob_dict['disco'],
            prob_hiphop=prob_dict['hiphop'],
            prob_jazz=prob_dict['jazz'],
            prob_metal=prob_dict['metal'],
            prob_pop=prob_dict['pop'],
            prob_reggae=prob_dict['reggae'],
            prob_rock=prob_dict['rock'],
            cluster_x=cluster_x,
            cluster_y=cluster_y,
            processing_status='completed'
        )
        
        db.add(song)
        db.commit()
        db.refresh(song)
        
        return SongResponse.from_orm(song)
    
    except HTTPException:
        raise
    except Exception as e:
        # Clean up file if processing failed
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/youtube", response_model=SongResponse)
async def upload_youtube(
    request: YouTubeUploadRequest,
    db: Session = Depends(get_db)
):
    """
    Download and process audio from YouTube URL
    """
    try:
        # Validate YouTube URL
        if not validate_youtube_url(request.url):
            raise HTTPException(
                status_code=400,
                detail="Invalid YouTube URL"
            )
        
        # Download audio
        audio_path, video_title = download_youtube_audio(request.url)
        
        # Get audio duration
        try:
            duration = get_audio_duration(audio_path)
        except:
            duration = None
        
        # Predict genre using multi-segment analysis (10 segments for better accuracy)
        predictor = get_predictor()
        predicted_genre, confidence, probabilities = predictor.predict_multi_segment(
            audio_path,
            num_segments=5
        )
        
        # Calculate position
        cluster_x, cluster_y = calculate_decagon_position(probabilities)
        
        # Get probability dict
        prob_dict = predictor.get_probabilities_dict(probabilities)
        
        # Create database entry
        song = Song(
            title=video_title,
            source='youtube',
            source_url=request.url,
            file_path=audio_path,
            duration=duration,
            predicted_genre=predicted_genre,
            confidence=confidence,
            prob_blues=prob_dict['blues'],
            prob_classical=prob_dict['classical'],
            prob_country=prob_dict['country'],
            prob_disco=prob_dict['disco'],
            prob_hiphop=prob_dict['hiphop'],
            prob_jazz=prob_dict['jazz'],
            prob_metal=prob_dict['metal'],
            prob_pop=prob_dict['pop'],
            prob_reggae=prob_dict['reggae'],
            prob_rock=prob_dict['rock'],
            cluster_x=cluster_x,
            cluster_y=cluster_y,
            processing_status='completed'
        )
        
        db.add(song)
        db.commit()
        db.refresh(song)
        
        return SongResponse.from_orm(song)
    
    except HTTPException:
        raise
    except Exception as e:
        # Clean up file if processing failed
        if 'audio_path' in locals() and Path(audio_path).exists():
            os.remove(audio_path)
        raise HTTPException(status_code=500, detail=str(e))