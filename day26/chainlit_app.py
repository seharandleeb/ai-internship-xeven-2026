"""
Day 26/27 - Chainlit chat UI for the agent, with conversation memory
and file upload support (ask questions about an uploaded document).
Run with: chainlit run chainlit_app.py -w
"""

import chainlit as cl
from langchain_core.messages import HumanMessage, AIMessage
from agent import build_agent

import fitz  # pymupdf

executor = None

MAX_DOC_CHARS = 50000  # keep the injected document excerpt prompt-sized


def extract_text(file_path: str, mime: str) -> str:
    """Extract plain text from an uploaded PDF or text file."""
    if mime == "application/pdf" or file_path.lower().endswith(".pdf"):
        doc = fitz.open(file_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


@cl.on_chat_start
async def start():
    global executor
    if executor is None:
        executor = build_agent()
    cl.user_session.set("history", [])
    cl.user_session.set("uploaded_doc", None)
    cl.user_session.set("uploaded_doc_name", None)
    await cl.Message(
        content="Hi! Ask me anything, or upload a PDF/text file and I'll answer questions about it."
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    # Handle any uploaded files attached to this message
    for element in message.elements:
        if element.mime in ("application/pdf", "text/plain") or element.path.lower().endswith((".pdf", ".txt", ".md")):
            text = extract_text(element.path, element.mime)
            cl.user_session.set("uploaded_doc", text[:MAX_DOC_CHARS])
            cl.user_session.set("uploaded_doc_name", element.name)
            await cl.Message(
                content=f"Got it, I've read **{element.name}** ({len(text)} characters). Ask me anything about it."
            ).send()

    history = cl.user_session.get("history", [])
    uploaded_doc = cl.user_session.get("uploaded_doc")
    doc_name = cl.user_session.get("uploaded_doc_name")

    user_input = message.content

    # If a document is loaded, inject it as grounding context for this turn
    if uploaded_doc:
        user_input = (
            f"The user has uploaded a document called '{doc_name}'. "
            f"Use it to answer if relevant, and say so explicitly when you do.\n\n"
            f"--- DOCUMENT CONTENT START ---\n{uploaded_doc}\n--- DOCUMENT CONTENT END ---\n\n"
            f"User question: {message.content}"
        )

    thinking = cl.Message(content="")
    await thinking.send()

    result = executor.invoke({
        "input": user_input,
        "chat_history": history,
    })
    answer = result["output"]

    history.append(HumanMessage(content=message.content))
    history.append(AIMessage(content=answer))
    cl.user_session.set("history", history[-12:])

    thinking.content = answer
    await thinking.update()