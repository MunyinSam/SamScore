"""
Audio preprocessing module to improve transcription accuracy.
Cleans and normalizes audio before sending to basic-pitch.
"""

import librosa
import numpy as np
import soundfile as sf
import os


def preprocess_audio(input_audio_path, output_folder=None, target_sr=22050):
    """
    Preprocesses audio to improve transcription accuracy:
    - Normalizes volume
    - Removes silence
    - Converts to mono
    - Resamples to optimal sample rate
    
    Args:
        input_audio_path: Path to input audio file
        output_folder: Optional folder to save preprocessed audio
        target_sr: Target sample rate (22050 Hz is optimal for basic-pitch)
    
    Returns:
        Path to preprocessed audio file
    """
    print(f"Preprocessing audio: {input_audio_path}")
    
    # Load audio file
    audio, sr = librosa.load(input_audio_path, sr=None, mono=True)
    
    # 1. Normalize volume (prevent clipping, improve consistency)
    audio = librosa.util.normalize(audio)
    
    # 2. Remove leading/trailing silence (reduces processing time)
    audio, _ = librosa.effects.trim(audio, top_db=20)
    
    # 3. Resample to optimal rate for basic-pitch
    if sr != target_sr:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
        sr = target_sr
    
    # 4. Apply gentle noise reduction (optional - can help with noisy recordings)
    # Uncomment if dealing with very noisy audio:
    # audio = reduce_noise(audio, sr)
    
    # Save preprocessed audio
    if output_folder is None:
        output_folder = os.path.dirname(input_audio_path)
    
    base_name = os.path.basename(input_audio_path)
    name_without_ext = os.path.splitext(base_name)[0]
    output_path = os.path.join(output_folder, f"{name_without_ext}_preprocessed.wav")
    
    sf.write(output_path, audio, sr)
    print(f"Preprocessed audio saved: {output_path}")
    
    return output_path


def reduce_noise(audio, sr, noise_duration=0.5):
    """
    Simple noise reduction by estimating noise profile from start of audio.
    
    Args:
        audio: Audio signal
        sr: Sample rate
        noise_duration: Duration in seconds to use for noise estimation
    
    Returns:
        Noise-reduced audio
    """
    # Estimate noise from the first noise_duration seconds
    noise_sample_length = int(sr * noise_duration)
    noise_profile = audio[:noise_sample_length]
    
    # Simple spectral subtraction
    noise_stft = librosa.stft(noise_profile)
    noise_power = np.mean(np.abs(noise_stft) ** 2, axis=1, keepdims=True)
    
    audio_stft = librosa.stft(audio)
    audio_power = np.abs(audio_stft) ** 2
    
    # Subtract noise (with floor to prevent negative values)
    clean_power = np.maximum(audio_power - noise_power, 0.1 * audio_power)
    clean_stft = np.sqrt(clean_power) * np.exp(1j * np.angle(audio_stft))
    
    return librosa.istft(clean_stft)
