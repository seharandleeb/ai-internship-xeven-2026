"""Day 20 - Task 1: Pydantic Model Suite.

Defines two Pydantic v2 models (Person, Product) with custom field
validators, then proves that valid data constructs cleanly and that
each invalid case raises ``ValidationError``. A small JSON report of
the test battery is written to ``outputs/`` so the run leaves an
artifact behind.

Run from inside ``day20/scripts/``:
    uv run python task1_pydantic_models.py
"""

import json
import os
import re
from typing import Callable, List

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    field_validator,
)

# Dependency-free email pattern. We deliberately use a regex validator
# instead of pydantic's EmailStr so we do not pull in the extra
# email-validator package (see the Day 20 stack notes).
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Person(BaseModel):
    """A person with a small public profile."""

    name: str
    age: int
    email: str
    hobbies: List[str] = Field(default_factory=list)

    @field_validator("email")
    @classmethod
    def email_must_be_valid(cls, value: str) -> str:
        """Reject anything that does not look like an address."""
        if not EMAIL_RE.match(value):
            raise ValueError("email is not a valid address")
        return value

    @field_validator("age")
    @classmethod
    def age_must_be_positive(cls, value: int) -> int:
        """Enforce age > 0."""
        if value <= 0:
            raise ValueError("age must be greater than 0")
        return value


class Product(BaseModel):
    """A catalogue product."""

    id: int
    name: str
    price: float
    in_stock: bool = True
    tags: List[str] = Field(default_factory=list)

    @field_validator("price")
    @classmethod
    def price_must_be_non_negative(cls, value: float) -> float:
        """Enforce price >= 0."""
        if value < 0:
            raise ValueError("price must be >= 0")
        return value


def run_case(label: str, builder: Callable[[], BaseModel],
             should_pass: bool) -> dict:
    """Run one construction attempt and record what happened.

    ``should_pass`` is what we expect: ``True`` means the data is
    valid, ``False`` means a validator should reject it.
    """
    record = {
        "case": label,
        "expected": "pass" if should_pass else "fail",
    }
    try:
        obj = builder()
        record["outcome"] = "constructed"
        record["behaved_as_expected"] = should_pass is True
        record["detail"] = obj.model_dump()
    except ValidationError as exc:
        record["outcome"] = "ValidationError"
        record["behaved_as_expected"] = should_pass is False
        record["detail"] = exc.errors()[0]["msg"]
    return record


def build_cases() -> List[tuple]:
    """Return the (label, builder, should_pass) test battery."""
    return [
        (
            "Person: valid",
            lambda: Person(
                name="Sehar",
                age=22,
                email="sehar@example.com",
                hobbies=["reading", "coding"],
            ),
            True,
        ),
        (
            "Person: bad email format",
            lambda: Person(
                name="Sehar",
                age=22,
                email="not-an-email",
            ),
            False,
        ),
        (
            "Person: age == 0",
            lambda: Person(
                name="Sehar",
                age=0,
                email="sehar@example.com",
            ),
            False,
        ),
        (
            "Person: negative age",
            lambda: Person(
                name="Sehar",
                age=-5,
                email="sehar@example.com",
            ),
            False,
        ),
        (
            "Product: valid",
            lambda: Product(
                id=1,
                name="Keyboard",
                price=49.99,
                tags=["peripherals"],
            ),
            True,
        ),
        (
            "Product: price == 0 (boundary, allowed)",
            lambda: Product(id=2, name="Free sample", price=0.0),
            True,
        ),
        (
            "Product: negative price",
            lambda: Product(id=3, name="Broken", price=-1.0),
            False,
        ),
    ]


def main() -> None:
    """Run the battery, write a report, and demo a JSON round-trip."""
    os.makedirs("outputs", exist_ok=True)

    results = [run_case(*case) for case in build_cases()]
    correct = sum(1 for r in results if r["behaved_as_expected"])
    total = len(results)

    summary = {
        "total_cases": total,
        "cases_behaving_as_expected": correct,
        "results": results,
    }
    out_path = os.path.join("outputs", "task1_validation_report.json")
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    print(f"Task 1: {correct}/{total} cases behaved as expected.")
    print(f"Report written to {out_path}")

    # JSON export + re-load round-trip on a valid model.
    person = Person(
        name="Sehar",
        age=22,
        email="sehar@example.com",
        hobbies=["reading", "coding"],
    )
    restored = Person.model_validate_json(person.model_dump_json())
    assert restored == person
    print("Person JSON round-trip OK:", restored.model_dump())


if __name__ == "__main__":
    main()
