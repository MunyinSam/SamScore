# 🎵 SamScore# SamScore

An AI that listens to audio files (MP3/WAV) and automatically transcribes them into sheet music (MIDI/MusicXML).

**Automatic Music Transcription: From Audio to Sheet Music**

# MuScribe

SamScore is an AI-powered tool that listens to audio files (MP3/WAV) and automatically transcribes them into professional sheet music (MIDI and PDF formats).(or)

# SamScore

Built with Spotify's [basic-pitch](https://github.com/spotify/basic-pitch) deep learning model and music21, SamScore makes it easy to convert any musical recording into readable notation.

> A deep learning project for Automatic Music Transcription (AMT), converting polyphonic audio into symbolic musical notation (MIDI/MusicXML).

---

**Status:** :construction: In Development

## ✨ Features

This project is an exploration into the field of Automatic Music Transcription. The goal is to build and train a neural network that can listen to a digital audio file (like an MP3 or WAV) and generate an accurate, playable musical score.

-   🎹 **Audio to MIDI Transcription** - Uses Spotify's basic-pitch AI model for accurate polyphonic transcription

-   📄 **MIDI to PDF Conversion** - Generates professional sheet music PDFs using music21This repository documents the entire process, from data processing and model architecture to final inference.

-   🚀 **Simple Command-Line Interface** - Easy to use with a single command

-   🎼 **Supports Multiple Audio Formats** - Works with MP3, WAV, FLAC, and more## 🚀 Getting Started

---These instructions will get you a copy of the project up and running on your local machine for development and testing.

## 🚀 Getting Started### 1. Clone the Repository

### Prerequisites```bash

git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)

-   Python 3.8 or highercd your-repo-name

-   [MuseScore](https://musescore.org/en/download) (required for PDF generation)

# On macOS/Linux

### Installationpython3 -m venv venv

source venv/bin/activate

1. **Clone the repository:**

    ```bash# On Windows

    git clone https://github.com/MunyinSam/SamScore.gitpython -m venv venv

    cd SamScore.\venv\Scripts\activate

    ```

pip install -r requirements.txt 2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Install MuseScore:**
    - Download and install [MuseScore](https://musescore.org/en/download)
    - Make sure it's added to your system PATH

---

## 📖 Usage

### Basic Usage

Place your audio file in the `input_audio/` folder, then run:

```bash
python app.py your_audio_file.mp3
```

### Example

```bash
# Transcribe a piano recording
python app.py test_piano.mp3
```

The script will:

1. ✅ Transcribe your audio to MIDI using AI
2. ✅ Convert the MIDI to a PDF sheet music file
3. ✅ Save both outputs to the `output_sheets/` folder

### Output

After successful transcription, you'll find:

-   `output_sheets/your_audio_file_basic_pitch.mid` - The MIDI file
-   `output_sheets/your_audio_file_basic_pitch.pdf` - The sheet music PDF

---

## 📁 Project Structure

```
SamScore/
├── app.py                  # Main application entry point
├── requirements.txt        # Python dependencies
├── MuScribe/              # Core transcription modules
│   ├── __init__.py
│   ├── transcriber.py     # Audio to MIDI conversion
│   └── formatter.py       # MIDI to PDF conversion
├── input_audio/           # Place your audio files here
└── output_sheets/         # Generated MIDI and PDF files
```

---

## 🛠️ How It Works

1. **Audio Input** - Reads audio files from the `input_audio/` folder
2. **AI Transcription** - Uses Spotify's basic-pitch model to analyze the audio and generate MIDI
3. **Format Conversion** - Converts MIDI to MusicXML and renders as PDF using music21 and MuseScore

---

## 🧪 Technologies Used

-   **[basic-pitch](https://github.com/spotify/basic-pitch)** - Spotify's deep learning model for audio-to-MIDI transcription
-   **[music21](http://web.mit.edu/music21/)** - Python toolkit for computer-aided musicology
-   **[librosa](https://librosa.org/)** - Audio analysis library
-   **[MuseScore](https://musescore.org/)** - Music notation software for PDF rendering

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

-   [Spotify Research](https://research.spotify.com/) - For the amazing basic-pitch model
-   [music21 community](http://web.mit.edu/music21/) - For the comprehensive music notation toolkit

---

## 📧 Contact

**Munyin Sam**

Project Link: [https://github.com/MunyinSam/SamScore](https://github.com/MunyinSam/SamScore)

---

**Made with ❤️ and AI**
