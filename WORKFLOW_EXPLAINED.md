# 🎵 SamScore Project Workflow Explained

A complete walkthrough of how SamScore transforms audio into sheet music.

---

## 📋 **Table of Contents**

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [The Pipeline](#the-pipeline)
4. [Step-by-Step Process](#step-by-step-process)
5. [Technical Details](#technical-details)
6. [Data Flow Diagram](#data-flow-diagram)

---

## 🎯 **Overview**

**What SamScore Does:**
Takes an audio file (like MP3/WAV) → Converts it to MIDI → Generates sheet music PDF

**The Magic:**
Uses Spotify's AI model (basic-pitch) to "listen" to music and figure out which notes are being played.

---

## 📁 **Project Structure**

```
SamScore/
│
├── app.py                      # Main entry point (simple version)
├── app_advanced.py             # Enhanced version with tuning options
│
├── MuScribe/                   # Core functionality modules
│   ├── __init__.py            # Makes MuScribe a Python package
│   ├── transcriber.py         # Audio → MIDI conversion
│   ├── transcriber_advanced.py # Enhanced transcriber with parameters
│   ├── formatter.py           # MIDI → PDF conversion
│   └── audio_preprocessor.py  # Audio cleaning/optimization
│
├── input_audio/               # PUT YOUR AUDIO FILES HERE
│   └── test1.mp3             # Example: your input audio
│
├── output_sheets/             # OUTPUTS SAVED HERE
│   ├── test1_basic_pitch.mid         # Generated MIDI file
│   ├── test1_basic_pitch.musicxml    # MusicXML (intermediate format)
│   └── test1_basic_pitch.pdf         # Final sheet music PDF
│
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── ACCURACY_GUIDE.md         # How to improve accuracy
├── QUICK_START.md            # Quick reference commands
└── .venv/                    # Virtual environment (dependencies)
```

---

## 🔄 **The Pipeline**

### **3-Stage Process:**

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   AUDIO     │ ───> │    MIDI     │ ───> │     PDF     │
│  (MP3/WAV)  │      │  (Musical   │      │  (Sheet     │
│             │      │   Notes)    │      │   Music)    │
└─────────────┘      └─────────────┘      └─────────────┘
     INPUT              INTERMEDIATE           OUTPUT
```

**Why 3 stages?**

-   Stage 1: AI extracts notes from sound waves
-   Stage 2: Notes are stored in MIDI (digital music format)
-   Stage 3: MIDI is rendered as readable sheet music

---

## 🔬 **Step-by-Step Process**

### **When you run:** `python app.py test1.mp3`

### **1. Command Line Parsing** (`app.py` - lines 6-16)

```python
parser = argparse.ArgumentParser(...)
parser.add_argument("input_file", ...)
args = parser.parse_args()
```

**What happens:**

-   Python reads your command: `test1.mp3`
-   Validates that you provided a filename
-   Stores it in `args.input_file`

---

### **2. File Path Construction** (`app.py` - lines 18-25)

```python
INPUT_FOLDER = "input_audio"
OUTPUT_FOLDER = "output_sheets"
input_path = os.path.join(INPUT_FOLDER, args.input_file)
```

**What happens:**

-   Builds full path: `input_audio/test1.mp3`
-   Checks if file exists
-   If not found → displays error and exits

---

### **3. Audio → MIDI Transcription** (`transcriber.py`)

#### **a) Load Audio & AI Model**

```python
predict_and_save(
    audio_path_list=[input_audio_path],
    model_or_model_path=ICASSP_2022_MODEL_PATH,
    ...
)
```

**What happens internally:**

1. **Load audio file:**

    - Reads MP3/WAV file
    - Converts to raw audio waveform (amplitude over time)
    - Resamples to 22050 Hz (optimal for AI model)

2. **Convert to spectrogram:**

    - Audio waveform → Frequency spectrum over time
    - Like a visual "fingerprint" of the sound
    - Shows which frequencies are present at each moment

3. **Run AI Model (basic-pitch):**

    - Deep neural network trained on thousands of audio + MIDI pairs
    - Looks at spectrogram patterns
    - Predicts: "Which notes are playing?" and "When do they start/stop?"
    - Outputs note probabilities for each pitch (C, C#, D, etc.)

4. **Post-processing:**

    - Converts probabilities to actual notes
    - Filters out weak detections (threshold)
    - Groups notes into chords (polyphonic detection)
    - Estimates note timing and duration

5. **Save MIDI file:**
    - Writes detected notes to MIDI format
    - File: `output_sheets/test1_basic_pitch.mid`

**Output:** `test1_basic_pitch.mid` (MIDI file with note data)

---

### **4. MIDI → PDF Conversion** (`formatter.py`)

#### **a) Parse MIDI**

```python
score = m21.converter.parse(midi_file_path)
```

**What happens:**

-   music21 library reads the MIDI file
-   Converts note data into a "Score" object
-   Score contains:
    -   Notes (pitch, duration, timing)
    -   Time signature (4/4, 3/4, etc.)
    -   Key signature (C major, G minor, etc.)
    -   Tempo information

#### **b) Render Sheet Music**

```python
score.write('musicxml.pdf', fp=pdf_file_path)
```

**What happens internally:**

1. **Convert to MusicXML:**

    - music21 converts Score → MusicXML format
    - MusicXML: Standard format for sheet music notation
    - Includes staff, clefs, time signatures, etc.

2. **Call MuseScore (External Program):**

    - music21 launches MuseScore in background
    - MuseScore reads MusicXML
    - Renders professional-looking sheet music
    - Exports to PDF

3. **Save PDF:**
    - File: `output_sheets/test1_basic_pitch.pdf`

**Output:** `test1_basic_pitch.pdf` (Sheet music PDF)

---

### **5. Success Message** (`app.py` - lines 46-49)

```python
print(f"\n✨ Success! ✨")
print(f"  Input: {input_path}")
print(f"  MIDI:  {midi_path}")
print(f"  PDF:   {pdf_path}")
```

---

## 🧠 **Technical Details**

### **Key Technologies:**

#### **1. basic-pitch (Spotify's AI Model)**

-   **Type:** Deep Convolutional Neural Network (CNN)
-   **Training:** Trained on ~10,000 audio clips with ground-truth MIDI
-   **Input:** Audio spectrogram (time-frequency representation)
-   **Output:** Note probabilities for 88 piano keys + timing
-   **Accuracy:** ~85% for solo instruments, ~60% for complex music

#### **2. librosa (Audio Processing)**

-   Loads audio files
-   Converts to spectrograms
-   Resamples and preprocesses audio
-   Used by basic-pitch internally

#### **3. music21 (Music Notation)**

-   Parses MIDI files
-   Understands music theory (scales, chords, etc.)
-   Converts between formats (MIDI → MusicXML → PDF)
-   Interfaces with MuseScore

#### **4. MuseScore (PDF Rendering)**

-   Professional music notation software
-   Renders MusicXML as beautiful sheet music
-   Called by music21 in the background

---

## 📊 **Data Flow Diagram**

### **Visual Workflow:**

```
┌─────────────────────────────────────────────────────────┐
│  USER INPUT: python app.py test1.mp3                    │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  app.py: Parse command & validate file                  │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  transcriber.py: convert_audio_to_midi()                │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 1. Load audio: test1.mp3 → waveform array       │   │
│  │ 2. Create spectrogram: waveform → frequencies   │   │
│  │ 3. AI inference: spectrogram → note predictions │   │
│  │ 4. Post-process: predictions → clean MIDI data  │   │
│  │ 5. Save: test1_basic_pitch.mid                  │   │
│  └─────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  formatter.py: convert_midi_to_pdf()                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 1. Parse MIDI: Load test1_basic_pitch.mid       │   │
│  │ 2. Build Score: MIDI → music21 Score object     │   │
│  │ 3. Convert: Score → MusicXML format             │   │
│  │ 4. Render: MuseScore → PDF (external program)   │   │
│  │ 5. Save: test1_basic_pitch.pdf                  │   │
│  └─────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  OUTPUT FILES:                                          │
│  • output_sheets/test1_basic_pitch.mid (MIDI)          │
│  • output_sheets/test1_basic_pitch.musicxml (XML)      │
│  • output_sheets/test1_basic_pitch.pdf (Sheet Music)   │
└─────────────────────────────────────────────────────────┘
```

---

## 🎼 **What Each File Format Means:**

### **MP3/WAV (Input)**

-   Raw audio: Sound waves as amplitude over time
-   Like a recording of someone playing
-   No note information

### **MIDI (Intermediate)**

-   Musical Instrument Digital Interface
-   Digital representation of notes
-   Contains: pitch, start time, duration, velocity
-   Like a piano roll or sheet music but in code
-   Small file size (~10KB)

### **MusicXML (Intermediate)**

-   Standard format for sheet music notation
-   XML text file with music symbols
-   Contains: notes, staff, clefs, time signatures
-   Can be opened in any notation software

### **PDF (Output)**

-   Visual sheet music you can read and print
-   Human-readable notation
-   Can't be edited easily (final output)

---

## ⚙️ **Advanced Workflow (app_advanced.py)**

For better accuracy, you can use:

```bash
python app_advanced.py test1.mp3 --preprocess --clean-midi
```

### **Enhanced Pipeline:**

```
AUDIO → [Preprocessing] → MIDI → [Cleaning] → PDF
         ↓                         ↓
    • Normalize volume        • Quantize notes
    • Remove silence          • Remove artifacts
    • Reduce noise            • Merge tracks
```

**Additional Steps:**

1. **Audio Preprocessing** (`audio_preprocessor.py`):

    - Clean up noisy recordings
    - Normalize volume levels
    - Optimize for AI model

2. **MIDI Post-Processing** (`transcriber_advanced.py`):
    - Quantize notes to grid (fix timing)
    - Remove percussion artifacts
    - Filter out very short notes

---

## 🔧 **Configuration & Tuning**

### **Key Parameters (app_advanced.py):**

```python
onset_threshold=0.5      # How sensitive to detect new notes
frame_threshold=0.3      # How long notes should sustain
minimum_note_length=127  # Filter out very short notes (ms)
```

**Think of it like camera settings:**

-   `onset_threshold`: Shutter speed (capture fast vs slow)
-   `frame_threshold`: Aperture (bright vs dark notes)
-   `minimum_note_length`: Noise reduction (filter out artifacts)

---

## 🚨 **Common Issues & Solutions**

### **Problem: "MIDI transcription failed"**

**Cause:** Audio file doesn't exist or is corrupted
**Solution:** Check file is in `input_audio/` folder

### **Problem: "PDF conversion failed"**

**Cause:** MuseScore not installed or not in PATH
**Solution:** Install MuseScore and add to system PATH

### **Problem: "Too many wrong notes"**

**Cause:** AI model confused by complex music
**Solution:**

-   Use higher quality audio
-   Try `--onset-threshold 0.7` (less sensitive)
-   Use `--preprocess` flag

### **Problem: "Missing notes"**

**Cause:** Threshold too high, quiet notes ignored
**Solution:**

-   Try `--onset-threshold 0.3` (more sensitive)
-   Use `--preprocess` to normalize volume

---

## 💡 **Key Takeaways**

1. **SamScore is a pipeline:** Audio → MIDI → PDF
2. **The AI model (basic-pitch) does the hard work:** Listening and figuring out notes
3. **music21 handles notation:** Converting digital notes to sheet music
4. **MuseScore renders the PDF:** Making it look professional
5. **You can tune parameters:** Adjust for different music types
6. **Quality matters:** Better input audio = better output

---

## 🔗 **Further Learning**

-   **Audio Processing:** How sound waves become spectrograms
-   **Deep Learning:** How neural networks learn to transcribe music
-   **Music Theory:** Understanding MIDI, time signatures, key signatures
-   **Digital Signal Processing:** Fourier transforms, frequency analysis

---

**Questions?** Check out:

-   `ACCURACY_GUIDE.md` - How to improve results
-   `QUICK_START.md` - Quick command reference
-   `README.md` - Project overview

---

**Created with ❤️ by Munyin Sam**
