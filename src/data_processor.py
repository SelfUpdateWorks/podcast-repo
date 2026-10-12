"""Part A: Data processing for Podcast Studio.

Loads text from a PDF, a link, or a text file and returns it as one
clean string, ready to be passed to the LLM step.
"""

import re

import io


def fetch_transcript(url):
    """Download a web page and return its raw text."""
    response = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")

        # A link to a PDF file: read the bytes as a PDF, not as text
    if "pdf" in content_type or url.lower().split("?")[0].endswith(".pdf"):
        reader = PdfReader(io.BytesIO(response.content))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages)

    if "html" in content_type:
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
            tag.decompose()
        return soup.get_text(separator="\n")

    return response.text


def read_pdf(file_path):
    """Read a PDF file and return all its text."""
    reader = PdfReader(file_path)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages)


def clean_paper(text):
    """Extra cleaning for academic PDFs."""
    # 1. Drop the title block (authors, universities, emails): start at "Abstract"
    match = re.search(r"\bAbstract\b", text)
    if match:
        text = text[match.start():]

    # 2. Drop the reference list: cut at the last line that says only "References"
    ref_match = None
    for m in re.finditer(r"^\s*(References|REFERENCES)\s*$", text, flags=re.MULTILINE):
        ref_match = m
    if ref_match:
        text = text[:ref_match.start()]

    # 3. Remove lines that contain only a page number
    text = re.sub(r"^\s*\d{1,3}\s*$\n?", "", text, flags=re.MULTILINE)

    # 4. Join words split by a hyphen at the end of a line ("trans-\nformation")
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    # 5. Join the lines inside each paragraph into one line
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    return text


def clean_text(text):
    """Tidy up whitespace so the text is easy for the LLM to use."""
    text = text.replace("\xa0", " ")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_transcript(source):
    """Main function: load text from a PDF, a link, or a text file and clean it."""
    if source.lower().endswith(".pdf"):
        raw = clean_paper(read_pdf(source))
    elif source.startswith("http"):
        raw = fetch_transcript(source)
    else:
        with open(source, "r", encoding="utf-8") as f:
            raw = f.read()
    return clean_text(raw)


if __name__ == "__main__":
    source = "Data/aiprojectsfail.pdf"
    transcript = load_transcript(source)

    with open("outputs/cleaned_transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript)

    print("Saved to outputs/cleaned_transcript.txt")
    print("Total characters:", len(transcript))