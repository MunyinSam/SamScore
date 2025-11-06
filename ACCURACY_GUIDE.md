# Improving Transcription Accuracy in SamScore

This document outlines strategies to improve the accuracy of audio-to-sheet-music transcription.

## 🎯 Quick Wins (Easy to Implement)

### 1. **Audio Quality Matters Most**

-   **Use high-quality recordings** (WAV/FLAC > MP3)
-   **Avoid compressed/lossy formats** when possible
-   **Record at 44.1kHz or higher** sample rate
-   **Minimize background noise** during recording
-   **Use a good microphone** (closer to instrument = better)

### 2. **Optimal Input Characteristics**

The AI works best with:

-   ✅ Solo instruments (piano, guitar, violin)
-   ✅ Clear, isolated recordings
-   ✅ Moderate tempo (not too fast)
-   ✅ Consistent volume/dynamics
-   ❌ Avoid: Dense polyphonic music, heavy reverb, background noise

### 3. **Tune Transcription Parameters**

Adjust these in `transcriber_advanced.py`:

```python
# For QUIET/SOFT recordings:
onset_threshold=0.3  # Lower = more sensitive
frame_threshold=0.2

# For LOUD/AGGRESSIVE recordings:
onset_threshold=0.7  # Higher = less false positives
frame_threshold=0.5

# For FAST passages:
minimum_note_length=60  # Lower = capture shorter notes

# For SLOW/LYRICAL music:
minimum_note_length=200  # Higher = filter out ornaments
```

---

## 🔧 Implementation Strategies

### **Strategy 1: Preprocessing Pipeline**

Add audio cleaning before transcription:

```python
from MuScribe.audio_preprocessor import preprocess_audio
from MuScribe import transcriber_advanced

# Clean audio first
cleaned_audio = preprocess_audio("input_audio/song.mp3")

# Then transcribe with tuned parameters
midi_path = transcriber_advanced.convert_audio_to_midi(
    cleaned_audio,
    "output_sheets",
    onset_threshold=0.5,
    frame_threshold=0.3
)
```

### **Strategy 2: Post-Processing**

Clean up MIDI artifacts:

```python
# After transcription
raw_midi = transcriber_advanced.convert_audio_to_midi(...)

# Clean and quantize
clean_midi = transcriber_advanced.clean_midi(
    raw_midi,
    remove_percussion=True,
    quantize=True,
    merge_tracks=True  # For solo piano
)
```

### **Strategy 3: Multiple Passes**

Run transcription with different parameters and combine results:

```python
# Conservative pass (fewer false positives)
midi_conservative = convert_audio_to_midi(
    audio_path,
    output_folder,
    onset_threshold=0.7,
    frame_threshold=0.5
)

# Aggressive pass (capture quiet notes)
midi_aggressive = convert_audio_to_midi(
    audio_path,
    output_folder,
    onset_threshold=0.3,
    frame_threshold=0.2
)

# Manually compare in MuseScore or merge programmatically
```

---

## 🚀 Advanced Improvements

### **Option 1: Use Different AI Models**

basic-pitch has multiple models:

```python
from basic_pitch import ICASSP_2022_MODEL_PATH  # Default
# Try experimental models if available in future versions
```

### **Option 2: Ensemble Approach**

Use multiple transcription engines and vote:

```python
# 1. basic-pitch (Spotify)
# 2. Omnizart (another open-source AMT)
# 3. MT3 (Google's Music Transformer)

# Combine results for better accuracy
```

### **Option 3: Add Manual Correction UI**

Build a simple interface to:

-   Visualize waveform + transcribed notes side-by-side
-   Allow quick corrections (add/remove/adjust notes)
-   Save corrected versions for training

### **Option 4: Fine-tune the Model**

(Advanced - requires ML knowledge)

-   Collect your own dataset of audio + ground truth MIDI
-   Fine-tune basic-pitch model on your specific instrument/style
-   Requires TensorFlow knowledge and training data

---

## 📊 Parameter Reference

| Parameter             | Range       | Effect                                    | Best For                                       |
| --------------------- | ----------- | ----------------------------------------- | ---------------------------------------------- |
| `onset_threshold`     | 0.0-1.0     | Controls note onset detection sensitivity | 0.3-0.4 for soft music, 0.6-0.7 for loud       |
| `frame_threshold`     | 0.0-1.0     | Controls note sustain detection           | 0.2-0.3 for legato, 0.4-0.5 for staccato       |
| `minimum_note_length` | 0-500ms     | Filters out short notes                   | 60-100ms for fast passages, 150-250ms for slow |
| `minimum_frequency`   | 20-2000Hz   | Removes low frequencies                   | 80Hz to remove bass rumble                     |
| `maximum_frequency`   | 2000-8000Hz | Removes high frequencies                  | 5000Hz to focus on fundamental tones           |

---

## 🎼 Instrument-Specific Tips

### **Piano**

```python
onset_threshold=0.5
frame_threshold=0.3
minimum_note_length=127
melodia_trick=True
merge_tracks=True  # Combine hands
```

### **Guitar**

```python
onset_threshold=0.4  # Capture soft fingerpicking
frame_threshold=0.25
minimum_frequency=80  # Remove low-end rumble
melodia_trick=True
```

### **Violin/Voice (Monophonic)**

```python
onset_threshold=0.4
frame_threshold=0.3
minimum_note_length=150  # Filter vibrato artifacts
melodia_trick=True
```

### **Drums/Percussion**

⚠️ basic-pitch is **not optimized** for drums. Consider:

-   Using dedicated drum transcription tools
-   Manual MIDI programming
-   Or accepting lower accuracy

---

## 🧪 Testing & Evaluation

### Measure Accuracy:

1. **Visual inspection**: Open MIDI in MuseScore and compare to audio
2. **Listen**: Export MIDI to audio and compare with original
3. **Metrics**: Calculate note precision/recall if you have ground truth

### Iterative Tuning:

```python
# Test suite of different parameter combinations
test_configs = [
    {"onset": 0.3, "frame": 0.2, "min_len": 80},
    {"onset": 0.5, "frame": 0.3, "min_len": 127},
    {"onset": 0.7, "frame": 0.5, "min_len": 200},
]

for config in test_configs:
    midi = convert_audio_to_midi(audio, output, **config)
    # Evaluate and pick best
```

---

## 📦 Required Dependencies

Add to `requirements.txt` for advanced features:

```
soundfile>=0.12.0  # For audio I/O
pretty-midi>=0.2.0  # For MIDI post-processing
noisereduce>=2.0.0  # Optional: for noise reduction
```

---

## 🎯 Expected Results

| Audio Quality                | Parameter Tuning       | Expected Accuracy                 |
| ---------------------------- | ---------------------- | --------------------------------- |
| Studio recording, solo piano | Well-tuned             | **85-95%** note accuracy          |
| Home recording, guitar       | Default params         | **70-85%**                        |
| Phone recording, noisy       | Preprocessing + tuning | **60-75%**                        |
| Complex orchestral           | Any settings           | **40-60%** (limitations of model) |

---

## 🔗 Further Reading

-   [basic-pitch documentation](https://github.com/spotify/basic-pitch)
-   [Audio preprocessing best practices](https://librosa.org/doc/latest/tutorial.html)
-   [MIDI quantization algorithms](<https://en.wikipedia.org/wiki/Quantization_(music)>)
-   Academic papers on Automatic Music Transcription (AMT)

---

**Next Steps:**

1. Try the preprocessing pipeline on your audio files
2. Experiment with different parameter combinations
3. Use MIDI cleaning for better sheet music output
4. Consider the advanced strategies if you need even better accuracy
