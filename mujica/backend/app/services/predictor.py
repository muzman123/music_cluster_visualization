"""
Genre prediction service using the trained PyTorch model
"""

import torch
import pickle
import numpy as np
from typing import Dict, Tuple
from pathlib import Path
import sys

# Add ml_models directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "ml_models"))

from ml_models.model_classes import ConfigurableBiLSTMAttentionModel
from app.config import MODEL_PATH, GENRE_ORDER


class GenrePredictor:
    """
    Genre prediction service that loads and uses the trained model
    """
    
    def __init__(self):
        """Initialize the predictor and load the model"""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_columns = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained model and associated components"""
        try:
            # Load model package
            with open(MODEL_PATH, 'rb') as f:
                model_package = pickle.load(f)
            
            # Extract components
            self.scaler = model_package['scaler']
            self.label_encoder = model_package['label_encoder']
            self.feature_columns = model_package['feature_columns']
            config = model_package['config']
            input_dim = model_package['input_dim']
            
            # Initialize model architecture
            self.model = ConfigurableBiLSTMAttentionModel(config, input_dim).to(self.device)
            
            # Load trained weights
            self.model.load_state_dict(model_package['model_state_dict'])
            self.model.eval()
            
            print(f"✓ Model loaded successfully on {self.device}")
            print(f"  Test Accuracy: {model_package.get('test_accuracy', 'N/A')}")
            
        except Exception as e:
            raise Exception(f"Failed to load model: {str(e)}")
    
    def predict(self, features: Dict[str, float]) -> Tuple[str, float, np.ndarray]:
        """
        Predict genre from extracted features (single segment)
        
        Args:
            features: Dictionary with 58 audio features
        
        Returns:
            Tuple of (predicted_genre, confidence, probabilities_array)
        """
        try:
            # Convert features to vector in correct order
            feature_vector = np.array([features[col] for col in self.feature_columns])
            
            # Normalize features using training scaler
            feature_vector_scaled = self.scaler.transform(feature_vector.reshape(1, -1))
            
            # Convert to PyTorch tensor
            feature_tensor = torch.FloatTensor(feature_vector_scaled).to(self.device)
            
            # Make prediction
            with torch.no_grad():
                output = self.model(feature_tensor)
                probabilities = torch.softmax(output, dim=1)
                predicted_class = torch.argmax(probabilities, dim=1).item()
                confidence = probabilities[0, predicted_class].item()
            
            # Get genre name
            predicted_genre = self.label_encoder.inverse_transform([predicted_class])[0]
            
            # Get all probabilities as numpy array
            all_probabilities = probabilities[0].cpu().numpy()
            
            return predicted_genre, confidence, all_probabilities
            
        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")
    
    def predict_multi_segment(self, audio_path: str, num_segments: int = 10) -> Tuple[str, float, np.ndarray]:
        """
        Predict genre by analyzing multiple 3-second segments (more accurate)
        
        Args:
            audio_path: Path to audio file
            num_segments: Number of segments to analyze (default 10)
        
        Returns:
            Tuple of (predicted_genre, confidence, averaged_probabilities)
        """
        import librosa
        from app.services.audio_processor import extract_features
        
        try:
            # Load full audio
            y_full, sr = librosa.load(audio_path, sr=22050)
            total_duration = len(y_full) / sr
            segment_duration = 3.0
            segment_samples = int(segment_duration * sr)
            
            # Determine segment positions (evenly spaced)
            if total_duration < segment_duration:
                # Audio too short, use single segment
                features = extract_features(audio_path)
                return self.predict(features)
            
            max_offset = total_duration - segment_duration
            if num_segments == 1:
                offsets = [max_offset / 2]
            else:
                offsets = np.linspace(0, max_offset, num_segments)
            
            # Predict for each segment
            all_probabilities = []
            
            for offset in offsets:
                # Extract segment
                start_sample = int(offset * sr)
                end_sample = start_sample + segment_samples
                y_segment = y_full[start_sample:end_sample]
                
                # Pad if needed
                if len(y_segment) < segment_samples:
                    y_segment = np.pad(y_segment, (0, segment_samples - len(y_segment)))
                
                # Extract features from segment
                features = self._extract_features_from_array(y_segment, sr)
                
                # Predict
                _, _, probs = self.predict(features)
                all_probabilities.append(probs)
            
            # Average probabilities across all segments
            avg_probabilities = np.mean(all_probabilities, axis=0)
            
            # Get final prediction
            predicted_class = np.argmax(avg_probabilities)
            predicted_genre = self.label_encoder.inverse_transform([predicted_class])[0]
            confidence = avg_probabilities[predicted_class]
            
            return predicted_genre, confidence, avg_probabilities
            
        except Exception as e:
            raise Exception(f"Multi-segment prediction failed: {str(e)}")
    
    def _extract_features_from_array(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        """Extract features from audio array (for multi-segment)"""
        import librosa
        
        features = {}
        
        features['length'] = len(y)
        
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        features['chroma_stft_mean'] = np.mean(chroma_stft)
        features['chroma_stft_var'] = np.var(chroma_stft)
        
        rms = librosa.feature.rms(y=y)
        features['rms_mean'] = np.mean(rms)
        features['rms_var'] = np.var(rms)
        
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        features['spectral_centroid_mean'] = np.mean(spec_cent)
        features['spectral_centroid_var'] = np.var(spec_cent)
        
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        features['spectral_bandwidth_mean'] = np.mean(spec_bw)
        features['spectral_bandwidth_var'] = np.var(spec_bw)
        
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        features['rolloff_mean'] = np.mean(rolloff)
        features['rolloff_var'] = np.var(rolloff)
        
        zcr = librosa.feature.zero_crossing_rate(y)
        features['zero_crossing_rate_mean'] = np.mean(zcr)
        features['zero_crossing_rate_var'] = np.var(zcr)
        
        y_harm, y_perc = librosa.effects.hpss(y)
        features['harmony_mean'] = np.mean(y_harm)
        features['harmony_var'] = np.var(y_harm)
        features['perceptr_mean'] = np.mean(y_perc)
        features['perceptr_var'] = np.var(y_perc)
        
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        features['tempo'] = float(tempo.item() if isinstance(tempo, np.ndarray) else tempo)
        
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        for i in range(1, 21):
            features[f'mfcc{i}_mean'] = np.mean(mfccs[i-1])
            features[f'mfcc{i}_var'] = np.var(mfccs[i-1])
        
        return features
    
    def get_probabilities_dict(self, probabilities: np.ndarray) -> Dict[str, float]:
        """
        Convert probability array to dictionary with genre names
        
        Args:
            probabilities: NumPy array of 10 probabilities
        
        Returns:
            Dictionary mapping genre names to probabilities
        """
        prob_dict = {}
        for genre, prob in zip(self.label_encoder.classes_, probabilities):
            prob_dict[genre] = float(prob)
        return prob_dict


# Global predictor instance (singleton)
_predictor_instance = None


def get_predictor() -> GenrePredictor:
    """
    Get the global predictor instance (lazy initialization)
    
    Returns:
        GenrePredictor instance
    """
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = GenrePredictor()
    return _predictor_instance