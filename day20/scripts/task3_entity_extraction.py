"""Day 20 - Task 3: Multi-Entity Extraction System.

Defines nested Pydantic models (``Company`` -> ``Employee[]``),
extracts entities from auto-created press releases, builds a small
knowledge graph (company -> employee -> skills), exports it to JSON,
and scores the extraction against known gold labels.

The live path uses ``ChatGroq(...).with_structured_output(Company)``
(LangChain 1.x). The sandbox uses a deterministic offline stub that
injects a few controlled, documented errors so the accuracy metric
is exercised honestly (it does not trivially report 100%).

Live run (reads GROQ_API_KEY from .env):
    uv run python task3_entity_extraction.py --live

Offline run (default):
    uv run python task3_entity_extraction.py
"""

import argparse
import json
import os
from typing import Callable, List

from pydantic import BaseModel, Field


class Employee(BaseModel):
    """A single employee mentioned in a company text."""

    name: str
    title: str
    department: str
    skills: List[str] = Field(default_factory=list)


class Company(BaseModel):
    """A company with its located staff."""

    name: str
    location: str
    employees: List[Employee] = Field(default_factory=list)


# Gold labels: the ground truth we score extraction against.
GOLD: List[dict] = [
    {
        "name": "NimbusAI",
        "location": "Lahore, PK",
        "employees": [
            {"name": "Ayesha Tariq", "title": "ML Engineer",
             "department": "Research",
             "skills": ["pytorch", "nlp", "mlops"]},
            {"name": "Bilal Sheikh", "title": "Data Engineer",
             "department": "Platform",
             "skills": ["spark", "airflow", "sql"]},
        ],
    },
    {
        "name": "Cobalt Robotics",
        "location": "Austin, US",
        "employees": [
            {"name": "Dana Reyes", "title": "Robotics Lead",
             "department": "Hardware",
             "skills": ["ros", "control-systems", "c++"]},
            {"name": "Evan Park", "title": "Perception Engineer",
             "department": "Vision",
             "skills": ["opencv", "slam", "python"]},
        ],
    },
    {
        "name": "Larkspur Health",
        "location": "Berlin, DE",
        "employees": [
            {"name": "Farah Noor", "title": "Clinical NLP Scientist",
             "department": "Research",
             "skills": ["transformers", "ehr", "python"]},
        ],
    },
]


def build_press_releases() -> List[str]:
    """Auto-create one unstructured press release per gold company."""
    releases: List[str] = []
    for company in GOLD:
        lines = [
            f"{company['name']}, based in {company['location']}, "
            "announced its core team today."
        ]
        for emp in company["employees"]:
            skills = ", ".join(emp["skills"])
            lines.append(
                f"{emp['name']} joins as {emp['title']} in the "
                f"{emp['department']} department, bringing {skills}."
            )
        releases.append(" ".join(lines))
    return releases


def offline_extract(company_gold: dict) -> dict:
    """Deterministic stand-in for the LLM extractor.

    Injects three documented errors so accuracy is realistic:
      - NimbusAI: drop Ayesha's "mlops" skill   (a recall miss).
      - NimbusAI: add a spurious "kafka" to Bilal (a precision miss).
      - Cobalt:   read Dana's title as "Robotics Engineer" (wrong).
    Larkspur is extracted perfectly.
    """
    out = json.loads(json.dumps(company_gold))  # deep copy
    if out["name"] == "NimbusAI":
        for emp in out["employees"]:
            if emp["name"] == "Ayesha Tariq":
                emp["skills"] = [s for s in emp["skills"]
                                 if s != "mlops"]
            if emp["name"] == "Bilal Sheikh":
                emp["skills"] = emp["skills"] + ["kafka"]
    if out["name"] == "Cobalt Robotics":
        for emp in out["employees"]:
            if emp["name"] == "Dana Reyes":
                emp["title"] = "Robotics Engineer"
    return out


def build_live_extractor() -> Callable[[str], dict]:
    """Build the real ChatGroq structured-output extractor."""
    from dotenv import load_dotenv
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_groq import ChatGroq

    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY not found in environment/.env")

    model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    structured = model.with_structured_output(Company)
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Extract the company, its location, and every employee with "
         "their title, department, and skills from the text."),
        ("human", "{text}"),
    ])
    chain = prompt | structured

    def _extract(text: str) -> dict:
        return chain.invoke({"text": text}).model_dump()

    return _extract


