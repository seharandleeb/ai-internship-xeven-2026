"""ScholarRAG - paper ingestion.

Fetches an arXiv paper by ID or URL, preferring the clean ar5iv HTML
rendering (which preserves real section headings) and falling back to
raw PDF text extraction when ar5iv has no version of that paper.
Also splits the resulting sections into overlapping word-chunks ready
for embedding.
"""

import re

import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup

AR5IV_URL = "https://ar5iv.labs.arxiv.org/html/{0}"
ARXIV_PDF_URL = "https://arxiv.org/pdf/{0}"
REQUEST_TIMEOUT = 20
CHUNK_WORDS = 180
CHUNK_OVERLAP = 40


def extract_arxiv_id(reference):
    """Pull a bare arXiv ID (e.g. '1706.03762') out of a URL or ID."""
    match = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", reference)
    if not match:
        raise ValueError(
            "Could not find an arXiv ID in: {0}".format(reference)
        )
    return match.group(1)


def fetch_ar5iv_html(arxiv_id):
    """Try the ar5iv HTML version. Returns None on any failure so the
    caller can fall back to the PDF instead."""
    url = AR5IV_URL.format(arxiv_id)
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
    except requests.RequestException:
        return None
    if response.status_code != 200:
        return None
    return response.text


def parse_ar5iv_html(html):
    """Pull title, authors, and {section_name: text} from ar5iv HTML."""
    soup = BeautifulSoup(html, "lxml")

    title_tag = soup.find("h1", class_="ltx_title")
    title = title_tag.get_text(strip=True) if title_tag else "Untitled"

    authors = []
    for tag in soup.select(".ltx_personname"):
        name = tag.get_text(strip=True)
        if name:
            authors.append(name)

    sections = {}
    abstract_tag = soup.find("div", class_="ltx_abstract")
    if abstract_tag:
        sections["Abstract"] = abstract_tag.get_text(" ", strip=True)

    for section in soup.find_all("section", class_="ltx_section"):
        heading_tag = section.find(["h2", "h3"], class_="ltx_title")
        heading = (
            heading_tag.get_text(" ", strip=True)
            if heading_tag else "Section"
        )
        paragraphs = section.find_all("div", class_="ltx_para")
        text = " ".join(p.get_text(" ", strip=True) for p in paragraphs)
        if text:
            sections[heading] = text

    return {"title": title, "authors": authors, "sections": sections}


def fetch_and_parse_pdf(arxiv_id):
    """Fallback path: download the PDF and pull text page by page.

    Less structured than ar5iv (no real section names), so each page
    becomes one pseudo-section labelled 'Page N'.
    """
    url = ARXIV_PDF_URL.format(arxiv_id)
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    document = fitz.open(stream=response.content, filetype="pdf")
    sections = {}
    for page_number, page in enumerate(document, start=1):
        text = page.get_text().strip()
        if text:
            sections["Page {0}".format(page_number)] = text
    document.close()

    return {
        "title": "arXiv:{0}".format(arxiv_id),
        "authors": [],
        "sections": sections,
    }


def load_paper(reference):
    """Fetch a paper by arXiv ID/URL. Tries ar5iv first, then PDF.

    Returns a dict: arxiv_id, title, authors, sections, source.
    """
    arxiv_id = extract_arxiv_id(reference)
    html = fetch_ar5iv_html(arxiv_id)

    if html:
        parsed = parse_ar5iv_html(html)
        source = "ar5iv"
    else:
        parsed = fetch_and_parse_pdf(arxiv_id)
        source = "pdf"

    parsed["arxiv_id"] = arxiv_id
    parsed["source"] = source
    return parsed


def chunk_text(text, chunk_words=CHUNK_WORDS, overlap=CHUNK_OVERLAP):
    """Split text into overlapping word windows."""
    words = text.split()
    if not words:
        return []
    if len(words) <= chunk_words:
        return [text.strip()]

    step = chunk_words - overlap
    pieces = []
    for start in range(0, len(words), step):
        window = words[start:start + chunk_words]
        if not window:
            break
        pieces.append(" ".join(window))
        if start + chunk_words >= len(words):
            break
    return pieces


def chunk_paper(paper):
    """Flatten a parsed paper into chunk dicts carrying citation
    metadata: which paper, which section, which position.
    """
    chunks = []
    counter = 0
    for section_name, text in paper["sections"].items():
        for piece in chunk_text(text):
            counter += 1
            chunks.append({
                "chunk_id": "{0}-{1:03d}".format(
                    paper["arxiv_id"], counter
                ),
                "arxiv_id": paper["arxiv_id"],
                "title": paper["title"],
                "section": section_name,
                "text": piece,
            })
    return chunks


if __name__ == "__main__":
    demo_paper = load_paper("1706.03762")
    print("Title:", demo_paper["title"])
    print("Source:", demo_paper["source"])
    print("Sections found:", list(demo_paper["sections"].keys()))

    demo_chunks = chunk_paper(demo_paper)
    print("Total chunks:", len(demo_chunks))
    print("First chunk text (first 150 chars):")
    print(demo_chunks[0]["text"][:150])