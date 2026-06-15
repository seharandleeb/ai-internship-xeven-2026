"""Day 19 - Task 1: Prompting Technique Comparison.

Compares zero-shot, few-shot, and chain-of-thought (CoT) prompting on a
3-class sentiment-analysis task (positive / negative / neutral) over 20
labeled samples. For each technique we report accuracy, average latency,
and an approximate token-based cost (Groq free tier = no $ charge).

Stack: LangChain 1.x LCEL (prompt | model | parser) with ChatGroq.
The GROQ_API_KEY is read from a local .env via os.getenv -- it never
appears in this file. If the key or LangChain is unavailable the script
falls back to a clearly-labeled OFFLINE lexicon classifier so the whole
pipeline (prompts, scoring, cost estimate, reporting) still runs and can
be verified end-to-end.

Run from inside day19/scripts/ so outputs land in day19/scripts/outputs/.
Full live run on your machine:
    uv run python task1_technique_comparison.py
"""

import json
import os
import time

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional offline
    def load_dotenv(*_a, **_k):
        return False

# LangChain is imported lazily/defensively so the script still runs in a
# sandbox without it installed. Real runs use these imports.
try:
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_groq import ChatGroq
    LANGCHAIN_OK = True
except ImportError:  # pragma: no cover - offline fallback
    LANGCHAIN_OK = False

MODEL_NAME = "llama-3.3-70b-versatile"
LABELS = ("positive", "negative", "neutral")

# 20 labeled samples auto-created here so the script runs with no setup.
SAMPLES = [
    ("Absolutely loved this, best purchase all year!", "positive"),
    ("The package arrived and the item works fine.", "neutral"),
    ("Terrible quality, broke after one day.", "negative"),
    ("I'm thrilled with how fast the support replied.", "positive"),
    ("It is a phone. It makes calls.", "neutral"),
    ("Worst customer service I have ever dealt with.", "negative"),
    ("Honestly exceeded every expectation I had.", "positive"),
    ("The meeting is scheduled for 3pm on Tuesday.", "neutral"),
    ("Such a waste of money, deeply disappointed.", "negative"),
    ("Fantastic experience, would recommend to anyone.", "positive"),
    ("The report contains four sections and an index.", "neutral"),
    ("Completely useless and frustrating to set up.", "negative"),
    ("What a delightful surprise, made my whole week.", "positive"),
    ("Delivery window is between 9am and noon.", "neutral"),
    ("I regret buying this, it never worked properly.", "negative"),
    ("Not bad, but not great either, just okay I guess.", "neutral"),
    ("The film was a dull, forgettable slog.", "negative"),
    ("Brilliant value and the build feels premium.", "positive"),
    ("They restocked the shelves this morning.", "neutral"),
    ("I can't stand how laggy this app has become.", "negative"),
]

FEW_SHOT_EXAMPLES = [
    ("This is the best thing I've ever owned!", "positive"),
    ("The store opens at nine every weekday.", "neutral"),
    ("Awful. I want a refund immediately.", "negative"),
]

ZERO_SHOT_SYSTEM = (
    "You are a precise sentiment classifier. Read the text and reply with "
    "exactly one lowercase word: positive, negative, or neutral. Output "
    "only that single word with no punctuation or explanation."
)

FEW_SHOT_SYSTEM = (
    "You are a precise sentiment classifier. Use the examples to learn the "
    "labeling style, then classify the new text. Reply with exactly one "
    "lowercase word: positive, negative, or neutral. No other text."
)

COT_SYSTEM = (
    "You are a precise sentiment classifier. Think step by step about tone, "
    "word choice, and intent in one short sentence, then on a new line "
    "output 'Label: <positive|negative|neutral>'. The label must be one of "
    "those three lowercase words."
)

# Simple lexicon used only by the OFFLINE fallback classifier.
POS_WORDS = {
    "loved", "love", "best", "thrilled", "exceeded", "fantastic",
    "recommend", "delightful", "brilliant", "premium", "great",
    "premium", "surprise", "premium",
}
NEG_WORDS = {
    "terrible", "broke", "worst", "waste", "disappointed", "useless",
    "frustrating", "regret", "dull", "forgettable", "awful", "laggy",
    "can't", "stand", "slog",
}


