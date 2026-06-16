"""Day 21 — Document Analyzer UI (Streamlit).

Roadmap requirements covered:
- Upload PDF or text file
- Extract embeddings (MiniLM live / offline hash)
- Smart chunking via RecursiveCharacterTextSplitter (tuned size/overlap)
- Semantic search: query documents, return relevant chunks + scores
- Structured extraction: Pydantic entities from document
- Output report: findings summary, entity list, relevance scores

Run (from day21/scripts/, inside .venv312):
    streamlit run app.py
"""
from __future__ import annotations

import hashlib
import os
import sys
import tempfile

import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))

import chunker  # noqa: E402
import document_loader as dl  # noqa: E402
import embeddings_index as ei  # noqa: E402
import entity_extraction as ee  # noqa: E402

# ── page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Document Analyzer — Day 21",
    page_icon="🔍",
    layout="wide",
)

# ── custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .stApp { background-color: #0f1117; color: #e8eaf0; }
    section[data-testid="stSidebar"] {
        background-color: #1a1d27;
        border-right: 1px solid #2d3045;
    }
    div[data-testid="metric-container"] {
        background: #1a1d27;
        border: 1px solid #2d3045;
        border-radius: 8px;
        padding: 12px 16px;
    }
    .chunk-card {
        background: #1a1d27;
        border-left: 3px solid #7c83fd;
        border-radius: 6px;
        padding: 14px 16px;
        margin-bottom: 10px;
        font-size: 0.88rem;
        line-height: 1.6;
    }
    .pill {
        display: inline-block;
        background: #23273a;
        border: 1px solid #7c83fd;
        border-radius: 20px;
        padding: 3px 12px;
        margin: 3px 4px 3px 0;
        font-size: 0.82rem;
        color: #c5c8e8;
    }
    .score-track {
        background: #23273a;
        border-radius: 4px;
        height: 6px;
        margin-top: 4px;
    }
    .score-fill {
        background: #7c83fd;
        border-radius: 4px;
        height: 6px;
    }
    h2, h3 { color: #a0a4d4; }
    div[data-testid="stFileUploader"] {
        background: #1a1d27;
        border: 1px dashed #2d3045;
        border-radius: 8px;
        padding: 8px;
    }
    div[data-testid="stButton"] > button {
        background: #7c83fd;
        color: #0f1117;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        padding: 0.5rem 1.4rem;
        width: 100%;
    }
    div[data-testid="stButton"] > button:hover {
        background: #9ba1ff;
        color: #0f1117;
    }
    button[data-baseweb="tab"] { color: #a0a4d4 !important; }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #7c83fd !important;
        border-bottom: 2px solid #7c83fd !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── cached helpers ───────────────────────────────────────────────────────────

@st.cache_resource(show_spinner=False)
def _get_embedder(use_live: bool):
    """Load embedder once; cached for the lifetime of the server."""
    return ei.get_embedder(use_offline=not use_live)


@st.cache_data(show_spinner=False)
def _load_text(file_bytes: bytes, filename: str) -> str:
    """Extract text from uploaded bytes; cached per file hash."""
    suffix = ".pdf" if filename.lower().endswith(".pdf") else ".txt"
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=suffix
    ) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    text = dl.load_document(tmp_path)
    os.unlink(tmp_path)
    return text


@st.cache_data(show_spinner=False)
def _chunk_text(
    text: str, chunk_size: int, chunk_overlap: int
) -> list[str]:
    """Chunk text; cached per (text, size, overlap)."""
    return chunker.chunk_text(text, chunk_size, chunk_overlap)


@st.cache_data(show_spinner=False)
def _build_index(
    chunks: tuple[str, ...],
    filename: str,
    use_live: bool,
):
    """Build FAISS index; cached per (chunks, filename, mode)."""
    embedder = _get_embedder(use_live)
    chunk_dicts = [
        {"source": filename, "chunk_id": i, "text": c}
        for i, c in enumerate(chunks)
    ]
    index = ei.SemanticIndex(embedder).build(chunk_dicts)
    return index, chunk_dicts


# ── helpers ──────────────────────────────────────────────────────────────────

def _pills(items: list[str]) -> str:
    if not items:
        return "<span style='color:#555'>None found</span>"
    return "".join(
        f"<span class='pill'>{i}</span>" for i in items
    )


def _score_bar(score: float) -> str:
    pct = int(min(max(score, 0.0), 1.0) * 100)
    return (
        f"<div class='score-track'>"
        f"<div class='score-fill' style='width:{pct}%'></div>"
        f"</div>"
    )


def _file_hash(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()[:8]


# ── sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")

    use_live = st.toggle(
        "Use real MiniLM embeddings",
        value=False,
        help=(
            "OFF = fast offline mode (no download).\n"
            "ON  = real all-MiniLM-L6-v2 "
            "(~80 MB download on first run)."
        ),
    )
    use_live_extract = st.toggle(
        "Use Groq entity extraction",
        value=False,
        help=(
            "OFF = offline regex extraction (instant).\n"
            "ON  = Groq llama-3.3-70b-versatile "
            "(needs GROQ_API_KEY in .env)."
        ),
    )

    st.markdown("---")
    st.markdown("**Chunk parameters**")
    chunk_size = st.slider(
        "Chunk size (chars)", 200, 800,
        chunker.DEFAULT_CHUNK_SIZE, 50,
    )
    chunk_overlap = st.slider(
        "Chunk overlap (chars)", 0, 200,
        chunker.DEFAULT_CHUNK_OVERLAP, 10,
    )
    top_k = st.slider("Top-K results", 1, 10, 3)

    st.markdown("---")
    st.markdown(
        "<small style='color:#555'>Day 21 · Xeven Solutions<br>"
        "Sehar Andleeb</small>",
        unsafe_allow_html=True,
    )

# ── main header ──────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='color:#7c83fd;margin-bottom:4px'>"
    "🔍 Document Analyzer</h1>"
    "<p style='color:#555;margin-top:0'>Week 3 Review — "
    "upload · chunk · embed · search · extract</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ── upload ───────────────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    "Upload a PDF or text file",
    type=["pdf", "txt"],
)

if uploaded is None:
    st.info(
        "Upload a PDF or .txt file above to get started. "
        "Adjust settings in the sidebar."
    )
    st.stop()

# ── process (all cached) ─────────────────────────────────────────────────────
file_bytes = uploaded.read()

with st.spinner("Reading document…"):
    raw_text = _load_text(file_bytes, uploaded.name)

if not raw_text.strip():
    st.error(
        "Could not extract text from this file. "
        "Try a different PDF."
    )
    st.stop()

with st.spinner("Chunking…"):
    chunks = _chunk_text(raw_text, chunk_size, chunk_overlap)

with st.spinner("Building index…"):
    index, chunk_dicts = _build_index(
        tuple(chunks), uploaded.name, use_live
    )

# ── metrics row ──────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Characters", f"{len(raw_text):,}")
c2.metric("Chunks", len(chunks))
c3.metric("Chunk size", chunk_size)
c4.metric(
    "Embedder",
    "MiniLM (live)" if use_live else "Offline hash",
)

st.markdown("---")

# ── tabs ─────────────────────────────────────────────────────────────────────
tab_search, tab_extract, tab_report, tab_preview = st.tabs([
    "🔎 Semantic Search",
    "🏷️ Entity Extraction",
    "📄 Output Report",
    "📑 Document Preview",
])

# ── TAB 1: SEMANTIC SEARCH ────────────────────────────────────────────
with tab_search:
    st.markdown("### Query your document")
    query = st.text_input(
        "Enter your question or search query",
        placeholder=(
            "e.g. What is the main topic of this document?"
        ),
    )
    search_btn = st.button("Search", key="search_btn")

    if search_btn and query.strip():
        with st.spinner("Searching…"):
            hits = index.search(query.strip(), k=top_k)
        st.markdown(
            f"**Top {len(hits)} results** for: *{query}*"
        )
        for i, hit in enumerate(hits, 1):
            score = hit["score"]
            st.markdown(
                f"<div class='chunk-card'>"
                f"<b style='color:#7c83fd'>#{i}</b> &nbsp;"
                f"<b>Score: {score:.4f}</b>"
                + _score_bar(score)
                + f"<br><br>{hit['text']}"
                f"</div>",
                unsafe_allow_html=True,
            )
    elif search_btn:
        st.warning("Please enter a query first.")
    else:
        st.markdown(
            "<p style='color:#555'>"
            "Enter a question above and click Search.</p>",
            unsafe_allow_html=True,
        )

# ── TAB 2: ENTITY EXTRACTION ──────────────────────────────────────────
with tab_extract:
    st.markdown("### Structured entity extraction")
    st.markdown(
        "Extracts **people, organizations, emails, dates, "
        "and monetary amounts** using "
        + (
            "Groq `llama-3.3-70b-versatile`"
            if use_live_extract
            else "offline regex extractor"
        )
        + "."
    )
    extract_btn = st.button(
        "Extract Entities", key="extract_btn"
    )

    if extract_btn:
        with st.spinner("Extracting…"):
            try:
                if use_live_extract:
                    entities = ee.live_extract(raw_text)
                else:
                    entities = ee.offline_extract(
                        raw_text, gold={}
                    )
                st.session_state["entities"] = entities
            except RuntimeError as exc:
                st.error(str(exc))

    if "entities" in st.session_state:
        ents = st.session_state["entities"]
        e1, e2 = st.columns(2)
        with e1:
            st.markdown("**👤 People**")
            st.markdown(
                _pills(ents.people), unsafe_allow_html=True
            )
            st.markdown("**🏢 Organizations**")
            st.markdown(
                _pills(ents.organizations),
                unsafe_allow_html=True,
            )
            st.markdown("**📧 Emails**")
            st.markdown(
                _pills(ents.emails), unsafe_allow_html=True
            )
        with e2:
            st.markdown("**📅 Dates**")
            st.markdown(
                _pills(ents.dates), unsafe_allow_html=True
            )
            st.markdown("**💰 Monetary Amounts**")
            st.markdown(
                _pills(ents.monetary_amounts),
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            "<p style='color:#555'>"
            "Click Extract Entities above.</p>",
            unsafe_allow_html=True,
        )

# ── TAB 3: OUTPUT REPORT ──────────────────────────────────────────────
with tab_report:
    st.markdown("### Output report")
    report_lines = [
        f"**File:** {uploaded.name}",
        f"**Characters:** {len(raw_text):,}",
        f"**Chunks:** {len(chunks)} "
        f"(size={chunk_size}, overlap={chunk_overlap})",
        "**Embedder:** "
        + ("MiniLM live" if use_live else "Offline hash"),
        "**Extractor:** "
        + (
            "Groq live"
            if use_live_extract
            else "Offline regex"
        ),
    ]
    for line in report_lines:
        st.markdown(line)

    st.markdown("---")

    if "entities" in st.session_state:
        ents = st.session_state["entities"]
        st.markdown("#### Entities found")
        for label, items in {
            "People": ents.people,
            "Organizations": ents.organizations,
            "Emails": ents.emails,
            "Dates": ents.dates,
            "Monetary Amounts": ents.monetary_amounts,
        }.items():
            st.markdown(
                f"- **{label}** ({len(items)}): "
                + (", ".join(items) if items else "*none*")
            )
    else:
        st.info(
            "Run entity extraction in the "
            "🏷️ tab to populate this section."
        )

    st.markdown("---")
    st.markdown("#### Chunk overview")
    for i, ch in enumerate(chunks[:5]):
        with st.expander(f"Chunk {i + 1} — {len(ch)} chars"):
            st.text(
                ch[:300] + ("…" if len(ch) > 300 else "")
            )
    if len(chunks) > 5:
        st.caption(f"… and {len(chunks) - 5} more chunks.")

# ── TAB 4: DOCUMENT PREVIEW ────────────────────────────────────────────
with tab_preview:
    st.markdown("### Raw document text")
    st.text_area(
        "Extracted text",
        value=raw_text,
        height=500,
        disabled=True,
        label_visibility="collapsed",
    )