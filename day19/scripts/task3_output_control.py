"""Day 19 - Task 3: Advanced Output Control.

Three output-control prompts plus the local validators that enforce them:

  1. JSON output  -> exact schema; validated with a minimal type/required
     checker and a robust extractor that survives code fences / prose.
  2. Markdown table -> fixed columns with alignment; a structural checker
     verifies the header, the separator row, and a consistent column count
     across a varying number of data rows.
  3. Code generation -> language, style, and docstring requirements stated
     in the prompt; a light static check confirms a def + docstring.

A robustness suite runs the validators on good, edge-case, and malformed
inputs to prove they hold up. Live Groq/LCEL calls are gated behind
GROQ_API_KEY so the script runs and is fully verifiable offline.

Run from inside day19/scripts/. Full live run on your machine:
    uv run python task3_output_control.py
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
    from langchain_core.output_parsers import JsonOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_groq import ChatGroq
    LANGCHAIN_OK = True
except ImportError:  # pragma: no cover - offline fallback
    LANGCHAIN_OK = False

MODEL_NAME = "llama-3.3-70b-versatile"

PERSON_SCHEMA = {
    "type": "object",
    "required": ["name", "age", "skills"],
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "skills": {"type": "array"},
    },
}

JSON_SYSTEM = (
    "You output ONLY valid JSON matching the requested schema. No prose, no "
    "markdown fences. Keys and types must match exactly."
)
JSON_USER = (
    "Return a JSON object with keys: name (string), age (integer), "
    "skills (array of strings). Source: {text}"
)

TABLE_SYSTEM = (
    "You output ONLY a GitHub-flavored markdown table. First row is the "
    "header, second row is the alignment separator, then one row per item. "
    "Every row must have the same number of columns."
)
TABLE_USER = (
    "Build a markdown table with columns | Item | Qty | Price | for:\n{text}"
)

CODE_SYSTEM = (
    "You are a senior Python engineer. Output ONLY a single Python code "
    "block. Follow PEP 8, include a docstring, and use type hints."
)
CODE_USER = (
    "Write a Python function for this spec: {text}"
)

_PY_TYPES = {
    "string": str,
    "integer": int,
    "number": (int, float),
    "array": list,
    "object": dict,
    "boolean": bool,
}


def extract_json(raw):
    """Pull a JSON object from text that may include fences or prose."""
    cleaned = raw.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(cleaned[start:end + 1])
        raise


def validate_schema(obj, schema):
    """Minimal validator: required keys + declared JSON types. Returns []."""
    errors = []
    if not isinstance(obj, dict):
        return ["root is not an object"]
    for req in schema.get("required", []):
        if req not in obj:
            errors.append(f"missing required key: {req}")
    for key, spec in schema.get("properties", {}).items():
        if key in obj:
            expected = _PY_TYPES.get(spec.get("type"))
            if expected and not isinstance(obj[key], expected):
                errors.append(
                    f"key '{key}' should be {spec['type']}")
            if spec.get("type") == "integer" and isinstance(obj[key], bool):
                errors.append(f"key '{key}' should be integer, got bool")
    return errors


def is_valid_markdown_table(md):
    """Validate header, alignment separator, and equal column counts."""
    rows = [ln for ln in md.strip().splitlines() if ln.strip()]
    if len(rows) < 2:
        return False, "need at least a header and separator row"

    def cells(line):
        return [c.strip() for c in line.strip().strip("|").split("|")]

    header = cells(rows[0])
    ncol = len(header)
    sep = cells(rows[1])
    if len(sep) != ncol:
        return False, "separator column count differs from header"
    sep_ok = all(re.fullmatch(r":?-{3,}:?", s) for s in sep)
    if not sep_ok:
        return False, "separator row is malformed"
    for i, row in enumerate(rows[2:], start=3):
        if len(cells(row)) != ncol:
            return False, f"row {i} has wrong column count"
    return True, f"valid table with {ncol} columns, {len(rows) - 2} rows"


def looks_like_documented_function(code):
    """Light check: a def, a docstring, and at least one type hint."""
    has_def = bool(re.search(r"\bdef\s+\w+\s*\(", code))
    has_doc = '"""' in code or "'''" in code
    has_hint = "->" in code or re.search(r":\s*\w+\s*[,)=]", code)
    return has_def and has_doc and bool(has_hint)


