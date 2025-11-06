# Quick Start: Improving Accuracy

## 🚀 Basic Usage (Current App)

```bash
python app.py test1.mp3
```

## ⚡ Advanced Usage (Better Accuracy)

### 1. **With Audio Preprocessing** (Recommended for noisy recordings)

```bash
python app_advanced.py test1.mp3 --preprocess
```

### 2. **For Quiet/Soft Music** (Classical, Jazz ballads)

```bash
python app_advanced.py quiet_song.mp3 --onset-threshold 0.3 --frame-threshold 0.2
```

### 3. **For Loud/Aggressive Music** (Rock, Heavy metal)

```bash
python app_advanced.py rock_song.mp3 --onset-threshold 0.7 --frame-threshold 0.5
```

### 4. **For Fast Music** (Capture quick notes)

```bash
python app_advanced.py fast_passage.mp3 --min-note-length 60
```

### 5. **Full Pipeline** (All improvements)

```bash
python app_advanced.py song.mp3 --preprocess --clean-midi --onset-threshold 0.4 --frame-threshold 0.3
```

### 6. **MIDI Only** (Skip PDF generation)

```bash
python app_advanced.py song.mp3 --no-pdf
```

---

## 📊 Parameter Quick Reference

| Music Type    | onset-threshold | frame-threshold | min-note-length |
| ------------- | --------------- | --------------- | --------------- |
| Soft/Quiet    | 0.3             | 0.2             | 100             |
| Normal        | 0.5 (default)   | 0.3 (default)   | 127 (default)   |
| Loud          | 0.7             | 0.5             | 150             |
| Fast passages | 0.4             | 0.3             | 60              |
| Slow/Lyrical  | 0.5             | 0.3             | 200             |

---

## 🎯 Which Settings to Use?

### **Piano (Solo)**

```bash
python app_advanced.py piano.mp3 --preprocess --clean-midi --onset-threshold 0.5
```

### **Guitar (Fingerstyle)**

```bash
python app_advanced.py guitar.mp3 --onset-threshold 0.4 --frame-threshold 0.25 --preprocess
```

### **Violin/Voice (Monophonic)**

```bash
python app_advanced.py violin.mp3 --onset-threshold 0.4 --min-note-length 150 --preprocess
```

### **Noisy Phone Recording**

```bash
python app_advanced.py phone_recording.mp3 --preprocess --clean-midi --onset-threshold 0.6
```

---

## 🔧 Installation

If using the advanced features, install additional dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install soundfile pretty-midi
```

---

## 💡 Tips for Best Results

1. **Start with high-quality audio** - Use WAV/FLAC instead of MP3 when possible
2. **Record in a quiet environment** - Minimize background noise
3. **Use solo instruments** - The AI works best with single instruments
4. **Experiment with parameters** - Try different thresholds for your specific audio
5. **Use preprocessing for noisy recordings** - The `--preprocess` flag can dramatically improve results
6. **Clean MIDI files** - The `--clean-midi` flag quantizes notes and removes artifacts

---

## 📖 For More Details

See **ACCURACY_GUIDE.md** for:

-   In-depth parameter explanations
-   Instrument-specific configurations
-   Advanced post-processing techniques
-   Manual fine-tuning strategies

---

## 🐛 Troubleshooting

**"Error: MIDI transcription failed"**

-   Check that your audio file exists in `input_audio/` folder
-   Try with `--preprocess` flag
-   Verify audio file is not corrupted

**"PDF conversion failed"**

-   Install MuseScore: https://musescore.org/en/download
-   Make sure MuseScore is added to your system PATH
-   Or use `--no-pdf` to skip PDF generation

**"Too many false notes detected"**

-   Increase `--onset-threshold` (try 0.6 or 0.7)
-   Use `--clean-midi` to filter artifacts
-   Increase `--min-note-length` to filter out very short notes

**"Missing notes in transcription"**

-   Decrease `--onset-threshold` (try 0.3 or 0.4)
-   Decrease `--frame-threshold` (try 0.2)
-   Use `--preprocess` to normalize volume
