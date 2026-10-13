# podcast-repo
# Science in Plain Words

Turn a scientific article into **3 plain-language takeaways** and a short **audio podcast**.
Paste a link or upload a PDF, click **Summarize**, read the takeaways and listen to them.
Click again for a different angle on the same article.

Built for curious people with no science background who want to understand research
without the jargon.

## How it works

```
PDF or link ──► data_processor.py ──► llm_processor.py ──► tts_generator.py ──► 🎧 .mp3
                 load + clean text     3 key takeaways      text-to-speech
                                  ▲
                          main.py (Gradio app) connects all the steps
```

| File | Job | Main function | Owner |
|---|---|---|---|
| `src/data_processor.py` | Load text from a PDF, a link or a .txt file and clean it (drops title block, references, page numbers, broken lines) | `load_transcript(source)` | Student B, Barsha |
| `src/llm_processor.py` | Send the clean text to the LLM and get back 3 spoken-style takeaways, with a random angle on each click | `create_script(text)` | Student A, Elif |
| `src/tts_generator.py` | Turn the takeaways into an mp3 file | `generate_audio(script, path)` | Student C, Ayhan |
| `src/main.py` | Gradio web app that connects the three steps | `summarize(url, pdf_file)` | Team |

Each file does one job and can be tested on its own.

## Tech stack

- **LLM:** OpenAI `gpt-4o-mini` (Chat Completions)
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
python src/llm_processor.py    # 3 takeaways from a sample text, 2 clicks
python src/tts_generator.py    # full chain -> outputs/recap.mp3
```

## Project structure

```
podcast-repo/
├── src/
│   ├── data_processor.py   # load + clean the article
│   ├── llm_processor.py    # LLM: 3 key takeaways
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

- **Scanned PDFs and login-protected pages** have no readable text. The app shows an error instead of a summary.
- **Text-to-speech limit:** one request accepts up to 4,096 characters. Three takeaways are well below that, so no splitting is needed.
- **Accuracy:** the prompt tells the LLM to use only facts from the article and to keep the strength of each claim, but takeaways should still be checked against the source.
- **Cost:** every click makes one LLM call and one TTS call.

## Team

Ironhack AI Consulting & Integration Bootcamp, Module 1 project.
Elif (Student A, LLM) · Barsha (Student B, data processing) · Ayhan (Student C, text-to-speech)