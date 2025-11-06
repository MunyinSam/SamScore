import music21 as m21
import os

def convert_midi_to_pdf(midi_file_path, output_folder):
    """
    Takes a MIDI file and converts it into a PDF sheet music file.
    Saves the PDF in the specified folder.
    """
    
    print(f"Converting MIDI to PDF: {midi_file_path}")
    
    try:
        # Load the MIDI file
        score = m21.converter.parse(midi_file_path)
        
        # Get the base name for the output file
        base_name = os.path.basename(midi_file_path)
        name_without_ext = os.path.splitext(base_name)[0]
        pdf_file_name = f"{name_without_ext}.pdf"
        pdf_file_path = os.path.join(output_folder, pdf_file_name)
        
        # Save as PDF
        # This requires MuseScore or LilyPond to be installed!
        score.write('musicxml.pdf', fp=pdf_file_path)
        
        print(f"PDF saved: {pdf_file_path}")
        return pdf_file_path
        
    except Exception as e:
        print(f"Error converting MIDI to PDF. Is MuseScore installed?")
        print(f"Error: {e}")
        return None