def build_prompt(technique):
    """Return an LCEL ChatPromptTemplate for the given technique."""
    if technique == "zero_shot":
        return ChatPromptTemplate.from_messages([
            ("system", ZERO_SHOT_SYSTEM),
            ("human", "Text: {text}"),
        ])
    if technique == "few_shot":
        shots = "\n".join(
            f"Text: {t}\nLabel: {lab}" for t, lab in FEW_SHOT_EXAMPLES
        )
        return ChatPromptTemplate.from_messages([
            ("system", FEW_SHOT_SYSTEM),
            ("human", shots + "\n\nText: {text}\nLabel:"),
        ])
    return ChatPromptTemplate.from_messages([
        ("system", COT_SYSTEM),
        ("human", "Text: {text}"),
    ])


def normalize_label(raw):
    """Map a raw model reply to one of the three canonical labels."""
    text = raw.lower()
    if "label:" in text:
        text = text.split("label:")[-1]
    for label in LABELS:
        if label in text:
            return label
    return "neutral"


def offline_classify(text):
    """Deterministic lexicon classifier for the OFFLINE fallback only."""
    tokens = {w.strip(".,!?'\"").lower() for w in text.split()}
    pos = len(tokens & POS_WORDS)
    neg = len(tokens & NEG_WORDS)
    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    return "neutral"


def estimate_tokens(text):
    """Approximate token count (~1.3 tokens per whitespace word)."""
    return int(len(text.split()) * 1.3) + 1


def accuracy(predictions, golds):
    """Fraction of predictions matching the gold labels."""
    hits = sum(p == g for p, g in zip(predictions, golds))
    return hits / len(golds) if golds else 0.0


def run_technique(technique, invoke, live):
    """Run one technique over all samples; return a metrics dict."""
    preds, golds = [], []
    in_tokens = out_tokens = 0
    start = time.perf_counter()
    for text, gold in SAMPLES:
        golds.append(gold)
        if live:
            raw = invoke(technique, text)
        else:
            raw = offline_classify(text)
        preds.append(normalize_label(raw))
        in_tokens += estimate_tokens(text) + 60
        out_tokens += estimate_tokens(raw)
    elapsed = time.perf_counter() - start
    return {
        "technique": technique,
        "accuracy": round(accuracy(preds, golds), 4),
        "avg_latency_s": round(elapsed / len(SAMPLES), 4),
        "approx_input_tokens": in_tokens,
        "approx_output_tokens": out_tokens,
        "approx_total_tokens": in_tokens + out_tokens,
        "approx_cost_usd": 0.0,
        "mode": "live" if live else "offline_mock",
        "predictions": preds,
    }


def make_live_invoker():
    """Build a closure that invokes the real Groq model via LCEL."""
    model = ChatGroq(model=MODEL_NAME, temperature=0)
    parser = StrOutputParser()
    chains = {
        name: build_prompt(name) | model | parser
        for name in ("zero_shot", "few_shot", "cot")
    }

    def invoke(technique, text):
        return chains[technique].invoke({"text": text})

    return invoke


def main():
    os.makedirs("outputs", exist_ok=True)
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    live = bool(key) and LANGCHAIN_OK

    if live:
        print(f"LIVE mode: calling Groq model {MODEL_NAME} via LangChain.")
        invoke = make_live_invoker()
    else:
        reason = "no GROQ_API_KEY" if not key else "LangChain not installed"
        print(f"OFFLINE mode ({reason}). Using lexicon mock classifier so "
              "the pipeline + scoring run. Numbers below are NOT real model "
              "results -- run the one-liner in the docstring for live ones.")
        invoke = None

    results = []
    for technique in ("zero_shot", "few_shot", "cot"):
        results.append(run_technique(technique, invoke, live))

    out_path = os.path.join("outputs", "task1_results.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)

    print("\nTechnique     | Accuracy | Avg latency | ~Tokens | Cost")
    print("-" * 58)
    for r in results:
        print("{:<13} | {:>7.1%}  | {:>9.4f}s | {:>7} | $0 (free)"
              .format(r["technique"], r["accuracy"],
                      r["avg_latency_s"], r["approx_total_tokens"]))
    print(f"\nSaved detailed results to {out_path}")
    print("Best-use guide: zero-shot = simple/cheap; few-shot = consistent "
          "labels & format; CoT = harder, ambiguous cases needing reasoning.")


if __name__ == "__main__":
    main()
