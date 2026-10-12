# GOAL: turn the podcast script into an mp3 file (Student C)
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # load OPENAI_API_KEY from .env, so this file also runs on its own
client = OpenAI()


# Input: the script (text) from LLM.
# Output: the path to the mp3 file.
def generate_audio(script, path="outputs/recap.mp3"): #path is the default output path, can be changed and or overwritten
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=script,
    )
    response.write_to_file(path)
    return path

# Test from data processor and llm processor, but commented out to avoid calling the LLM and spending money.
if __name__ == "__main__":
    from data_processor import read_transcript, clean_text
    from llm_processor import create_script

    text = clean_text(read_transcript("sample.pdf"))  # any short test file in the repo root
    script = create_script(text)
    print(script)  # check the script before listening
    print("Saved:", generate_audio(script))