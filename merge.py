import whisper_timestamped as whisper
import soundfile as sf
import librosa
from pydub import AudioSegment

def merge_replacements_into_vocal_track(original_vocal_filepath, replacements, project_dir):
    # sample_rate_original = librosa.get_samplerate(original_vocal_filepath) #41000# librosa.get_samplerate("snoop.mp3")
    orig_audio, sample_rate_original = librosa.load(original_vocal_filepath)
    print("original audio", orig_audio)
    print("Sample rate orig:", sample_rate_original)
    for r in replacements.replacements:
        print(r)
        repl_filepath = r.audio_filepath(project_dir)
        # repl_audio = whisper.load_audio(repl_filepath)
        repl_audio, sample_rate_replacement = librosa.load(repl_filepath)
        print(repl_audio)
        print("Sample rate repl:", sample_rate_replacement)


        resampled_repl_audio = repl_audio #librosa.resample(repl_audio, orig_sr=sample_rate_replacement, target_sr=sample_rate_original)

        # # change audio to the right length
        desired_length_seconds = r.end - r.start
        # stretched_audio = librosa.effects.time_stretch(resampled_repl_audio, rate=len(resampled_repl_audio) / (desired_length_seconds * sample_rate_original))
        stretched_audio = resampled_repl_audio # todo

        insertion_position_seconds = r.start  # Specify the insertion position in seconds
        insertion_position_samples = int(insertion_position_seconds * sample_rate_original)

        print(len(repl_audio))
        print(len(orig_audio))
        print(len(stretched_audio))
        print(insertion_position_samples)

        if insertion_position_samples > len(orig_audio):
            continue

        # Create a new audio array with the appropriate length
        orig_audio[insertion_position_samples : insertion_position_samples + len(stretched_audio)] = stretched_audio

        # Copy the background audio into the new array
        # combined_audio[:len(background_audio)] = background_audio

        # # Insert the squished audio at the specified position


        # combined_audio[insertion_position_samples:insertion_position_samples + len(stretched_audio)] = stretched_audio
    new_vocal_filepath = f"{project_dir}/merged_vocals.wav"
    sf.write(new_vocal_filepath, orig_audio, sample_rate_original)
        # todo
    return new_vocal_filepath

def merge_tracks(bg_filepath, vocal_filepath, project_dir):
    bg = AudioSegment.from_wav(bg_filepath)
    vox = AudioSegment.from_wav(vocal_filepath)
    combined = bg.overlay(vox)
    combined_fp = f"{project_dir}/final.wav"
    combined.export(combined_fp, format="wav")
    return combined_fp
    # todo
    