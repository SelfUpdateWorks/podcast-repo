"""
llm_processor.py
Job: send the clean article text to the LLM and get back 3 key takeaways.
Input:  text (str)  - the clean article text from data_processor.py
Output: script (str) - plain spoken text, ready for tts_generator.py
"""

import os
import random

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # reads OPENAI_API_KEY from the .env file

MODEL = "gpt-4o-mini"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# A different "angle" on each click, so the takeaways really change
ANGLES = [
    "the main findings and why they matter",
    "practical implications for everyday life or work",
    "the most surprising or counter-intuitive results",
    "how the study was done and how strong the evidence is",
    "open questions and limitations the authors mention",
]

TONES = {
    "Serious": "Calm, clear and neutral, like a good science journalist.",
    "Funny": (
        "Light and playful, like a friendly comedian explaining science to friends. "
        "Use at least one funny everyday comparison per takeaway. "
        "Every fact must stay exactly as in the article. "
        "Joke about the topic, never about the results, and never exaggerate them."
    ),
}

# SYSTEM PROMPT = our instructions: who the LLM is and what it must do
SYSTEM_PROMPT = """You are a friendly science communicator. You explain research to a curious
friend who has no science background, as if you were chatting over coffee.

Read the scientific article and give exactly 3 key takeaways.

Focus on this angle: {angle}.

How to write:
- Use everyday words. Avoid technical terms. If a technical term is essential,
  explain it right away in simple words (for example: "a placebo, which is a fake
  pill with no medicine in it").
- Turn statistics into plain meaning. Say "noticeably better" or "about one in five
  people" instead of percentages, p-values or confidence intervals.
- Use a short comparison from daily life when an idea is complex.
- Keep sentences short: one idea per sentence.
- For each takeaway, say why it matters to an ordinary person.
- Each takeaway is 2 or 3 sentences.

Accuracy:
- Only use information that is in the article. Do not add facts.
- Simplify the language, never the meaning. If the article is uncertain, say so.
- Keep the strength of the claims: if people only reported how they felt, say
  "people felt" or "people said", not that it was proven.
- Always summarize the text you are given, even if it is long, very technical,
  or partly messy (formulas, symbols, broken lines). Never refuse and never apologize.

Tone:
- {tone}

Format (the text will be read aloud by a voice):
- No markdown, no bullet symbols, no asterisks, no headings.
- Begin with one short sentence that names the article title and, if the text
  gives one, its date.
- Describe the date exactly as the text does: if the text says "submitted",
  say submitted; say "published" only if the text says it was published
  (for example in a journal). If it is unclear what the date means, leave it out.
- If the text says the article is a preprint or not yet peer-reviewed, mention
  that briefly in the opening sentence. If it was accepted at a journal or
  conference, you may mention that instead.
- Keep the article title in its original language, exactly as written in the article.
- Never guess a date.
- Then give the 3 takeaways. Start each one with a natural ordinal word for
  "first", "second" and "finally" in the output language.

Language (most important rule):
- Write your ENTIRE answer in {language}: the opening sentence, the ordinal words
  and every takeaway. The only exception is the article title.
- Translate technical terms into everyday {language} words, not word for word.
"""


def create_script(text: str, language: str = "English", tone: str = "Serious") -> str:
    """Turn the article text into 3 spoken-style takeaways."""
    {"role": "user", "content": f"{text}\n\nWrite the summary in {language}."},
    if not text or not text.strip():
        raise ValueError("The article text is empty.")
    
    text =  text = text[:30000]          # first part of the paper is enough

    angle = random.choice(ANGLES)

    system = SYSTEM_PROMPT.format(angle=angle, language=language, tone=TONES[tone])

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.7,         # was 1.0: still varied, less erratic
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": text},  # USER PROMPT = the data
        ],
    )
    return response.choices[0].message.content.strip()



# Test this file on its own (slide 6): python src/llm_processor.py
if __name__ == "__main__":
    sample = (
        "In a randomized controlled trial (n = 2,000), participants assigned to a "
        "10-minute post-prandial walking intervention demonstrated a statistically "
        "significant improvement in self-reported afternoon cognitive performance "
        "(+15%, p < 0.01) and increased mean sleep duration (+20 min, 95% CI 12-28) "
        "compared with the sedentary control group. Effect sizes were larger among "
        "participants with low baseline physical activity. Limitations include "
        "reliance on self-reported outcome measures."
    )
    for click in range(1, 3):
        print(f"--- Click {click} ---")
        print(create_script(sample))
        print()
