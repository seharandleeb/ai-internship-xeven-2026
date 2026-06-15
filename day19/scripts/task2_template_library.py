"""Day 19 - Task 2: Prompt Template Library.

Builds a reusable library of prompt templates for four common task types
(summarization, extraction, generation, analysis). Each template carries a
system message, a user-instruction format with {variables}, and an explicit
output-format specification. The library is stored as JSON in the shape:

    {task_name: {"system": ..., "user": ..., "examples": [...]}}

We then render every template with sample variables and validate that no
placeholder is left unfilled. A live ChatGroq/LCEL call is included but
gated behind GROQ_API_KEY so the script runs (and is verifiable) offline.

Variables supported: {text} {format} {constraints} {examples}

Run from inside day19/scripts/. Full live run on your machine:
    uv run python task2_template_library.py
"""

import json
import os
import re

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional offline
    def load_dotenv(*_a, **_k):
        return False

try:
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_groq import ChatGroq
    LANGCHAIN_OK = True
except ImportError:  # pragma: no cover - offline fallback
    LANGCHAIN_OK = False

MODEL_NAME = "llama-3.3-70b-versatile"
PLACEHOLDER_RE = re.compile(r"\{([a-z_]+)\}")

TEMPLATES = {
    "summarization": {
        "system": (
            "You are a concise technical summarizer. Preserve key facts and "
            "numbers. Never invent information not present in the source."
        ),
        "user": (
            "Summarize the text below.\n"
            "Text: {text}\n"
            "Output format: {format}\n"
            "Constraints: {constraints}"
        ),
        "examples": [],
    },
    "extraction": {
        "system": (
            "You are an information-extraction engine. Return only data that "
            "is explicitly stated. If a field is missing, use null."
        ),
        "user": (
            "Extract the requested fields from the text.\n"
            "Text: {text}\n"
            "Output format: {format}\n"
            "Constraints: {constraints}\n"
            "Examples: {examples}"
        ),
        "examples": [
            {"text": "Ada Lovelace, born 1815 in London.",
             "fields": {"name": "Ada Lovelace", "year": 1815,
                        "city": "London"}},
        ],
    },
    "generation": {
        "system": (
            "You are a creative but on-brief content generator. Follow the "
            "format and constraints exactly; do not exceed limits."
        ),
        "user": (
            "Generate content for the following brief.\n"
            "Brief: {text}\n"
            "Output format: {format}\n"
            "Constraints: {constraints}"
        ),
        "examples": [],
    },
    "analysis": {
        "system": (
            "You are an analytical assistant. Support each claim with "
            "evidence from the text and state uncertainty where it exists."
        ),
        "user": (
            "Analyze the text and answer the prompt.\n"
            "Text: {text}\n"
            "Output format: {format}\n"
            "Constraints: {constraints}"
        ),
        "examples": [],
    },
}

# Sample variable sets used to render/test each template offline.
SAMPLE_VARS = {
    "summarization": {
        "text": "Groq serves the Llama 3.3 70B model at very high tokens "
                "per second on its LPU hardware.",
        "format": "two bullet points",
        "constraints": "max 25 words total; no marketing language",
        "examples": "",
    },
    "extraction": {
        "text": "Marie Curie won the Nobel Prize in Physics in 1903.",
        "format": "JSON with keys name, prize, year",
        "constraints": "year must be an integer; use null if unknown",
        "examples": "{\"name\": \"...\", \"prize\": \"...\", \"year\": 0}",
    },
    "generation": {
        "text": "A launch tweet for a free prompt-engineering workshop.",
        "format": "single tweet",
        "constraints": "under 280 characters; one emoji max; include a CTA",
        "examples": "",
    },
    "analysis": {
        "text": "Few-shot raised our classifier accuracy from 0.72 to 0.86.",
        "format": "one short paragraph then a 'Confidence:' line",
        "constraints": "state the percentage-point gain explicitly",
        "examples": "",
    },
}


def render(template_text, variables):
    """Replace only known {var} placeholders; leave other braces intact."""
    def _sub(match):
        key = match.group(1)
        return str(variables.get(key, match.group(0)))
    return PLACEHOLDER_RE.sub(_sub, template_text)


def unfilled_placeholders(rendered):
    """Return any {placeholder} tokens still present after rendering."""
    return PLACEHOLDER_RE.findall(rendered)


def build_library_file(path):
    """Write the template library to JSON and return the file path."""
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(TEMPLATES, fh, indent=2)
    return path


def render_all():
    """Render every template with its sample vars; return a report list."""
    report = []
    for task, spec in TEMPLATES.items():
        variables = SAMPLE_VARS[task]
        rendered_user = render(spec["user"], variables)
        leftovers = unfilled_placeholders(rendered_user)
        report.append({
            "task": task,
            "rendered_system": spec["system"],
            "rendered_user": rendered_user,
            "unfilled": leftovers,
            "valid": not leftovers,
        })
    return report


def make_live_chain(task):
    """Build an LCEL chain from a stored template for live runs."""
    spec = TEMPLATES[task]
    prompt = ChatPromptTemplate.from_messages([
        ("system", spec["system"]),
        ("human", spec["user"]),
    ])
    model = ChatGroq(model=MODEL_NAME, temperature=0)
    return prompt | model | StrOutputParser()


def main():
    os.makedirs("outputs", exist_ok=True)
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    live = bool(key) and LANGCHAIN_OK

    lib_path = build_library_file(
        os.path.join("outputs", "prompt_templates.json"))
    print(f"Wrote template library -> {lib_path}")

    report = render_all()
    report_path = os.path.join("outputs", "task2_render_report.json")
    with open(report_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)

    print("\nTemplate render check (offline, no API needed):")
    print("-" * 52)
    for item in report:
        status = "OK" if item["valid"] else f"MISSING {item['unfilled']}"
        print(f"{item['task']:<14} render -> {status}")

    all_valid = all(item["valid"] for item in report)
    print(f"\nAll templates rendered cleanly: {all_valid}")
    print(f"Saved render report -> {report_path}")

    if live:
        print(f"\nLIVE mode: testing 'summarization' on Groq "
              f"{MODEL_NAME}...")
        chain = make_live_chain("summarization")
        out = chain.invoke(SAMPLE_VARS["summarization"])
        print("Model output:\n" + out)
    else:
        reason = "no GROQ_API_KEY" if not key else "LangChain not installed"
        print(f"\nOFFLINE mode ({reason}): skipped live template test. "
              "Rendering + validation above already prove the library.")


if __name__ == "__main__":
    main()
