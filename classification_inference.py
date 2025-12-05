"""
Genre Prediction Script
Usage: python predict_genre.py path/to/song.mp3
"""

import torch
import torch.nn as nn
import numpy as np
import pickle
import sys
import librosa

# ============================================================================
# MODEL ARCHITECTURE (Must match training!)
# ============================================================================

class AttentionLayer(nn.Module):
    def __init__(self, hidden_dim):
        super(AttentionLayer, self).__init__()
        self.attention = nn.Linear(hidden_dim, 1)
    
    def forward(self, lstm_output):
        attention_weights = torch.softmax(self.attention(lstm_output), dim=1)
        context = torch.sum(attention_weights * lstm_output, dim=1)
        return context, attention_weights


class BiLSTMAttentionModel(nn.Module):
    def __init__(self, input_dim, num_classes=10):
        super(BiLSTMAttentionModel, self).__init__()
        
        self.input_bn = nn.BatchNorm1d(1)
        
        self.lstm1 = nn.LSTM(input_dim, 256, batch_first=True, bidirectional=True)
        self.attention1 = AttentionLayer(512)
        self.bn1 = nn.BatchNorm1d(512)
        self.dropout1 = nn.Dropout(0.3)
        
        self.lstm2 = nn.LSTM(512, 128, batch_first=True, bidirectional=True)
        self.attention2 = AttentionLayer(256)
        self.bn2 = nn.BatchNorm1d(256)
        self.dropout2 = nn.Dropout(0.3)
        
        self.lstm3 = nn.LSTM(256, 64, batch_first=True, bidirectional=True)
        self.bn3 = nn.BatchNorm1d(128)
        self.dropout3 = nn.Dropout(0.3)
        
        self.fc1 = nn.Linear(128, 128)
        self.bn4 = nn.BatchNorm1d(128)
        self.dropout4 = nn.Dropout(0.4)
        
        self.fc2 = nn.Linear(128, 64)
        self.bn5 = nn.BatchNorm1d(64)
        self.dropout5 = nn.Dropout(0.4)
        
        self.fc3 = nn.Linear(64, num_classes)
        
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = x.unsqueeze(1)
        x = self.input_bn(x)
        
        lstm1_out, _ = self.lstm1(x)
        attn1_out, _ = self.attention1(lstm1_out)
        x = self.bn1(attn1_out)
        x = self.relu(x)
        x = self.dropout1(x)
        x = x.unsqueeze(1)
        
        lstm2_out, _ = self.lstm2(x)
        attn2_out, _ = self.attention2(lstm2_out)
        x = self.bn2(attn2_out)
        x = self.relu(x)
        x = self.dropout2(x)
        x = x.unsqueeze(1)
        
        lstm3_out, _ = self.lstm3(x)
        x = lstm3_out[:, -1, :]
        x = self.bn3(x)
        x = self.relu(x)
        x = self.dropout3(x)
        
        x = self.fc1(x)
        x = self.bn4(x)
        x = self.relu(x)
        x = self.dropout4(x)
        
        x = self.fc2(x)
        x = self.bn5(x)
        x = self.relu(x)
        x = self.dropout5(x)
        
        x = self.fc3(x)
        
        return x


# ============================================================================
# FEATURE EXTRACTION
# ============================================================================

