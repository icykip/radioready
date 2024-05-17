import whisper_timestamped as whisper
import json

def get_lyrics_from_vocal_track(vocal_track_filename, project_dir):
    vocal_audio = whisper.load_audio(vocal_track_filename)
    model = whisper.load_model("small", device="cpu")
    timestamped_transcription = whisper.transcribe(model, vocal_audio, language="en")
    # Print Results
    segments = timestamped_transcription['segments']
    json_str = json.dumps(segments, indent = 2, ensure_ascii = False)
    with open(f"{project_dir}/segments.json", "w") as f:
        f.write(json_str)

    return segments