def robustness_suite():
    """Run validators on good / edge / malformed inputs; return results."""
    cases = []

    # --- JSON cases ---
    good_json = '{"name": "Sara", "age": 23, "skills": ["python"]}'
    fenced = "```json\n" + good_json + "\n```"
    prose = "Here is the object: " + good_json + " hope it helps!"
    bad_type = '{"name": "Sara", "age": "23", "skills": ["python"]}'
    missing = '{"name": "Sara", "skills": []}'
    for label, raw, expect_ok in [
        ("json_clean", good_json, True),
        ("json_fenced", fenced, True),
        ("json_with_prose", prose, True),
        ("json_wrong_type", bad_type, False),
        ("json_missing_key", missing, False),
    ]:
        try:
            obj = extract_json(raw)
            errs = validate_schema(obj, PERSON_SCHEMA)
            ok = not errs
        except json.JSONDecodeError:
            ok, errs = False, ["unparseable JSON"]
        cases.append({
            "case": label, "passed": ok == expect_ok,
            "valid": ok, "detail": errs or "ok",
        })

    # --- Markdown table cases ---
    good_tbl = ("| Item | Qty | Price |\n| --- | ---: | ---: |\n"
                "| Pen | 3 | 1.50 |\n| Mug | 1 | 8.00 |")
    one_row = "| Item | Qty | Price |\n| --- | --- | --- |\n| Pen | 3 | 1.5 |"
    ragged = ("| Item | Qty | Price |\n| --- | --- | --- |\n| Pen | 3 |")
    no_sep = "| Item | Qty | Price |\n| Pen | 3 | 1.50 |"
    for label, md, expect_ok in [
        ("table_good", good_tbl, True),
        ("table_single_row", one_row, True),
        ("table_ragged_row", ragged, False),
        ("table_missing_separator", no_sep, False),
    ]:
        ok, detail = is_valid_markdown_table(md)
        cases.append({
            "case": label, "passed": ok == expect_ok,
            "valid": ok, "detail": detail,
        })

    # --- Code-generation cases ---
    good_code = (
        "def add(a: int, b: int) -> int:\n"
        '    """Return the sum of a and b."""\n'
        "    return a + b\n"
    )
    no_doc = "def add(a: int, b: int) -> int:\n    return a + b\n"
    for label, code, expect_ok in [
        ("code_documented", good_code, True),
        ("code_no_docstring", no_doc, False),
    ]:
        ok = looks_like_documented_function(code)
        cases.append({
            "case": label, "passed": ok == expect_ok,
            "valid": ok, "detail": "checked def/docstring/hint",
        })

    return cases


def main():
    os.makedirs("outputs", exist_ok=True)
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    live = bool(key) and LANGCHAIN_OK

    results = robustness_suite()
    passed = sum(c["passed"] for c in results)
    out_path = os.path.join("outputs", "task3_robustness.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)

    print("Output-control robustness suite (offline, no API needed):")
    print("-" * 56)
    for c in results:
        mark = "PASS" if c["passed"] else "FAIL"
        print(f"[{mark}] {c['case']:<24} valid={c['valid']}")
    print(f"\n{passed}/{len(results)} validator cases behaved as expected.")
    print(f"Saved -> {out_path}")

    if live:
        print(f"\nLIVE mode: requesting schema-bound JSON from Groq "
              f"{MODEL_NAME}...")
        prompt = ChatPromptTemplate.from_messages([
            ("system", JSON_SYSTEM),
            ("human", JSON_USER),
        ])
        model = ChatGroq(model=MODEL_NAME, temperature=0)
        chain = prompt | model | JsonOutputParser()
        obj = chain.invoke({"text": "Sara, 23, codes in Python and Rust."})
        errs = validate_schema(obj, PERSON_SCHEMA)
        print("Model JSON:", obj)
        print("Schema errors:", errs or "none")
    else:
        reason = "no GROQ_API_KEY" if not key else "LangChain not installed"
        print(f"\nOFFLINE mode ({reason}): skipped live generation. The "
              "validators above are exactly what gate the live outputs.")


if __name__ == "__main__":
    main()