def extract_features_from_audio(audio_path):
    """
    Extract the same 58 features that the model was trained on
    """
    print(f"Loading audio: {audio_path}")
    
    try:
        # Load audio (30 seconds, 22050 Hz sample rate - same as training)
        y, sr = librosa.load(audio_path, duration=3, sr=22050)
        print(f"✓ Audio loaded: {len(y)} samples, {sr} Hz")
        
        features = {}
        print(len(y) / sr)
        # 0. Length (duration in seconds) - IMPORTANT!
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
        
        # 7. Harmony
        y_harm, y_perc = librosa.effects.hpss(y)
        features['harmony_mean'] = np.mean(y_harm)
        features['harmony_var'] = np.var(y_harm)
        
        # 8. Perceptr (Percussive)
        features['perceptr_mean'] = np.mean(y_perc)
        features['perceptr_var'] = np.var(y_perc)
        
        # 9. Tempo - FIXED
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        if isinstance(tempo, np.ndarray):
            features['tempo'] = float(tempo.item())
        else:
            features['tempo'] = float(tempo)
        
        # 10. MFCCs (20 coefficients)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        for i in range(1, 21):
            features[f'mfcc{i}_mean'] = np.mean(mfccs[i-1])
            features[f'mfcc{i}_var'] = np.var(mfccs[i-1])
        
        print(f"✓ Extracted {len(features)} features")
        return features
    
    except Exception as e:
        print(f"✗ Error extracting features: {e}")
        return None

# ============================================================================
# PREDICTION
# ============================================================================

def predict_genre(audio_path, model_path='models/classification_mode/pytorch_genre_classifier_best.pkl'):
    """
    Predict genre for a given audio file
    """
    print("="*70)
    print("GENRE PREDICTION")
    print("="*70)
    
    # 1. Load the model package
    print(f"\nLoading model from: {model_path}")
    try:
        with open(model_path, 'rb') as f:
            model_package = pickle.load(f)
        print("✓ Model package loaded")
    except FileNotFoundError:
        print(f"✗ Model file not found: {model_path}")
        return None
    
    # 2. Extract model components
    scaler = model_package['scaler']
    label_encoder = model_package['label_encoder']
    input_dim = model_package['input_dim']
    
    # DEBUG: Print expected feature columns
    print("\n" + "="*70)
    print("DEBUG: Expected Feature Columns")
    print("="*70)
    print(f"Number of features expected: {len(model_package['feature_columns'])}")
    print(f"First 10 features: {model_package['feature_columns'][:10]}")
    print(f"Last 10 features: {model_package['feature_columns'][-10:]}")
    
    # 3. Load model architecture
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = BiLSTMAttentionModel(input_dim=input_dim, num_classes=10).to(device)
    model.load_state_dict(model_package['model_state_dict'])
    model.eval()
    print(f"✓ Model loaded on {device}")
    
    # 4. Extract features from audio
    features = extract_features_from_audio(audio_path)
    if features is None:
        return None
    
    # DEBUG: Print extracted features
    print("\n" + "="*70)
    print("DEBUG: Extracted Features")
    print("="*70)
    print(f"Number of features extracted: {len(features)}")
    print(f"Feature names: {list(features.keys())[:10]}...")
    
    # Check for NaN or inf values
    has_issues = False
    for key, value in features.items():
        if np.isnan(value) or np.isinf(value):
            print(f"⚠ WARNING: {key} = {value} (NaN or Inf!)")
            has_issues = True
    
    if not has_issues:
        print("✓ All features are valid (no NaN or Inf)")
    
    # DEBUG: Check if all expected columns exist
    missing_cols = set(model_package['feature_columns']) - set(features.keys())
    extra_cols = set(features.keys()) - set(model_package['feature_columns'])
    
    if missing_cols:
        print(f"\n⚠ MISSING FEATURES: {missing_cols}")
    if extra_cols:
        print(f"\n⚠ EXTRA FEATURES: {extra_cols}")
    
    # 5. Convert to feature vector (same order as training)
    feature_vector = np.array([features[col] for col in model_package['feature_columns']])
    print(f"\n✓ Feature vector shape: {feature_vector.shape}")
    
    # DEBUG: Print raw feature values
    print("\n" + "="*70)
    print("DEBUG: Raw Feature Values (first 10)")
    print("="*70)
    for i, col in enumerate(model_package['feature_columns'][:10]):
        print(f"{col:30s} = {feature_vector[i]:.6f}")
    
    # 6. Normalize features (using training scaler)
    feature_vector_scaled = scaler.transform(feature_vector.reshape(1, -1))
    
    # DEBUG: Print scaled feature values
    print("\n" + "="*70)
    print("DEBUG: Scaled Feature Values (first 10)")
    print("="*70)
    for i, col in enumerate(model_package['feature_columns'][:10]):
        print(f"{col:30s} = {feature_vector_scaled[0, i]:.6f}")
    
    # Check if all scaled values are the same (indicates scaling issue)
    if np.allclose(feature_vector_scaled, feature_vector_scaled[0, 0]):
        print("\n⚠ WARNING: All scaled features are nearly identical!")
        print("   This indicates a scaling problem!")
    
    # 7. Convert to PyTorch tensor
    feature_tensor = torch.FloatTensor(feature_vector_scaled).to(device)
    
    # 8. Make prediction
    print("\nPredicting...")
    with torch.no_grad():
        output = model(feature_tensor)
        probabilities = torch.softmax(output, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0, predicted_class].item()
    
    # DEBUG: Print raw model output (before softmax)
    print("\n" + "="*70)
    print("DEBUG: Model Output (logits)")
    print("="*70)
    for i, genre in enumerate(label_encoder.classes_):
        print(f"{genre:12s} = {output[0, i].item():.4f}")
    
    # 9. Get genre name
    predicted_genre = label_encoder.inverse_transform([predicted_class])[0]
    
    # 10. Display results
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print(f"Predicted Genre: {predicted_genre.upper()}")
    print(f"Confidence: {confidence*100:.2f}%")
    
    print("\nAll Genre Probabilities:")
    for i, genre in enumerate(label_encoder.classes_):
        prob = probabilities[0, i].item()
        bar = "█" * int(prob * 50)
        print(f"  {genre:12s} {prob*100:6.2f}% {bar}")
    
    print("\nTop 3 Predictions:")
    top3_probs, top3_indices = torch.topk(probabilities[0], 3)
    for i, (prob, idx) in enumerate(zip(top3_probs, top3_indices), 1):
        genre = label_encoder.inverse_transform([idx.item()])[0]
        print(f"  {i}. {genre:12s} - {prob.item()*100:.2f}%")
    
    print("="*70)
    # Add this after loading the model
    print("Expected columns:")
    print(model_package['feature_columns'])
    print("\nExtracted features:")
    print(list(features.keys()))
    return {
        'genre': predicted_genre,
        'confidence': confidence,
        'all_probabilities': probabilities[0].cpu().numpy(),
        'all_genres': label_encoder.classes_
    }

