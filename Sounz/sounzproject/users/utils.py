import librosa
import numpy as np
from scipy.spatial.distance import euclidean

def extract_mfcc(audio_file):
    """Extracts MFCC features from an audio file."""
    y, sr = librosa.load(audio_file, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc, axis=1)  # Take mean for simplified comparison

def compare_audio(file1, file2, threshold=50):
    """Compares two audio files using MFCC and returns similarity."""
    mfcc1 = extract_mfcc(file1)
    mfcc2 = extract_mfcc(file2)

    distance = euclidean(mfcc1, mfcc2)
    return distance < threshold  # Lower = more similar
