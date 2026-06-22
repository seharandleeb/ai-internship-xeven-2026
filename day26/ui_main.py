"""
Day 26/27 - FastAPI wrapper around the ReAct agent, now with
multi-turn conversation memory per session.
"""

import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agent import build_agent

# session_id -> list of {"role": "user"/"assistant", "content": str}
SESSIONS: dict[str, list[dict]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.executor = build_agent()
    yield


app = FastAPI(title="Day26 Agent UI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str
    session_id: str | None = None


class AskResponse(BaseModel):
    answer: str
    session_id: str


def build_contextual_input(history: list[dict], question: str) -> str:
    """Fold prior turns into the input so the ReAct agent has context."""
    if not history:
        return question
    convo = "\n".join(
        f"{'User' if h['role'] == 'user' else 'Assistant'}: {h['content']}"
        for h in history[-6:]  # last 6 turns to keep prompt small
    )
    return (
        f"Previous conversation:\n{convo}\n\n"
        f"New question (answer this, using the conversation above only "
        f"as context if relevant): {question}"
    )


@app.post("/ask", response_model=AskResponse)
async def ask(payload: AskRequest):
    session_id = payload.session_id or str(uuid.uuid4())
    history = SESSIONS.setdefault(session_id, [])

    contextual_input = build_contextual_input(history, payload.question)

    executor = app.state.executor
    result = executor.invoke({"input": contextual_input})
    answer = result["output"]

    history.append({"role": "user", "content": payload.question})
    history.append({"role": "assistant", "content": answer})

    return AskResponse(answer=answer, session_id=session_id)


@app.post("/new_session")
async def new_session():
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = []
    return {"session_id": session_id}


app.mount("/", StaticFiles(directory="ui", html=True), name="ui")