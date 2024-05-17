import locale
# from pydub import AudioSegment
import librosa
import librosa.effects
import soundfile as sf
import subprocess

def getpreferredencoding(do_setlocale = True):
    return "UTF-8"
locale.getpreferredencoding = getpreferredencoding

def split_track(project_dir):
    input_file = f"{project_dir}/song.mp3"
    command = ["python3", "-m", "bytesep", "separate", " --source_type", "vocals", "--audio_path", input_file, "--output_path", f"{project_dir}/song/vocals.wav"]
    subprocess.run(command, check=True)
    print(f"Audio separation completed successfully. Output files saved in: {project_dir}")

    vocal_fn = f"{project_dir}/song/vocals.wav"
    bg_fn = f"{project_dir}/song/accompaniment.wav"
    return (vocal_fn, bg_fn)