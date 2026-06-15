"""Day 20 - Task 2: LLM -> Structured Data Pipeline.

Defines an ``Article`` Pydantic model and a pipeline that turns raw
article text into validated ``Article`` objects with retry +
default-value fallback, then exports a structured JSON dataset.

The real path uses ``ChatGroq(...).with_structured_output(Article)``
(LangChain 1.x). A sandbox cannot make live Groq calls, so extraction
is gated: an offline deterministic stub returns objects so the whole
pipeline (retry, fallback, batch loop, JSON export) runs and is
provable with no network and no API key.

Live run on your machine (reads GROQ_API_KEY from .env):
    uv run python task2_structured_pipeline.py --live

Offline run (default, no key needed):
    uv run python task2_structured_pipeline.py
"""

import argparse
import json
import os
from typing import Callable, List, Optional

from pydantic import BaseModel, Field, ValidationError

MAX_RETRIES = 3


class Article(BaseModel):
    """A news article reduced to structured metadata.

    Defaults exist so the pipeline can emit a placeholder object when
    extraction never produces valid data (the fallback path).
    """

    title: str = "UNKNOWN"
    author: str = "UNKNOWN"
    published_date: str = "1970-01-01"
    summary: str = ""
    tags: List[str] = Field(default_factory=list)


def parse_markers(raw: str) -> dict:
    """Parse the simple marker block in a sample article.

    The live LLM never sees these markers as a contract - it reads the
    whole text. They exist only so the offline stub is deterministic.
    """
    fields: dict = {}
    for line in raw.splitlines():
        if line.startswith("TITLE:"):
            fields["title"] = line[len("TITLE:"):].strip()
        elif line.startswith("AUTHOR:"):
            fields["author"] = line[len("AUTHOR:"):].strip()
        elif line.startswith("DATE:"):
            fields["published_date"] = line[len("DATE:"):].strip()
        elif line.startswith("TAGS:"):
            raw_tags = line[len("TAGS:"):].strip()
            fields["tags"] = [
                tag.strip() for tag in raw_tags.split(",") if tag.strip()
            ]
        elif line.startswith("BODY:"):
            fields["summary"] = line[len("BODY:"):].strip()[:160]
    return fields


def offline_extract(raw: str, behavior: str, attempt: int) -> dict:
    """Deterministic stand-in for the LLM call.

    ``behavior`` lets us exercise every branch of the pipeline:
      - ``ok``       : always returns valid data.
      - ``retry``    : returns invalid data on attempt 1, valid after.
      - ``permafail``: always invalid, forcing the default fallback.
    """
    data = parse_markers(raw)
    if behavior == "retry" and attempt == 1:
        data["title"] = None            # None is not str -> error
    if behavior == "permafail":
        data["tags"] = 12345            # int is not List[str] -> error
    return data


def build_live_extractor() -> Callable[[str, int], dict]:
    """Build the real ChatGroq structured-output extractor.

    Imports are local so the offline run needs neither langchain nor
    an API key installed.
    """
    from dotenv import load_dotenv
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_groq import ChatGroq

    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY not found in environment/.env")

    model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    structured = model.with_structured_output(Article)
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You extract article metadata. Fill every field of the "
         "schema from the text. If a field is missing, infer a "
         "sensible value."),
        ("human", "{text}"),
    ])
    chain = prompt | structured

    def _extract(raw: str, attempt: int) -> dict:
        result = chain.invoke({"text": raw})
        return result.model_dump()

    return _extract


def extract_one(sample: dict,
                extractor: Optional[Callable[[str, int], dict]]) -> dict:
    """Extract one article with retry and default-value fallback."""
    raw = sample["raw"]
    behavior = sample["behavior"]
    errors: List[dict] = []
    attempts = 0
    for attempt in range(1, MAX_RETRIES + 1):
        attempts = attempt
        try:
            if extractor is not None:
                data = extractor(raw, attempt)
            else:
                data = offline_extract(raw, behavior, attempt)
            return {
                "article": Article(**data),
                "attempts": attempts,
                "used_default": False,
                "errors": errors,
            }
        except ValidationError as exc:
            errors.append({
                "attempt": attempt,
                "error": exc.errors()[0]["msg"],
            })
    # Retries exhausted: emit a placeholder Article from defaults.
    return {
        "article": Article(),
        "attempts": attempts,
        "used_default": True,
        "errors": errors,
    }


