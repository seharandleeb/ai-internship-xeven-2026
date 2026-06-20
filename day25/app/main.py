"""ScholarRAG - FastAPI service.

Thin HTTP wrapper around RagService: add/list/remove papers, search,
ask questions, and a health check. A simple X-API-Key header protects
every endpoint except /health, since each call to the others costs
real Gemini/Groq quota on the live demo.
"""

import logging
import os
import time
from contextlib import asynccontextmanager
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

from rag_service import RagService

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scholarrag")

API_KEY = os.getenv("SCHOLARRAG_API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Build the RagService once at startup, reuse it for every call."""
    logger.info("Starting ScholarRAG service...")
    app.state.service = RagService()
    logger.info("ScholarRAG service ready.")
    yield
    logger.info("Shutting down ScholarRAG service.")


app = FastAPI(title="ScholarRAG", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log method, path, status code, and duration for every request."""
    start = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start) * 1000
    logger.info(
        "%s %s -> %s (%.1fms)",
        request.method, request.url.path,
        response.status_code, duration_ms,
    )
    return response


def require_api_key(x_api_key: Optional[str] = Depends(api_key_header)):
    """Reject requests without a valid X-API-Key header.

    If SCHOLARRAG_API_KEY isn't set in .env at all, auth is skipped -
    convenient for local development. The deployed demo will have it
    set, so this only matters once it's live.
    """
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key.")


class AddPaperRequest(BaseModel):
    reference: str = Field(
        ..., description="arXiv ID or URL, e.g. '1706.03762'"
    )


class PaperInfo(BaseModel):
    arxiv_id: str
    title: str
    source: str
    chunk_count: int


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    rerank: bool = True


class SearchHit(BaseModel):
    chunk_id: str
    arxiv_id: str
    title: str
    section: str
    text: str
    score: float


class AskRequest(BaseModel):
    query: str
    top_k: int = 5


class SourceInfo(BaseModel):
    arxiv_id: str
    title: str
    section: str
    chunk_id: str


class AskResponse(BaseModel):
    answer: str
    sources: List[SourceInfo]


class HealthResponse(BaseModel):
    status: str
    papers_loaded: int
    total_chunks: int


@app.get("/health", response_model=HealthResponse)
async def health(request: Request):
    """Unauthenticated status check - safe for uptime monitors."""
    info = request.app.state.service.health()
    return HealthResponse(status="ok", **info)


@app.post(
    "/papers",
    response_model=PaperInfo,
    dependencies=[Depends(require_api_key)],
)
async def add_paper(payload: AddPaperRequest, request: Request):
    service: RagService = request.app.state.service
    try:
        info = service.add_paper(payload.reference)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Failed to add paper: %s", payload.reference)
        raise HTTPException(
            status_code=502,
            detail="Could not fetch or parse that paper.",
        ) from exc
    return PaperInfo(**info)


@app.get(
    "/papers",
    response_model=List[PaperInfo],
    dependencies=[Depends(require_api_key)],
)
async def list_papers(request: Request):
    service: RagService = request.app.state.service
    return [PaperInfo(**paper) for paper in service.list_papers()]


@app.delete("/papers/{arxiv_id}", dependencies=[Depends(require_api_key)])
async def remove_paper(arxiv_id: str, request: Request):
    service: RagService = request.app.state.service
    removed = service.remove_paper(arxiv_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Paper not found.")
    return {"removed": arxiv_id}


@app.post(
    "/search",
    response_model=List[SearchHit],
    dependencies=[Depends(require_api_key)],
)
async def search(payload: SearchRequest, request: Request):
    service: RagService = request.app.state.service
    hits = service.search(
        payload.query, top_k=payload.top_k, rerank=payload.rerank
    )
    return [SearchHit(**hit) for hit in hits]


@app.post(
    "/ask",
    response_model=AskResponse,
    dependencies=[Depends(require_api_key)],
)
async def ask(payload: AskRequest, request: Request):
    service: RagService = request.app.state.service
    try:
        result = service.ask(payload.query, top_k=payload.top_k)
    except Exception as exc:
        logger.exception("Ask failed for query: %s", payload.query)
        raise HTTPException(
            status_code=503,
            detail="The assistant is temporarily unavailable.",
        ) from exc
    return AskResponse(**result)