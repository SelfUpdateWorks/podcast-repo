"""
main.py
Job: connect the three steps into a Gradio web app.
Article -> load_transcript -> create_script -> generate_audio -> show text + audio
"""

import time

import gradio as gr

from data_processor import load_transcript
from llm_processor import create_script
from tts_generator import generate_audio

# MVP: one fixed article (a link or a PDF path). Later, the user will upload their own.
ARTICLE_SOURCE = "https://arxiv.org/abs/2601.15195"

# Load and clean the article ONCE when the app starts, not on every click
print("Loading article...")
ARTICLE_TEXT = load_transcript(ARTICLE_SOURCE)
print(f"Article loaded: {len(ARTICLE_TEXT)} characters")


def summarize():
    """Runs on every click: 3 new takeaways + their audio."""
    script = create_script(ARTICLE_TEXT)
    audio_path = generate_audio(script, path=f"outputs/takeaways_{int(time.time())}.mp3")
    return script, audio_path


with gr.Blocks(title="Science in Plain Words") as demo:
    gr.Markdown("# Science in Plain Words\nClick the button to get 3 easy takeaways from the article.")
    button = gr.Button("Summarize", variant="primary")
    takeaways = gr.Textbox(label="Key takeaways", lines=12)
    audio = gr.Audio(label="Listen", type="filepath")

    button.click(fn=summarize, inputs=None, outputs=[takeaways, audio])

demo.launch()