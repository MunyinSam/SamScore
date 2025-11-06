from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH
import os

def convert_audio_to_midi(input_audio_path, output_folder):
    """
    Takes an audio file and uses basic-pitch to transcribe it.
    Saves the output as a MIDI file in the specified folder.
    """
    
    # predict_and_save will:
    # 1. Load the audio
    # 2. Run the AI model
    # 3. Save the MIDI, MIDI notes, and a sonified version
    
    print(f"Starting transcription for: {input_audio_path}")
    
    predict_and_save(
        audio_path_list=[input_audio_path],
        output_directory=output_folder,
        save_midi=True,
        sonify_midi=False,
        save_model_outputs=False,
        save_notes=False,
        model_or_model_path=ICASSP_2022_MODEL_PATH
    )
    
    print(f"Transcription finished. MIDI saved in: {output_folder}")
    
    # Helper to return the *exact* path of the new MIDI file
    base_name = os.path.basename(input_audio_path)
    name_without_ext = os.path.splitext(base_name)[0]
    midi_file_name = f"{name_without_ext}_basic_pitch.mid"
    midi_file_path = os.path.join(output_folder, midi_file_name)
    
    return midi_file_path