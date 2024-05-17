import torch
import os
import requests
from TTS.api import TTS
from pathlib import Path
# from lyric_replacements import *

DEFAULT_MODEL="tts_models/multilingual/multi-dataset/xtts_v2"

class VoiceCloner:
    def __init__(self, vocal_filename, model_name=DEFAULT_MODEL):
        tts_home_dir = "/home/Elliot/tts_home"
        # %env TTS_HOME={tts_home_dir}
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        self.speaker_wav = vocal_filename
        if not vocal_filename.endswith(".wav"):
            print("file must be a wav file.")
            exit(1)

    def list_models():
        print(TTS().list_models().list_models())

    def clone_phrase(self, phrase, output_file):
        self.tts.tts_to_file(text=phrase, speaker_wav=self.speaker_wav, language="en", file_path=output_file)


def clone_replacements(vocal_filename, replacements, project_dir):
    cloner = VoiceCloner(vocal_filename)
    for r in replacements.replacements:
        phrase = r.replacement_phrase
        cloner.clone_phrase(phrase, r.audio_filepath(project_dir))