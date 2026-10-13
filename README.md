# Science in Plain Words

Turn a scientific article into **3 plain-language takeaways** and a short **audio podcast**,
in **8 languages** and a **serious or funny tone**.

Paste a link or upload a PDF, choose a language and a tone, click **Summarize**, then read
and listen. Click again for a different angle on the same article.

Built for curious people with no science background who want to understand research
without the jargon.

## Features

- **Input:** a link (works best with open-access sources such as arXiv) or an uploaded PDF
- **Output:** a short opening with the article title (and its date, and whether it is a preprint, when the text says so), then 3 takeaways in everyday words, plus an mp3
- **Languages:** English, Turkish, German, French, Spanish, Italian, Chinese, Hindi
- **Tone:** Serious (like a science journalist) or Funny (playful comparisons, facts unchanged)
- **New angle on every click:** main findings, everyday impact, surprises, how the study was done, or its limits
- **Accuracy rules in the prompt:** only facts from the article, the strength of each claim kept, no guessed dates

## How it works

```
PDF or link ──► data_processor.py ──► llm_processor.py ──► tts_generator.py ──► 🎧 .mp3
                 load + clean text     title + 3 takeaways   text-to-speech
                                       (language, tone)
                                  ▲
                          main.py (Gradio app) connects all the steps
```

| File | Job | Main function | Owner |
|---|---|---|---|
| `src/data_processor.py` | Load text from a PDF, a link or a .txt file and clean it (drops title block, references, page numbers, broken lines) | `load_transcript(source)` | Student B, Barsha |
| `src/llm_processor.py` | Send the clean text (first 30,000 characters) to the LLM and get back a spoken-style summary in the chosen language and tone, with a random angle on each click | `create_script(text, language, tone)` | Student A, Elif |
| `src/tts_generator.py` | Turn the summary into an mp3 file; the voice reads whichever language the text is in | `generate_audio(script, path)` | Student C, Ayhan |
| `src/main.py` | Gradio web app: inputs, language and tone choice, error messages, one retry if the answer is too short | `summarize(url, pdf_file, language, tone)` | Team |

Each file does one job and can be tested on its own.

## Tech stack

- **LLM:** OpenAI `gpt-4o-mini` (Chat Completions, temperature 0.7)
- **Text-to-speech:** OpenAI `tts-1`, voice `alloy`
- **Web app:** Gradio
- **Text extraction:** pypdf (PDFs), requests + BeautifulSoup (web pages)

## Setup

1. Clone the repo and open the folder:
   ```
   git clone https://github.com/SelfUpdateWorks/podcast-repo.git
   cd podcast-repo
   ```
2. Create and activate an environment (Python 3.11):
   ```
   conda create -n bootcamp-env python=3.11
   conda activate bootcamp-env
   ```
3. Install the packages:
   ```
   pip install -r requirements.txt
   ```
   `requirements.txt` needs: `openai`, `gradio`, `pypdf`, `python-dotenv`, `requests`, `beautifulsoup4`.
4. Create a `.env` file in the repo root (copy `.env.example`) and add your OpenAI key:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```
   `.env` is in `.gitignore` and is never committed.

## Run the app

From the repo root:
```
python src/main.py
```
Open the local link shown in the terminal (usually http://127.0.0.1:7860).
Audio files are saved in `outputs/`.

## Test each step on its own

Run these from the repo root. Only the LLM and TTS steps call the API and cost money.

```
python src/data_processor.py   # cleans Data/aiprojectsfail.pdf -> outputs/cleaned_transcript.txt
python src/llm_processor.py    # summary of a sample text, 2 clicks
python src/tts_generator.py    # full chain -> outputs/recap.mp3
```

## Project structure

```
podcast-repo/
├── src/
│   ├── data_processor.py   # load + clean the article
│   ├── llm_processor.py    # LLM: title + 3 takeaways, language, tone
│   ├── tts_generator.py    # text-to-speech -> mp3
│   └── main.py             # Gradio app
├── Data/                   # sample input articles
├── outputs/                # cleaned text and generated audio
├── requirements.txt        # packages to install
├── .env.example            # template for the API key
├── .gitignore
└── README.md
```

## Limitations

- **Scanned PDFs and login-protected pages** have no readable text. The app shows an error; uploading the PDF usually works better than a paywalled link.
- **Long papers:** only the first 30,000 characters go to the LLM, which covers the abstract, method and main results of most papers.
- **Voices:** OpenAI's voices are optimized for English. Other languages are clear but may carry a slight English accent.
- **Text-to-speech limit:** one request accepts up to 4,096 characters. The opening plus 3 takeaways stays well below that.
- **Accuracy:** the prompt keeps the LLM to facts from the article, but takeaways should still be checked against the source, especially in the Funny tone.
- **Cost:** every click makes one LLM call (two if the first answer is too short) and one TTS call.

## Team

Ironhack AI Consulting & Integration Bootcamp, Module 1 project.
Elif (Student A, LLM) · Barsha (Student B, data processing) · Ayhan (Student C, text-to-speech)