def build_sample_articles() -> List[dict]:
    """Auto-create a 12-article batch so the run needs no setup."""
    specs = [
        ("Groq Posts Record Low-Latency Inference", "A. Khan",
         "2026-02-10", "hardware,inference,llm",
         "Groq reported a new throughput record for its LPU stack."),
        ("LangChain 1.x Lands Structured Output", "M. Rivera",
         "2026-01-22", "langchain,tooling,llm",
         "The 1.x line stabilises with_structured_output across models."),
        ("Pydantic v2 Speeds Validation", "T. Osei",
         "2025-11-30", "python,validation,pydantic",
         "The Rust core keeps Python ergonomics while cutting overhead."),
        ("Small Models Close the Gap", "L. Conti",
         "2026-03-05", "llm,benchmarks,efficiency",
         "Distilled models rival larger ones on narrow tasks."),
        ("Vector Stores Go Mainstream", "R. Patel",
         "2026-02-18", "rag,vector-db,retrieval",
         "Teams adopt managed vector stores for retrieval pipelines."),
        ("Eval Harnesses Get Serious", "S. Nguyen",
         "2026-01-09", "evaluation,llm,quality",
         "Reproducible eval suites become a release gate."),
        ("Function Calling Standardises", "D. Mwangi",
         "2025-12-14", "tooling,api,llm",
         "Tool schemas converge across major providers."),
        ("On-Device Inference Matures", "K. Larsson",
         "2026-03-21", "edge,inference,mobile",
         "Quantised models run comfortably on consumer hardware."),
        ("Data Contracts Reach LLM Apps", "P. Haddad",
         "2026-02-02", "data,schema,reliability",
         "Typed contracts cut silent failures in production apps."),
        ("Observability for LLM Pipelines", "J. Fischer",
         "2026-01-27", "observability,ops,llm",
         "Tracing spans now cover prompt, tool, and parse stages."),
        ("Prompt Templating Best Practice", "N. Abebe",
         "2026-03-11", "prompting,langchain,llm",
         "Reusable templates reduce drift across a codebase."),
        ("Structured Logs Aid Debugging", "C. Romero",
         "2026-02-25", "logging,ops,python",
         "Structured logs make extraction failures easy to trace."),
    ]
    samples: List[dict] = []
    for index, (title, author, date, tags, body) in enumerate(specs):
        raw = (
            f"TITLE: {title}\n"
            f"AUTHOR: {author}\n"
            f"DATE: {date}\n"
            f"TAGS: {tags}\n"
            f"BODY: {body}"
        )
        behavior = "ok"
        if index == 10:
            behavior = "retry"
        elif index == 11:
            behavior = "permafail"
        samples.append({"raw": raw, "behavior": behavior})
    return samples


def estimate_tokens(samples: List[dict]) -> int:
    """Rough token estimate: ~1 token per 0.75 words (approx)."""
    words = sum(len(s["raw"].split()) for s in samples)
    return int(words / 0.75)


def main() -> None:
    """Run the batch pipeline and write the structured dataset."""
    parser = argparse.ArgumentParser(description="Article pipeline")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Use live ChatGroq instead of the offline stub.",
    )
    args = parser.parse_args()

    os.makedirs("outputs", exist_ok=True)
    samples = build_sample_articles()
    extractor = build_live_extractor() if args.live else None

    dataset: List[dict] = []
    error_log: List[dict] = []
    via_retry = 0
    defaults = 0

    for index, sample in enumerate(samples):
        result = extract_one(sample, extractor)
        if result["used_default"]:
            defaults += 1
        elif result["attempts"] > 1:
            via_retry += 1
        if result["errors"]:
            error_log.append({"article_index": index,
                              "events": result["errors"]})
        dataset.append({
            "index": index,
            "used_default": result["used_default"],
            "attempts": result["attempts"],
            "article": result["article"].model_dump(),
        })

    extracted_ok = len(samples) - defaults
    dataset_path = os.path.join("outputs", "task2_articles_dataset.json")
    with open(dataset_path, "w", encoding="utf-8") as handle:
        json.dump(dataset, handle, indent=2)

    log_path = os.path.join("outputs", "task2_errors.log")
    with open(log_path, "w", encoding="utf-8") as handle:
        json.dump(error_log, handle, indent=2)

    approx_tokens = estimate_tokens(samples)
    mode = "LIVE (Groq)" if args.live else "OFFLINE (stub)"
    print(f"Task 2 [{mode}]")
    print(f"  Articles processed     : {len(samples)}")
    print(f"  Extracted successfully : {extracted_ok}")
    print(f"  Recovered via retry    : {via_retry}")
    print(f"  Fell back to default   : {defaults}")
    print(f"  Approx input tokens    : ~{approx_tokens} "
          "(cost ~$0.00, Groq free tier)")
    print(f"  Dataset -> {dataset_path}")
    print(f"  Errors  -> {log_path}")


if __name__ == "__main__":
    main()
