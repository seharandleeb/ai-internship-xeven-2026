"""
Day 26 - FastAPI wrapper around the ReAct agent for the UI.
Run with: uvicorn ui_main:app --reload
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agent import build_agent


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


class AskResponse(BaseModel):
    answer: str


@app.post("/ask", response_model=AskResponse)
async def ask(payload: AskRequest):
    executor = app.state.executor
    result = executor.invoke({"input": payload.question})
    return AskResponse(answer=result["output"])


app.mount("/", StaticFiles(directory="ui", html=True), name="ui")