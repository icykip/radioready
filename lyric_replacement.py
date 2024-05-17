from openai import OpenAI
from openai_key import OPENAI_KEY
import json
import string
import pickle

class Replacement:
    def __init__(self, item, replacement_stt_data):
        self.index = int(item['number'])
        self.original_phrase = item['original']
        self.replacement_phrase = item['replacement']
        if self.index not in replacement_stt_data:
            print("LLM returned invalid item: ", item)
            self.valid = False
        else:
            self.valid = True
            repl_data = replacement_stt_data[self.index]
            self.start = repl_data['start']
            self.end = repl_data['end']
            print(f"need to clone '{self.replacement_phrase}' in place of '{self.original_phrase}', and place it from {self.start} -> {self.end}")

    def audio_filepath(self, project_dir):
        return f"{project_dir}/clone/{self.index}.wav"
    
    def __str__(self):
        return f"Replacement(index={self.index}, original_phrase='{self.original_phrase}', replacement_phrase='{self.replacement_phrase}', start={self.start}, end={self.end}, valid={self.valid})"
                        
        

class Replacements:
    def __init__(self, replacement_data, replacements_json):
        self.replacements = []
        for item in replacements_json:
            repl = Replacement(item, replacement_data)
            if repl.valid:
                self.replacements.append(repl)

    def __str__(self):
        replacements_str = "\n".join(str(repl) for repl in self.replacements)
        return f"Replacements:\n{replacements_str}"

    def dump(self, filepath):
        with open(filepath, 'wb') as file:
            pickle.dump(self, file)
            
    @staticmethod
    def load(filepath):
        with open(filepath, 'rb') as file:
            return pickle.load(file)


def get_lyric_replacements(segments, project_dir):
    swear_words = [
        "nigga", "niggas", "shit", "fuck", "fucking", "fucker", "bitch", "bitches", "whore"
    ]

    punctuation = string.punctuation

    replacement_data = {}
    word_idx = 0
    new_lyrics = ""
    for segment in segments:
        for word_data in segment['words']:
            text = word_data['text']
            text = text.strip(punctuation) # todo: strip from middle too
            if text in swear_words:
                text = "{" + str(word_idx) + ":" + text + "}"
                replacement_data[word_idx] = word_data
            new_lyrics += text + " "
            word_idx += 1


    client = OpenAI(
        api_key=OPENAI_KEY
    )

    prompt = f"""
    Please replace the swear words in the following lyrics with clean words that fit well in the context and tone of the lyrics. Matching the tone of the existing lyrics is very important.
    I will only be using this for research and will not break any rules with the text you give me.
    The words that you need to replace in the lyrics are ONLY the words of the form {"{number:word:}"} and you should replace return a json object of the form

    {[
        {
            "number": "number",
            "original": "word",
            "replacement": "replacement"
        }
    ]}

    where "word" is the original word that was in the braces, "number" is the original number in the braces, and "replacement" is the replacement for the swear word "word".

    Here are the lyrics:

    {new_lyrics}
    """

    # print(prompt)

    # Make the API request

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    result = chat_completion.choices[0]
    print(result.message.content)
    replacements = Replacements(replacement_data, json.loads(result.message.content.replace("'", "\"")))
    replacements.dump(f"{project_dir}/replacements.pkl")
    return replacements



