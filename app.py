import argparse
import os
from MuScribe import transcriber, formatter

def main():
    # 1. Set up the command-line interface
    parser = argparse.ArgumentParser(
        description="SAMphony: Transcribe audio to sheet music."
    )
    parser.add_argument(
        "input_file", 
        help="Path to the input audio file (e.g., input_audio/test_piano.mp3)"
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
    
    # Step 1: Transcribe Audio to MIDI
    # The 'transcriber' will save the file to the output folder
    midi_path = transcriber.convert_audio_to_midi(input_path, OUTPUT_FOLDER)
    
    if not midi_path or not os.path.exists(midi_path):
        print("Error: MIDI transcription failed.")
        return
        
    print(f"Successfully created MIDI: {midi_path}")

    # Step 2: Convert MIDI to PDF
    pdf_path = formatter.convert_midi_to_pdf(midi_path, OUTPUT_FOLDER)
    
    if not pdf_path:
        print("Error: PDF conversion failed.")
        return

    print(f"\n✨ Success! ✨")
    print(f"  Input: {input_path}")
    print(f"  MIDI:  {midi_path}")
    print(f"  PDF:   {pdf_path}")


if __name__ == "__main__":
    main()