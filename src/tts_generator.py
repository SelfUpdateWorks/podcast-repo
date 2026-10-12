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


# Test 2: voice only with a dummy script (no transcript, no LLM call)
if __name__ == "__main__":
    dummy_script = (
        "Welcome back to the show, where we make hard tech simple. "
        "Today's topic sounds scary: Retrieval-Augmented Generation, or RAG. "
        "Here is the idea. A large language model is like a very smart student "
        "who studied a lot, but a while ago. Ask about your company's latest "
        "policy, and it can only guess. "
        "RAG gives that student an open-book exam. Before answering, the system "
        "searches your own documents, picks the few pages that matter, "
        "and hands them to the model together with your question. "
        "So the answer is based on your facts, not on old memory. "
        "One sentence to remember: RAG means look it up first, then answer. "
        "Thanks for listening, see you next time."
    )
    print("Saved:", generate_audio(dummy_script))
 

# Test from data processor and llm processor, but commented out to avoid calling the LLM and spending money.

#if __name__ == "__main__":
    #from data_processor import read_transcript, clean_text
    #from llm_processor import create_script
 
    #text = clean_text(read_transcript("sample.pdf"))  # any short test file in the repo root
    #script = create_script(text)
   # print(script)  # check the script before listening
    #print("Saved:", generate_audio(script))