def to_graph(companies: List[Company]) -> dict:
    """Turn validated companies into a nested knowledge graph."""
    graph: dict = {}
    for company in companies:
        graph[company.name] = {
            "location": company.location,
            "employees": {
                emp.name: {
                    "title": emp.title,
                    "department": emp.department,
                    "skills": emp.skills,
                }
                for emp in company.employees
            },
        }
    return graph


def score(extracted: List[Company]) -> dict:
    """Score extraction against GOLD.

    Field accuracy counts leaf facts: each employee contributes a
    correct/incorrect title and department (2 facts), plus one fact
    per gold skill found. Skill precision/recall/F1 are reported
    separately so over- and under-extraction are both visible. The
    metric is chosen for this nested shape rather than copied from a
    textbook - skills are a set per employee, so set overlap is the
    natural fit.
    """
    by_name = {c.name: c for c in extracted}
    total_facts = 0
    correct_facts = 0
    skill_tp = 0
    skill_fp = 0
    skill_fn = 0

    for gold_company in GOLD:
        got = by_name.get(gold_company["name"])
        got_emps = {e.name: e for e in got.employees} if got else {}
        for gold_emp in gold_company["employees"]:
            got_emp = got_emps.get(gold_emp["name"])
            # title + department are two leaf facts.
            total_facts += 2
            if got_emp is not None:
                if got_emp.title == gold_emp["title"]:
                    correct_facts += 1
                if got_emp.department == gold_emp["department"]:
                    correct_facts += 1
            gold_skills = set(gold_emp["skills"])
            got_skills = set(got_emp.skills) if got_emp else set()
            # one leaf fact per gold skill (correct if found).
            total_facts += len(gold_skills)
            correct_facts += len(gold_skills & got_skills)
            skill_tp += len(gold_skills & got_skills)
            skill_fp += len(got_skills - gold_skills)
            skill_fn += len(gold_skills - got_skills)

    precision = skill_tp / (skill_tp + skill_fp) if skill_tp else 0.0
    recall = skill_tp / (skill_tp + skill_fn) if skill_tp else 0.0
    f1 = (2 * precision * recall / (precision + recall)
          if (precision + recall) else 0.0)

    return {
        "field_accuracy": round(correct_facts / total_facts, 4),
        "correct_facts": correct_facts,
        "total_facts": total_facts,
        "skill_precision": round(precision, 4),
        "skill_recall": round(recall, 4),
        "skill_f1": round(f1, 4),
    }


def main() -> None:
    """Extract, validate, build the graph, and score it."""
    parser = argparse.ArgumentParser(description="Entity extraction")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Use live ChatGroq instead of the offline stub.",
    )
    args = parser.parse_args()

    os.makedirs("outputs", exist_ok=True)
    releases = build_press_releases()
    extractor = build_live_extractor() if args.live else None

    companies: List[Company] = []
    for index, gold_company in enumerate(GOLD):
        if extractor is not None:
            data = extractor(releases[index])
        else:
            data = offline_extract(gold_company)
        companies.append(Company(**data))  # validates every record

    graph = to_graph(companies)
    metrics = score(companies)

    graph_path = os.path.join("outputs", "task3_knowledge_graph.json")
    with open(graph_path, "w", encoding="utf-8") as handle:
        json.dump(graph, handle, indent=2)

    metrics_path = os.path.join("outputs", "task3_accuracy_report.json")
    with open(metrics_path, "w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)

    mode = "LIVE (Groq)" if args.live else "OFFLINE (stub)"
    print(f"Task 3 [{mode}]")
    print(f"  Companies extracted : {len(companies)}")
    print(f"  Employees extracted : "
          f"{sum(len(c.employees) for c in companies)}")
    print(f"  Field accuracy      : "
          f"{metrics['field_accuracy'] * 100:.1f}% "
          f"({metrics['correct_facts']}/{metrics['total_facts']})")
    print(f"  Skill P / R / F1    : "
          f"{metrics['skill_precision']:.2f} / "
          f"{metrics['skill_recall']:.2f} / {metrics['skill_f1']:.2f}")
    print(f"  Graph   -> {graph_path}")
    print(f"  Metrics -> {metrics_path}")


if __name__ == "__main__":
    main()
