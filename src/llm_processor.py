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
- If the text is not a readable article, reply only with: UNREADABLE

Format (the text will be read aloud by a voice):
- No markdown, no bullet symbols, no asterisks, no headings.
- Start the takeaways with "First,", "Second," and "Finally,".
"""


def create_script(text: str) -> str:
    """Turn the article text into 3 spoken-style takeaways."""
    if not text or not text.strip():
        raise ValueError("The article text is empty.")

    angle = random.choice(ANGLES)

    response = client.chat.completions.create(
        model=MODEL,
        temperature=1.0,  # higher = more variety between clicks
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(angle=angle)},
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