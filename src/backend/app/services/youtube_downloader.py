"""
YouTube audio download service using pytubefix
"""

from pytubefix import YouTube
from pytubefix.cli import on_progress
from pathlib import Path
from typing import Tuple
import subprocess
from app.config import UPLOAD_DIR


def download_youtube_audio(url: str) -> Tuple[str, str]:
    """
    Download audio from YouTube URL using pytubefix
    
    Args:
        url: YouTube video URL
    
    Returns:
        Tuple of (audio_file_path, video_title)
    """
    try:
        print(f"1️⃣ Creating YouTube object for: {url}")
        
        # Create YouTube object with progress callback
        yt = YouTube(url, on_progress_callback=on_progress)
        
        # Get video info
        video_title = yt.title
        video_id = yt.video_id
        print(f"2️⃣ Video: {video_title} (ID: {video_id})")
        
        # Get the highest quality audio stream
        print("3️⃣ Finding best audio stream...")
        audio_stream = get_best_audio_stream(yt)
        
        if not audio_stream:
            raise Exception("No audio stream available")
        
        print(f"4️⃣ Audio quality: {audio_stream.abr}")
        
        # Download audio to temp file
        print("5️⃣ Downloading audio...")
        temp_filename = f"{video_id}_temp"
        downloaded_file = audio_stream.download(
            output_path=str(UPLOAD_DIR),
            filename=temp_filename
        )
        print(f"6️⃣ Downloaded to: {downloaded_file}")
        
        # Convert to MP3
        output_path = UPLOAD_DIR / f"{video_id}.mp3"
        print(f"7️⃣ Converting to MP3: {output_path}")
        convert_to_mp3(downloaded_file, str(output_path))
        
        # Clean up temp file
        Path(downloaded_file).unlink()
        print("8️⃣ Cleaned up temp file")
        
        if not output_path.exists():
            raise Exception("Conversion to MP3 failed")
        
        print(f"✅ Success! Audio saved to: {output_path}")
        return str(output_path), video_title
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise Exception(f"YouTube download failed: {str(e)}")


def get_best_audio_stream(yt: YouTube):
    """
    Get the highest quality audio stream
    
    Args:
        yt: YouTube object
    
    Returns:
        Best audio stream
    """
    max_audio_bitrate = 0
    best_audio_stream = None
    
    # Find the audio stream with highest bitrate
    for audio_stream in yt.streams.filter(only_audio=True):
        try:
            # Extract bitrate value (e.g., "128kbps" -> 128)
            abr = int(audio_stream.abr.replace('kbps', ''))
            if abr > max_audio_bitrate:
                max_audio_bitrate = abr
                best_audio_stream = audio_stream
        except (AttributeError, ValueError):
            continue
    
    return best_audio_stream


def convert_to_mp3(input_file: str, output_file: str):
    """
    Convert audio file to MP3 using FFmpeg
    
    Args:
        input_file: Path to input audio file
        output_file: Path to output MP3 file
    """
    try:
        command = [
            'ffmpeg',
            '-i', input_file,
            '-vn',  # No video
            '-ab', '192k',  # 192 kbps bitrate
            '-ar', '44100',  # 44.1 kHz sample rate
            '-y',  # Overwrite output file
            output_file
        ]
        
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("✅ FFmpeg conversion successful")
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg error: {e.stderr.decode()}")
        raise Exception(f"FFmpeg conversion failed: {str(e)}")
    except FileNotFoundError:
        raise Exception("FFmpeg not found. Please install FFmpeg: https://ffmpeg.org/download.html")


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