def predict_genre_multi_segment(audio_path, model_path='models/classification_model/pytorch_genre_classifier_best.pkl', num_segments=5, sampling='random'):
    """
    Predict genre by analyzing multiple 3-second segments from the song
    
    Args:
        audio_path: Path to audio file
        model_path: Path to trained model
        num_segments: Number of 3-second clips to analyze
        sampling: 'random' or 'evenly_spaced'
    """
    print("="*70)
    print(f"MULTI-SEGMENT GENRE PREDICTION ({num_segments} segments)")
    print("="*70)
    
    # 1. Load the full audio
    print(f"\nLoading full audio: {audio_path}")
    y_full, sr = librosa.load(audio_path, sr=22050)
    total_duration = len(y_full) / sr
    print(f"✓ Full audio loaded: {total_duration:.1f} seconds")
    
    # 2. Load model package
    try:
        with open(model_path, 'rb') as f:
            model_package = pickle.load(f)
        print("✓ Model package loaded")
    except FileNotFoundError:
        print(f"✗ Model file not found: {model_path}")
        return None
    
    # 3. Setup model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = BiLSTMAttentionModel(
        input_dim=model_package['input_dim'], 
        num_classes=10
    ).to(device)
    model.load_state_dict(model_package['model_state_dict'])
    model.eval()
    print(f"✓ Model loaded on {device}")
    
    scaler = model_package['scaler']
    label_encoder = model_package['label_encoder']
    
    # 4. Determine segment positions
    segment_duration = 3.0  # seconds
    segment_samples = int(segment_duration * sr)
    
    if total_duration < segment_duration:
        print(f"⚠ Warning: Audio too short ({total_duration:.1f}s), using entire clip")
        offsets = [0]
    else:
        max_offset = total_duration - segment_duration
        
        if sampling == 'random':
            # Random sampling
            np.random.seed(42)  # For reproducibility
            offsets = sorted(np.random.uniform(0, max_offset, num_segments))
        else:
            # Evenly spaced sampling
            if num_segments == 1:
                offsets = [max_offset / 2]  # Middle of song
            else:
                offsets = np.linspace(0, max_offset, num_segments)
    
    print(f"\n{'='*70}")
    print(f"Analyzing {len(offsets)} segments ({sampling} sampling):")
    print(f"{'='*70}")
    
    # 5. Extract features and predict for each segment
    all_predictions = []
    
    for i, offset in enumerate(offsets):
        # Extract segment
        start_sample = int(offset * sr)
        end_sample = start_sample + segment_samples
        y_segment = y_full[start_sample:end_sample]
        
        # Pad if needed
        if len(y_segment) < segment_samples:
            y_segment = np.pad(y_segment, (0, segment_samples - len(y_segment)))
        
        # Extract features
        features = extract_features_from_segment(y_segment, sr)
        if features is None:
            continue
        
        # Convert to feature vector
        feature_vector = np.array([features[col] for col in model_package['feature_columns']])
        feature_vector_scaled = scaler.transform(feature_vector.reshape(1, -1))
        feature_tensor = torch.FloatTensor(feature_vector_scaled).to(device)
        
        # Predict
        with torch.no_grad():
            output = model(feature_tensor)
            probabilities = torch.softmax(output, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            predicted_genre = label_encoder.inverse_transform([predicted_class])[0]
            confidence = probabilities[0, predicted_class].item()
        
        all_predictions.append({
            'genre': predicted_genre,
            'confidence': confidence,
            'probabilities': probabilities[0].cpu().numpy(),
            'offset': offset
        })
        
        print(f"  Segment {i+1} @ {offset:5.1f}s: {predicted_genre:12s} ({confidence*100:5.1f}%)")
    
    # 6. Aggregate predictions
    print(f"\n{'='*70}")
    print("AGGREGATING RESULTS")
    print(f"{'='*70}")
    
    # Method 1: Majority voting
    genre_votes = {}
    for pred in all_predictions:
        genre = pred['genre']
        genre_votes[genre] = genre_votes.get(genre, 0) + 1
    
    majority_genre = max(genre_votes, key=genre_votes.get)
    print(f"\nMajority Vote Winner: {majority_genre.upper()}")
    print(f"Vote Distribution:")
    for genre, count in sorted(genre_votes.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * count
        print(f"  {genre:12s}: {count}/{len(all_predictions)} {bar}")
    
    # Method 2: Average probabilities (more nuanced)
    avg_probabilities = np.zeros(len(label_encoder.classes_))
    for pred in all_predictions:
        avg_probabilities += pred['probabilities']
    avg_probabilities /= len(all_predictions)
    
    avg_predicted_class = np.argmax(avg_probabilities)
    avg_genre = label_encoder.classes_[avg_predicted_class]
    avg_confidence = avg_probabilities[avg_predicted_class]
    
    print(f"\nAverage Probability Winner: {avg_genre.upper()} ({avg_confidence*100:.2f}%)")
    
    # 7. Display final results
    print(f"\n{'='*70}")
    print("FINAL RESULTS")
    print(f"{'='*70}")
    
    # Use average probabilities as final result (more reliable)
    final_genre = avg_genre
    final_confidence = avg_confidence
    
    print(f"Predicted Genre: {final_genre.upper()}")
    print(f"Confidence: {final_confidence*100:.2f}%")
    
    print("\nAll Genre Probabilities (averaged):")
    sorted_indices = np.argsort(avg_probabilities)[::-1]
    for idx in sorted_indices:
        genre = label_encoder.classes_[idx]
        prob = avg_probabilities[idx]
        bar = "█" * int(prob * 50)
        print(f"  {genre:12s} {prob*100:6.2f}% {bar}")
    
    print(f"\nTop 3 Predictions:")
    top3_indices = sorted_indices[:3]
    for i, idx in enumerate(top3_indices, 1):
        genre = label_encoder.classes_[idx]
        prob = avg_probabilities[idx]
        print(f"  {i}. {genre:12s} - {prob*100:.2f}%")
    
    print(f"{'='*70}")
    
    return {
        'genre': final_genre,
        'confidence': final_confidence,
        'avg_probabilities': avg_probabilities,
        'majority_genre': majority_genre,
        'vote_counts': genre_votes,
        'all_predictions': all_predictions,
        'all_genres': label_encoder.classes_
    }


def extract_features_from_segment(y, sr):
    """
    Extract features from a 3-second audio segment
    (Same as extract_features_from_audio but works on array instead of file)
    """
    try:
        features = {}
        
        # Length (sample count)
        features['length'] = len(y)
        
        # Chroma STFT
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        features['chroma_stft_mean'] = np.mean(chroma_stft)
        features['chroma_stft_var'] = np.var(chroma_stft)
        
        # RMS Energy
        rms = librosa.feature.rms(y=y)
        features['rms_mean'] = np.mean(rms)
        features['rms_var'] = np.var(rms)
        
        # Spectral Centroid
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        features['spectral_centroid_mean'] = np.mean(spec_cent)
        features['spectral_centroid_var'] = np.var(spec_cent)
        
        # Spectral Bandwidth
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        features['spectral_bandwidth_mean'] = np.mean(spec_bw)
        features['spectral_bandwidth_var'] = np.var(spec_bw)
        
        # Rolloff
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        features['rolloff_mean'] = np.mean(rolloff)
        features['rolloff_var'] = np.var(rolloff)
        
        # Zero Crossing Rate
        zcr = librosa.feature.zero_crossing_rate(y)
        features['zero_crossing_rate_mean'] = np.mean(zcr)
        features['zero_crossing_rate_var'] = np.var(zcr)
        
        # Harmony
        y_harm, y_perc = librosa.effects.hpss(y)
        features['harmony_mean'] = np.mean(y_harm)
        features['harmony_var'] = np.var(y_harm)
        features['perceptr_mean'] = np.mean(y_perc)
        features['perceptr_var'] = np.var(y_perc)
        
        # Tempo
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        if isinstance(tempo, np.ndarray):
            features['tempo'] = float(tempo.item())
        else:
            features['tempo'] = float(tempo)
        
        # MFCCs
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        for i in range(1, 21):
            features[f'mfcc{i}_mean'] = np.mean(mfccs[i-1])
            features[f'mfcc{i}_var'] = np.var(mfccs[i-1])
        
        return features
    
    except Exception as e:
        print(f"✗ Error extracting features: {e}")
        return None

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python predict_genre.py <audio_file> [--multi] [--segments N]")
        print("\nExamples:")
        print("  python predict_genre.py song.mp3")
        print("  python predict_genre.py song.mp3 --multi")
        print("  python predict_genre.py song.mp3 --multi --segments 10")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    
    # Check for multi-segment mode
    use_multi = '--multi' in sys.argv
    
    # Get number of segments
    num_segments = 5  # default
    if '--segments' in sys.argv:
        idx = sys.argv.index('--segments')
        if idx + 1 < len(sys.argv):
            num_segments = int(sys.argv[idx + 1])
    
    # Make prediction
    if use_multi:
        result = predict_genre_multi_segment(
            audio_path, 
            num_segments=num_segments,
            sampling='evenly_spaced'  # or 'random'
        )
    else:
        result = predict_genre(audio_path)
    
    if result:
        print(f"\n✓ Prediction complete!")
    else:
        print(f"\n✗ Prediction failed!")