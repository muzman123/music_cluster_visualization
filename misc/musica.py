import librosa
import numpy as np

def extract_all_features(audio_path):
    """
    Extract the exact features found in GTZAN CSV
    """
    # Load audio
    y, sr = librosa.load(audio_path, sr=22050)
    
    # Initialize feature dictionary
    features = {}
    
    # 1. CHROMA STFT (12 pitch classes)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    features['chroma_stft_mean'] = np.mean(chroma_stft)
    features['chroma_stft_var'] = np.var(chroma_stft)
    
    # 2. RMS (Energy)
    rms = librosa.feature.rms(y=y)
    features['rms_mean'] = np.mean(rms)
    features['rms_var'] = np.var(rms)
    
    # 3. SPECTRAL CENTROID
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    features['spectral_centroid_mean'] = np.mean(spectral_centroid)
    features['spectral_centroid_var'] = np.var(spectral_centroid)
    
    # 4. SPECTRAL BANDWIDTH
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    features['spectral_bandwidth_mean'] = np.mean(spectral_bandwidth)
    features['spectral_bandwidth_var'] = np.var(spectral_bandwidth)
    
    # 5. SPECTRAL ROLLOFF
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    features['rolloff_mean'] = np.mean(spectral_rolloff)
    features['rolloff_var'] = np.var(spectral_rolloff)
    
    # 6. ZERO CROSSING RATE
    zcr = librosa.feature.zero_crossing_rate(y)
    features['zcr_mean'] = np.mean(zcr)
    features['zcr_var'] = np.var(zcr)
    
    # 7. HARMONY (harmonic component)
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    features['harmony_mean'] = np.mean(y_harmonic)
    features['harmony_var'] = np.var(y_harmonic)
    
    # 8. PERCEPTR (percussive component)
    features['perceptr_mean'] = np.mean(y_percussive)
    features['perceptr_var'] = np.var(y_percussive)
    
    # 9. TEMPO
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    features['tempo'] = float(tempo) if isinstance(tempo, np.ndarray) else tempo

    # 10. MFCCs (20 coefficients)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    for i in range(1, 21):
        features[f'mfcc{i}_mean'] = np.mean(mfccs[i-1])
        features[f'mfcc{i}_var'] = np.var(mfccs[i-1])
    
    return features

# Use it
features = extract_all_features('audios/laufey.mp3')

# Print all features
for key, value in features.items():
    print(f"{key}: {value:.6f}")