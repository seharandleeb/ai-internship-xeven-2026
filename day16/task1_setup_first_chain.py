"""Day 16 - Task 1: LangChain setup and first LCEL chain.

Sets up the ChatGroq model wrapper, runs a simple completion, builds a
reusable PromptTemplate, and wires a first chain together with the
LangChain Expression Language (LCEL): ``prompt | model | parser``.

Stack: Groq free tier, model ``llama-3.3-70b-versatile``, key ``GROQ_API_KEY``
read from a local ``.env`` file.
"""

import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_groq import ChatGroq

MODEL_NAME = "llama-3.3-70b-versatile"


def load_api_key() -> str:
    """Load ``GROQ_API_KEY`` from the environment / .env file.

    Returns:
        The API key string.

    Raises:
        RuntimeError: If the key is not set.
    """
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to a .env file in this folder:\n"
            "    GROQ_API_KEY=your_key_here"
        )
    return api_key


def build_model(temperature: float = 0.3) -> ChatGroq:
    """Create the ChatGroq model wrapper.

    Args:
        temperature: Sampling temperature (0 = deterministic).

    Returns:
        A configured :class:`ChatGroq` instance.
    """
    load_api_key()
    return ChatGroq(model=MODEL_NAME, temperature=temperature)


def simple_completion(model: ChatGroq, question: str) -> str:
    """Run a single completion through the raw model wrapper.

    Args:
        model: The ChatGroq model.
        question: A plain-text question.

    Returns:
        The model's text answer.
    """
    response = model.invoke(question)
    return response.content


def build_first_chain(model: ChatGroq):
    """Build the first LCEL chain: prompt | model | output parser.

    Args:
        model: The ChatGroq model.

    Returns:
        A runnable chain that accepts ``{"topic": ...}`` and returns text.
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a concise technical tutor."),
            ("human", "Explain {topic} to a beginner in exactly two sentences."),
        ]
    )
    parser = StrOutputParser()
    return prompt | model | parser


def demo_prompt_template() -> str:
    """Show a reusable single-variable PromptTemplate being formatted.

    Returns:
        The formatted prompt string.
    """
    template = PromptTemplate.from_template(
        "Write a one-line definition of: {term}"
    )
    return template.format(term="vector embeddings")


def main() -> None:
    """Run the Task 1 demonstrations end to end."""
    print("=== Task 1: LangChain Setup & First Chain ===\n")

    print("PromptTemplate formatting (no API call needed):")
    print(" ", demo_prompt_template(), "\n")

    model = build_model()

    print("Simple completion:")
    print(" ", simple_completion(model, "In one sentence, what is LangChain?"))
    print()

    print("First LCEL chain (prompt | model | parser):")
    chain = build_first_chain(model)
    answer = chain.invoke({"topic": "LangChain Expression Language"})
    print(" ", answer)


if __name__ == "__main__":
    main()
