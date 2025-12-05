"""
YouTube audio download service using yt-dlp
"""

import yt_dlp
from pathlib import Path
from typing import Tuple
from app.config import UPLOAD_DIR


def download_youtube_audio(url: str) -> Tuple[str, str]:
    """
    Download audio from YouTube URL
    
    Args:
        url: YouTube video URL
    
    Returns:
        Tuple of (audio_file_path, video_title)
    """
    try:
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(UPLOAD_DIR / '%(id)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
        # Download audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info first
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'Unknown Title')
            video_id = info.get('id', 'unknown')
            
            # Download
            ydl.download([url])
            
            # Construct output path
            audio_path = UPLOAD_DIR / f"{video_id}.mp3"
            
            if not audio_path.exists():
                raise Exception("Downloaded file not found")
            
            return str(audio_path), video_title
    
    except Exception as e:
        raise Exception(f"YouTube download failed: {str(e)}")


def validate_youtube_url(url: str) -> bool:
    """
    Validate if URL is a valid YouTube URL
    
    Args:
        url: URL to validate
    
    Returns:
        True if valid YouTube URL, False otherwise
    """
    youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
    return any(domain in url for domain in youtube_domains)