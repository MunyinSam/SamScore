from basic_pitch.inference import predict_and_save, predict
from basic_pitch import ICASSP_2022_MODEL_PATH
import os
import pretty_midi


def convert_audio_to_midi(input_audio_path, output_folder, 
                          onset_threshold=0.5, 
                          frame_threshold=0.3,
                          minimum_note_length=127.70,
                          minimum_frequency=None,
                          maximum_frequency=None,
                          melodia_trick=True):
    """
    Takes an audio file and uses basic-pitch to transcribe it.
    Saves the output as a MIDI file in the specified folder.
    
    Args:
        input_audio_path: Path to input audio file
        output_folder: Output directory for MIDI file
        onset_threshold: Threshold for note onset detection (0.0-1.0, default 0.5)
                        Lower = more notes detected (may include false positives)
                        Higher = fewer notes (may miss quiet notes)
        frame_threshold: Threshold for note frame detection (0.0-1.0, default 0.3)
                        Controls note duration accuracy
        minimum_note_length: Minimum note length in milliseconds (default 127.70)
                            Higher = filters out very short notes
        minimum_frequency: Minimum frequency in Hz (default None = no filter)
                          Set to filter out bass if transcribing treble only
        maximum_frequency: Maximum frequency in Hz (default None = no filter)
                          Set to filter out high frequencies if needed
        melodia_trick: Use melodia algorithm trick for better pitch tracking (default True)
    
    Returns:
        Path to generated MIDI file
    """
    
    print(f"Starting transcription for: {input_audio_path}")
    print(f"Settings: onset={onset_threshold}, frame={frame_threshold}, min_note_len={minimum_note_length}ms")
    
    predict_and_save(
        audio_path_list=[input_audio_path],
        output_directory=output_folder,
        save_midi=True,
        sonify_midi=False,
        save_model_outputs=False,
        save_notes=False,
        model_or_model_path=ICASSP_2022_MODEL_PATH,
        onset_threshold=onset_threshold,
        frame_threshold=frame_threshold,
        minimum_note_length=minimum_note_length,
        minimum_frequency=minimum_frequency,
        maximum_frequency=maximum_frequency,
        melodia_trick=melodia_trick
    )
    
    print(f"Transcription finished. MIDI saved in: {output_folder}")
    
    # Helper to return the *exact* path of the new MIDI file
    base_name = os.path.basename(input_audio_path)
    name_without_ext = os.path.splitext(base_name)[0]
    midi_file_name = f"{name_without_ext}_basic_pitch.mid"
    midi_file_path = os.path.join(output_folder, midi_file_name)
    
    return midi_file_path


def clean_midi(midi_file_path, 
               remove_percussion=True,
               quantize=True,
               merge_tracks=False):
    """
    Post-process MIDI file to clean up transcription artifacts.
    
    Args:
        midi_file_path: Path to MIDI file
        remove_percussion: Remove percussion channel (often contains artifacts)
        quantize: Snap notes to grid (improves readability)
        merge_tracks: Merge all tracks into one (useful for piano)
    
    Returns:
        Path to cleaned MIDI file
    """
    print(f"Cleaning MIDI file: {midi_file_path}")
    
    # Load MIDI file
    midi = pretty_midi.PrettyMIDI(midi_file_path)
    
    # Remove percussion tracks (channel 9/10)
    if remove_percussion:
        midi.instruments = [inst for inst in midi.instruments if not inst.is_drum]
    
    # Quantize notes to 16th note grid
    if quantize:
        for instrument in midi.instruments:
            for note in instrument.notes:
                # Snap to nearest 16th note (0.125 seconds at 120 BPM)
                grid = 0.125
                note.start = round(note.start / grid) * grid
                note.end = round(note.end / grid) * grid
                
                # Ensure minimum note length
                if note.end - note.start < 0.05:
                    note.end = note.start + 0.05
    
    # Merge tracks if requested
    if merge_tracks and len(midi.instruments) > 1:
        merged_instrument = pretty_midi.Instrument(program=0, name="Merged")
        for instrument in midi.instruments:
            merged_instrument.notes.extend(instrument.notes)
        midi.instruments = [merged_instrument]
    
    # Save cleaned MIDI
    base_name = os.path.basename(midi_file_path)
    name_without_ext = os.path.splitext(base_name)[0]
    output_path = midi_file_path.replace(".mid", "_cleaned.mid")
    
    midi.write(output_path)
    print(f"Cleaned MIDI saved: {output_path}")
    
    return output_path
