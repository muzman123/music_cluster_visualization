"""
Audio feature extraction service
Extracts 58 audio features from MP3/WAV files using librosa
"""

import librosa
import numpy as np
from typing import Dict
from app.config import AUDIO_DURATION, SAMPLE_RATE


def extract_features(audio_path: str, duration: int = AUDIO_DURATION) -> Dict[str, float]:
    """
    Extract 58 audio features from audio file (same as training)
    
    Args:
        audio_path: Path to audio file
        duration: Duration to analyze (default 3 seconds)
    
    Returns:
        Dictionary with 58 features in the correct order
    """
    try:
        # Load audio
        y, sr = librosa.load(audio_path, duration=duration, sr=SAMPLE_RATE)
        
        features = {}
        
        # 0. Length (sample count, not duration!)
        features['length'] = len(y)
        
        # 1. Chroma STFT
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        features['chroma_stft_mean'] = np.mean(chroma_stft)
        features['chroma_stft_var'] = np.var(chroma_stft)
        
        # 2. RMS Energy
        rms = librosa.feature.rms(y=y)
        features['rms_mean'] = np.mean(rms)
        features['rms_var'] = np.var(rms)
        
        # 3. Spectral Centroid
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        features['spectral_centroid_mean'] = np.mean(spec_cent)
        features['spectral_centroid_var'] = np.var(spec_cent)
        
        # 4. Spectral Bandwidth
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        features['spectral_bandwidth_mean'] = np.mean(spec_bw)
        features['spectral_bandwidth_var'] = np.var(spec_bw)
        
        # 5. Rolloff
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        features['rolloff_mean'] = np.mean(rolloff)
        features['rolloff_var'] = np.var(rolloff)
        
        # 6. Zero Crossing Rate
        zcr = librosa.feature.zero_crossing_rate(y)
        features['zero_crossing_rate_mean'] = np.mean(zcr)
        features['zero_crossing_rate_var'] = np.var(zcr)
        
        # 7. Harmony and Perceptr
        y_harm, y_perc = librosa.effects.hpss(y)
        features['harmony_mean'] = np.mean(y_harm)
        features['harmony_var'] = np.var(y_harm)
        features['perceptr_mean'] = np.mean(y_perc)
        features['perceptr_var'] = np.var(y_perc)
        
        # 8. Tempo
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        features['tempo'] = float(tempo.item() if isinstance(tempo, np.ndarray) else tempo)
        
        # 9. MFCCs (20 coefficients)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        for i in range(1, 21):
            features[f'mfcc{i}_mean'] = np.mean(mfccs[i-1])
            features[f'mfcc{i}_var'] = np.var(mfccs[i-1])
        
        return features
    
    except Exception as e:
        raise Exception(f"Error extracting features: {str(e)}")


def get_audio_duration(audio_path: str) -> float:
    """
    Get the duration of an audio file in seconds
    
    Args:
        audio_path: Path to audio file
    
    Returns:
        Duration in seconds
    """
    try:
        duration = librosa.get_duration(path=audio_path)
        return duration
    except Exception as e:
        raise Exception(f"Error getting audio duration: {str(e)}")