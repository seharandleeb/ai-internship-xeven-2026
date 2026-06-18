"""Day 24 - Task 2: First FastAPI application.

A minimal API demonstrating a health check, a path parameter with an
optional query parameter, and a POST endpoint with Pydantic body
validation. Run with:
    uvicorn main:app --reload
from inside the day24/api/ folder.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 24 API", version="0.1.0")

# In-memory store so POST has somewhere to put things (resets on
# restart; a real app would use a database).
ITEMS = {
    1: {"name": "Notebook", "price": 3.5},
    2: {"name": "Pen", "price": 1.0},
}


class Item(BaseModel):
    """Shape of an item in a request body."""

    name: str
    price: float


@app.get("/health")
def health():
    """Report that the service is running."""
    return {"status": "ok"}


@app.get("/items/{item_id}")
def get_item(item_id: int, q: str | None = None):
    """Return one item by id, with an optional query echo."""
    item = ITEMS.get(item_id)
    if item is None:
        return {"error": "item not found", "item_id": item_id}
    result = {"item_id": item_id, "item": item}
    if q is not None:
        result["q"] = q
    return result


@app.post("/items")
def create_item(item: Item):
    """Create a new item and return it with its assigned id."""
    new_id = max(ITEMS) + 1 if ITEMS else 1
    ITEMS[new_id] = {"name": item.name, "price": item.price}
    return {"item_id": new_id, "item": ITEMS[new_id]}