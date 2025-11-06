import argparse
import os
from MuScribe import formatter
from MuScribe.transcriber_advanced import convert_audio_to_midi, clean_midi
from MuScribe.audio_preprocessor import preprocess_audio


def main():
    # 1. Set up the command-line interface with advanced options
    parser = argparse.ArgumentParser(
        description="SamScore: Transcribe audio to sheet music with accuracy controls."
    )
    parser.add_argument(
        "input_file", 
        help="Path to the input audio file (e.g., input_audio/test_piano.mp3)"
    )
    parser.add_argument(
        "--preprocess", 
        action="store_true",
        help="Apply audio preprocessing (normalize, trim silence, reduce noise)"
    )
    parser.add_argument(
        "--onset-threshold",
        type=float,
        default=0.5,
        help="Note onset detection threshold (0.0-1.0, default 0.5). Lower = more notes detected"
    )
    parser.add_argument(
        "--frame-threshold",
        type=float,
        default=0.3,
        help="Note frame detection threshold (0.0-1.0, default 0.3). Lower = longer note durations"
    )
    parser.add_argument(
        "--min-note-length",
        type=float,
        default=127.70,
        help="Minimum note length in milliseconds (default 127.70). Higher = filter out short notes"
    )
    parser.add_argument(
        "--clean-midi",
        action="store_true",
        help="Apply MIDI post-processing (quantize, remove artifacts)"
    )
    parser.add_argument(
        "--no-pdf",
        action="store_true",
        help="Skip PDF generation (only output MIDI)"
    )
    
    args = parser.parse_args()
    
    # 2. Define our input and output folders
    INPUT_FOLDER = "input_audio"
    OUTPUT_FOLDER = "output_sheets"
    
    # Create the full path to the input file
    input_path = os.path.join(INPUT_FOLDER, args.input_file)
    
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at: {input_path}")
        return

    # 3. --- The Pipeline ---
    
    # Step 0: Optional preprocessing
    audio_to_transcribe = input_path
    if args.preprocess:
        print("\n=== Step 0: Preprocessing Audio ===")
        audio_to_transcribe = preprocess_audio(input_path, OUTPUT_FOLDER)
    
    # Step 1: Transcribe Audio to MIDI with tuned parameters
    print("\n=== Step 1: Transcribing Audio to MIDI ===")
    midi_path = convert_audio_to_midi(
        audio_to_transcribe, 
        OUTPUT_FOLDER,
        onset_threshold=args.onset_threshold,
        frame_threshold=args.frame_threshold,
        minimum_note_length=args.min_note_length
    )
    
    if not midi_path or not os.path.exists(midi_path):
        print("Error: MIDI transcription failed.")
        return
        
    print(f"✓ Successfully created MIDI: {midi_path}")
    
    # Step 1.5: Optional MIDI cleaning
    if args.clean_midi:
        print("\n=== Step 1.5: Cleaning MIDI ===")
        midi_path = clean_midi(midi_path, quantize=True, remove_percussion=True)
        print(f"✓ Cleaned MIDI: {midi_path}")

    # Step 2: Convert MIDI to PDF
    if not args.no_pdf:
        print("\n=== Step 2: Converting MIDI to PDF ===")
        pdf_path = formatter.convert_midi_to_pdf(midi_path, OUTPUT_FOLDER)
        
        if not pdf_path:
            print("⚠ Warning: PDF conversion failed. Is MuseScore installed and in PATH?")
            print(f"You can still use the MIDI file: {midi_path}")
        else:
            print(f"✓ Successfully created PDF: {pdf_path}")

    # Final summary
    print(f"\n{'='*60}")
    print(f"✨ Transcription Complete! ✨")
    print(f"{'='*60}")
    print(f"  Input:  {input_path}")
    print(f"  MIDI:   {midi_path}")
    if not args.no_pdf and pdf_path:
        print(f"  PDF:    {pdf_path}")
    print(f"{'='*60}")
    print("\nTips for better accuracy:")
    print("  • Use --preprocess for noisy recordings")
    print("  • Adjust --onset-threshold (0.3-0.7) for sensitivity")
    print("  • Use --clean-midi to quantize and remove artifacts")
    print(f"  • See ACCURACY_GUIDE.md for detailed tuning tips")


if __name__ == "__main__":
    main()
