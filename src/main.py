"""
main.py
Job: connect the three steps into a Gradio web app.
The user pastes a link OR uploads a PDF -> 3 plain-language takeaways + audio.
"""

import time
from functools import lru_cache

import gradio as gr

from data_processor import load_transcript
from llm_processor import create_script
from tts_generator import generate_audio


@lru_cache(maxsize=10)
def get_article(source):
    """Load + clean an article. Cached, so clicking again on the same
    article does not download or read it a second time."""
    return load_transcript(source)


def summarize(url, pdf_file):
    """Runs on every click."""
    # 1. Decide which source to use: an uploaded PDF wins over a link
    if pdf_file:
        source = pdf_file
    elif url and url.strip():
        source = url.strip()
    else:
        raise gr.Error("Please paste a link or upload a PDF first.")

    # 2. Read the article (show a friendly message if it fails)
    try:
        text = get_article(source)
    except Exception as e:
        raise gr.Error(f"Sorry, I could not read this article: {e}")

    if len(text) < 200:
        raise gr.Error("I found almost no text. Is it a scanned PDF or a page that needs a login?")

    # 3. Takeaways + audio (same as the MVP)
    script = create_script(text)
    audio_path = generate_audio(script, path=f"outputs/takeaways_{int(time.time())}.mp3")
    return script, audio_path

    script = create_script(text)
    if script.strip() == "UNREADABLE":
        raise gr.Error("This doesn't look like a readable article. Try uploading the PDF instead.")


with gr.Blocks(title="Science in Plain Words") as demo:
    gr.Markdown("# Science in Plain Words\n"
                "Paste a link to a scientific article **or** upload a PDF, "
                "then click the button to get 3 easy takeaways.")

    with gr.Row():
        url_box = gr.Textbox(label="Article link",
                             placeholder="https://arxiv.org/abs/2601.15195")
        pdf_box = gr.File(label="…or upload a PDF", file_types=[".pdf"], type="filepath")

    button = gr.Button("Summarize", variant="primary")
    takeaways = gr.Textbox(label="Key takeaways", lines=12)
    audio = gr.Audio(label="Listen", type="filepath")

    button.click(fn=summarize, inputs=[url_box, pdf_box], outputs=[takeaways, audio])

demo.launch()