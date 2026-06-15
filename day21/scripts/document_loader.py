"""Document loading + auto-generated sample corpus.

Loads ``.txt`` and ``.pdf`` files into plain text. Also auto-creates a
small sample corpus (text files + one real PDF) so the whole Day 21
pipeline runs end-to-end with zero manual setup.

Each sample document ships with a KNOWN set of gold entities and one
document contains the answer to a known test query, so semantic search
and extraction accuracy can both be verified deterministically.

PDF loading uses ``PyPDFLoader`` (langchain-community) when available and
falls back to ``pypdf`` directly. The sample PDF is written with a tiny
hand-rolled, dependency-free PDF writer so no extra package is needed.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class SampleDoc:
    """A sample document plus its gold-standard entities."""

    filename: str
    text: str
    gold: dict = field(default_factory=dict)


# --- The known sample corpus ------------------------------------------
# Test query targets DOC 1 (the cloud-migration budget sentence).

_MEMO_CLOUD = SampleDoc(
    filename="memo_cloud.txt",
    text=(
        "Internal Memo - Cloud Migration Initiative\n\n"
        "From: Ayesha Khan (Director of Engineering)\n"
        "To: Platform Team\n"
        "Date: 2026-03-14\n"
        "Contact: ayesha.khan@xeven.example.com\n\n"
        "The cloud migration project has an approved budget of "
        "$250,000 for fiscal year 2026. We will migrate the primary "
        "database and the analytics workloads to the new platform.\n\n"
        "Vendor evaluation will be led by Bilal Ahmed in coordination "
        "with Acme Cloud Services. Please direct billing questions to "
        "finance@xeven.example.com before 2026-04-01.\n"
    ),
    gold={
        "people": ["Ayesha Khan", "Bilal Ahmed"],
        "organizations": ["Acme Cloud Services"],
        "emails": [
            "ayesha.khan@xeven.example.com",
            "finance@xeven.example.com",
        ],
        "dates": ["2026-03-14", "2026-04-01"],
        "monetary_amounts": ["$250,000"],
    },
)

_RESEARCH_NOTE = SampleDoc(
    filename="research_note.txt",
    text=(
        "Research Note - Semantic Search Evaluation\n\n"
        "Author: Sara Malik\n"
        "Organization: Xeven Solutions\n"
        "Date: 2026-02-09\n"
        "Email: sara.malik@xeven.example.com\n\n"
        "We benchmarked the all-MiniLM-L6-v2 embedding model against a "
        "larger encoder. The MiniLM model produced 384-dimensional "
        "vectors and ran fully offline. Retrieval quality was "
        "acceptable for short documents, with a small compute budget "
        "of $1,200 spent during the experiment.\n"
    ),
    gold={
        "people": ["Sara Malik"],
        "organizations": ["Xeven Solutions"],
        "emails": ["sara.malik@xeven.example.com"],
        "dates": ["2026-02-09"],
        "monetary_amounts": ["$1,200"],
    },
)

_CONTRACT_PDF = SampleDoc(
    filename="contract_summary.pdf",
    text=(
        "Contract Summary\n"
        "Client: Globex Corporation\n"
        "Signed by: Omar Farooq\n"
        "Date: 2026-01-20\n"
        "Email: omar.farooq@globex.example.com\n"
        "Total contract value: $48,500.\n"
    ),
    gold={
        "people": ["Omar Farooq"],
        "organizations": ["Globex Corporation"],
        "emails": ["omar.farooq@globex.example.com"],
        "dates": ["2026-01-20"],
        "monetary_amounts": ["$48,500"],
    },
)

SAMPLE_DOCS = [_MEMO_CLOUD, _RESEARCH_NOTE, _CONTRACT_PDF]

# A query whose answer lives in DOC 1; used to verify semantic search.
TEST_QUERY = "What is the approved budget for the cloud migration project?"
# The phrase the top-ranked chunk must contain for the test query.
EXPECTED_TOP_PHRASE = "approved budget of $250,000"


def _escape_pdf_text(text: str) -> str:
    """Escape characters that are special inside a PDF text string."""
    return text.replace("\\", r"\\").replace("(", r"\(").replace(
        ")", r"\)"
    )


def write_minimal_pdf(path: str, lines: list[str]) -> None:
    """Write a minimal but valid single-page PDF with selectable text.

    Dependency-free: builds the PDF byte stream by hand so the sample
    corpus needs no PDF-writing library. ``pypdf`` can extract the text
    back out, which is what the loader relies on.
    """
    content_lines = ["BT", "/F1 12 Tf", "72 720 Td"]
    for i, line in enumerate(lines):
        if i > 0:
            content_lines.append("0 -16 Td")
        content_lines.append(f"({_escape_pdf_text(line)}) Tj")
    content_lines.append("ET")
    stream = "\n".join(content_lines)
    stream_bytes = stream.encode("latin-1")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> "
            b">> >>"
        ),
        (
            b"<< /Length "
            + str(len(stream_bytes)).encode("ascii")
            + b" >>\nstream\n"
            + stream_bytes
            + b"\nendstream"
        ),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]

    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode("ascii") + body + b"\nendobj\n"

    xref_pos = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode("ascii")
    out += b"0000000000 65535 f \n"
    for off in offsets[1:]:
        out += f"{off:010d} 00000 n \n".encode("ascii")
    out += (
        b"trailer\n<< /Size "
        + str(len(objects) + 1).encode("ascii")
        + b" /Root 1 0 R >>\nstartxref\n"
        + str(xref_pos).encode("ascii")
        + b"\n%%EOF\n"
    )

    with open(path, "wb") as handle:
        handle.write(out)


def create_sample_corpus(data_dir: str) -> list[SampleDoc]:
    """Materialise the sample corpus on disk and return its metadata."""
    os.makedirs(data_dir, exist_ok=True)
    for doc in SAMPLE_DOCS:
        path = os.path.join(data_dir, doc.filename)
        if doc.filename.lower().endswith(".pdf"):
            write_minimal_pdf(path, doc.text.splitlines())
        else:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(doc.text)
    return SAMPLE_DOCS


def _load_pdf(path: str) -> str:
    """Extract text from a PDF (PyPDFLoader first, then pypdf)."""
    try:
        from langchain_community.document_loaders import PyPDFLoader

        pages = PyPDFLoader(path).load()
        text = "\n".join(p.page_content for p in pages).strip()
        if text:
            return text
    except Exception:
        pass
    from pypdf import PdfReader

    reader = PdfReader(path)
    return "\n".join(
        (page.extract_text() or "") for page in reader.pages
    ).strip()


def load_document(path: str) -> str:
    """Load a single ``.txt`` or ``.pdf`` file to plain text."""
    if path.lower().endswith(".pdf"):
        return _load_pdf(path)
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def load_corpus(data_dir: str) -> list[dict]:
    """Load every sample file from ``data_dir`` with its gold labels."""
    docs = []
    for doc in SAMPLE_DOCS:
        path = os.path.join(data_dir, doc.filename)
        docs.append(
            {
                "filename": doc.filename,
                "text": load_document(path),
                "gold": doc.gold,
            }
        )
    return docs
