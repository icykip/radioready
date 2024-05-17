from lyric_replacement import *
from vocal_splitter import *
from lyrics_stt import *
from vocal_tts import *
from merge import *
import sys
import os

def main(project_dir, step):
    print(f"running with project_dir={project_dir}, step={step}")
    if not os.path.exists(f"{project_dir}/clone"):
        os.makedirs(f"{project_dir}/clone")
    if step <= 1:
        vocal_track_fp, background_track_fp = split_track(project_dir)
        print(f"step 1: vocal track filename: {vocal_track_fp}\n\n\n")
    else:
        vocal_track_fp = f"{project_dir}/song/vocals.wav"
        background_track_fp = f"{project_dir}/song/accompaniment.wav"

    lyric_segments = None
    if step <= 2:
        lyric_segments = get_lyrics_from_vocal_track(vocal_track_fp, project_dir)
        print(f"step 2: lyric segments: {lyric_segments}\n\n\n")
    else:
        with open(f"{project_dir}/segments.json") as f:
            lyric_segments = json.load(f)

    if step <= 3:
        lyric_replacements = get_lyric_replacements(lyric_segments, project_dir)
        print(f"step 3: lyric replacements: {lyric_replacements}\n\n\n")
    else:
        lyric_replacements = Replacements.load(f"{project_dir}/replacements.pkl")
    
    if step <= 4:
        clone_replacements(vocal_track_fp, lyric_replacements, project_dir)
        print(f"step 4: cloned replacements: {lyric_replacements}\n\n\n")

    if step <= 5:
        new_vocal_track_fp = merge_replacements_into_vocal_track(vocal_track_fp, lyric_replacements, project_dir)
        print(f"step 5: new vocal track filepath: {new_vocal_track_fp}\n\n\n")
    else:
        new_vocal_track_fp = f"{project_dir}/merged_vocals.wav"

    if step <= 6:
        merged_filepath = merge_tracks(background_track_fp, new_vocal_track_fp, project_dir)
        print(f"step 6: final merged filepath: {merged_filepath}\n\n\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 main.py <project_dir> <step>")
        sys.exit(1)

    project_dir = sys.argv[1]
    step = int(sys.argv[2])

    main(project_dir, step)
