"""
Day 10 - Task 2: Product Inventory Manager
==========================================
Demonstrates dictionary-based inventory management, category analytics,
and JSON report export.
Connection to AI Engineering: Model registries, dataset catalogs, and
feature stores all use this pattern — keyed records with typed fields,
aggregation queries, and serialised snapshots.

Author: Sehar Andleeb
Internship: Xeven Solutions, Lahore — AI Engineering
Mentor: Mubashir Sir (Sr. Machine Learning Engineer)
Date: Day 10 of 30-Day AI Engineering Roadmap
"""

import json
import os
from collections import defaultdict
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
INVENTORY_FILE = "inventory.json"
REPORT_FILE = "inventory_report.json"
LOW_STOCK_THRESHOLD = 10          # units below this trigger an alert
CURRENCY = "PKR"


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------

def load_inventory(filepath: str = INVENTORY_FILE) -> dict:
    """
    Load product inventory from a JSON file.

    Args:
        filepath: Path to the JSON inventory file.

    Returns:
        Dictionary mapping product IDs to product records.
    """
    if not os.path.exists(filepath):
        return {}

    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        print(f"[INFO] Loaded {len(data)} product(s) from '{filepath}'.")
        return data
    except (json.JSONDecodeError, OSError) as exc:
        print(f"[ERROR] Cannot read '{filepath}': {exc}")
        return {}


def save_inventory(inventory: dict, filepath: str = INVENTORY_FILE) -> bool:
    """
    Persist inventory to a JSON file.

    Args:
        inventory: The in-memory inventory dictionary.
        filepath: Destination file path.

    Returns:
        True on success, False on failure.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump(inventory, fh, indent=4, ensure_ascii=False)
        print(f"[INFO] Inventory saved to '{filepath}'.")
        return True
    except OSError as exc:
        print(f"[ERROR] Cannot save inventory: {exc}")
        return False


# ---------------------------------------------------------------------------
# CRUD operations
# ---------------------------------------------------------------------------

def add_product(
    inventory: dict,
    product_id: str,
    name: str,
    price: float,
    quantity: int,
    category: str,
) -> bool:
    """
    Add a new product to the inventory.

    Args:
        inventory: In-memory inventory dict (modified in-place).
        product_id: Unique product code (e.g. "P001").
        name: Human-readable product name.
        price: Unit price in PKR.
        quantity: Initial stock quantity.
        category: Product category string (e.g. "Electronics").

    Returns:
        True if added, False if the product_id already exists.
    """
    if product_id in inventory:
        print(f"[WARN] Product '{product_id}' already exists.")
        return False

    if price < 0 or quantity < 0:
        print("[ERROR] Price and quantity must be non-negative.")
        return False

    inventory[product_id] = {
        "name": name,
        "price": price,
        "quantity": quantity,
        "category": category,
    }
    print(f"[INFO] Added product: {name} (ID: {product_id}, Category: {category}).")
    return True


def update_stock(
    inventory: dict,
    product_id: str,
    delta: int,
) -> bool:
    """
    Adjust stock quantity for an existing product.

    Args:
        inventory: In-memory inventory dict.
        product_id: Target product identifier.
        delta: Units to add (positive) or remove (negative).

    Returns:
        True on success, False if product not found or stock goes negative.
    """
    if product_id not in inventory:
        print(f"[ERROR] Product '{product_id}' not found.")
        return False

    new_qty = inventory[product_id]["quantity"] + delta
    if new_qty < 0:
        print(
            f"[ERROR] Insufficient stock for '{product_id}'. "
            f"Available: {inventory[product_id]['quantity']}, Requested change: {delta}."
        )
        return False

    inventory[product_id]["quantity"] = new_qty
    action = "Restocked" if delta >= 0 else "Sold"
    print(
        f"[INFO] {action} {abs(delta)} unit(s) of "
        f"'{inventory[product_id]['name']}'. New stock: {new_qty}."
    )
    return True


# ---------------------------------------------------------------------------
# Query / analysis functions
# ---------------------------------------------------------------------------

def search_by_category(inventory: dict, category: str) -> dict:
    """
    Return all products that belong to the specified category.

    Args:
        inventory: In-memory inventory dict.
        category: Category name to filter by (case-insensitive).

    Returns:
        Sub-dictionary of matching products.
    """
    category_lower = category.lower()
    # Dict comprehension — O(n)
    matches = {
        pid: info
        for pid, info in inventory.items()
        if info["category"].lower() == category_lower
    }
    print(f"[INFO] Found {len(matches)} product(s) in category '{category}'.")
    return matches


def low_stock_alert(
    inventory: dict,
    threshold: int = LOW_STOCK_THRESHOLD,
) -> list:
    """
    Identify products with stock at or below the threshold.

    Args:
        inventory: In-memory inventory dict.
        threshold: Maximum quantity that triggers an alert.

    Returns:
        Sorted list of (product_id, name, quantity) tuples.
    """
    alerts = [
        (pid, info["name"], info["quantity"])
        for pid, info in inventory.items()
        if info["quantity"] <= threshold
    ]
    # Sort by quantity ascending so most critical items are first
    alerts.sort(key=lambda x: x[2])
    return alerts


def calculate_total_inventory_value(inventory: dict) -> float:
    """
    Compute the total monetary value of all stock.

    Args:
        inventory: In-memory inventory dict.

    Returns:
        Sum of (price × quantity) across all products.
    """
    total = sum(
        info["price"] * info["quantity"]
        for info in inventory.values()
    )
    return round(total, 2)


def average_price_per_category(inventory: dict) -> dict:
    """
    Calculate the mean unit price for each product category.

    Args:
        inventory: In-memory inventory dict.

    Returns:
        Dict mapping category names to their average unit price.
    """
    # defaultdict accumulates (total_price, count) tuples
    category_data: dict = defaultdict(lambda: {"total": 0.0, "count": 0})

    for info in inventory.values():
        cat = info["category"]
        category_data[cat]["total"] += info["price"]
        category_data[cat]["count"] += 1

    return {
        cat: round(data["total"] / data["count"], 2)
        for cat, data in category_data.items()
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def export_inventory_report(inventory: dict, filepath: str = REPORT_FILE) -> bool:
    """
    Build a structured summary report and export it as JSON.

    Report includes: total_products, total_value, categories, low_stock_items,
    category_avg_prices, and the full product list.

    Args:
        inventory: In-memory inventory dict.
        filepath: Output JSON path.

    Returns:
        True on successful write.
    """
    low_stock = low_stock_alert(inventory)
    category_avgs = average_price_per_category(inventory)

    report = {
        "summary": {
            "total_products": len(inventory),
            "total_inventory_value_pkr": calculate_total_inventory_value(inventory),
            "categories": list(category_avgs.keys()),
            "low_stock_count": len(low_stock),
        },
        "category_average_prices": category_avgs,
        "low_stock_items": [
            {"product_id": pid, "name": name, "quantity": qty}
            for pid, name, qty in low_stock
        ],
        "products": inventory,
    }

    try:
        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=4, ensure_ascii=False)
        print(f"[INFO] Inventory report exported to '{filepath}'.")
        return True
    except OSError as exc:
        print(f"[ERROR] Cannot export report: {exc}")
        return False


def print_inventory_summary(inventory: dict) -> None:
    """
    Display a formatted console summary of the inventory.

    Args:
        inventory: In-memory inventory dict.
    """
    print("\n" + "=" * 70)
    print(f"{'PRODUCT INVENTORY SUMMARY':^70}")
    print("=" * 70)
    print(f"{'ID':<8} {'Name':<25} {'Category':<15} {'Price':>10} {'Stock':>6}")
    print("-" * 70)

    for pid, info in sorted(inventory.items()):
        flag = " ⚠" if info["quantity"] <= LOW_STOCK_THRESHOLD else ""
        print(
            f"{pid:<8} {info['name']:<25} {info['category']:<15} "
            f"{info['price']:>9,.0f} {info['quantity']:>6}{flag}"
        )

    # Footer stats
    total_value = calculate_total_inventory_value(inventory)
    cat_avgs = average_price_per_category(inventory)

    print("-" * 70)
    print(f"  Total inventory value: {CURRENCY} {total_value:,.2f}")
    print(f"  Total SKUs: {len(inventory)}")
    print("\n  Average price by category:")
    for cat, avg in sorted(cat_avgs.items()):
        print(f"    {cat:<20} {CURRENCY} {avg:,.2f}")

    # Low stock section
    alerts = low_stock_alert(inventory)
    if alerts:
        print(f"\n  ⚠  LOW STOCK ALERTS ({len(alerts)} item(s)):")
        for pid, name, qty in alerts:
            print(f"    [{pid}] {name:<25} — only {qty} unit(s) remaining")

    print("=" * 70 + "\n")


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("╔══════════════════════════════════════════╗")
    print("║   Day 10 — Product Inventory Manager     ║")
    print("╚══════════════════════════════════════════╝\n")

    # ── Load or seed inventory ───────────────────────────────────────────────
    inventory = load_inventory()

    if not inventory:
        print("[DEMO] Seeding sample inventory...\n")

        products = [
            ("P001", "GPU RTX 4090",          350_000, 5,  "Electronics"),
            ("P002", "Mechanical Keyboard",    12_500, 30,  "Peripherals"),
            ("P003", "USB-C Hub (7-in-1)",      4_200, 8,   "Peripherals"),
            ("P004", "27\" 4K Monitor",         85_000, 12, "Electronics"),
            ("P005", "Laptop Stand",             2_800, 3,  "Accessories"),
            ("P006", "Noise-Cancelling Headset", 18_000, 20, "Peripherals"),
            ("P007", "NVMe SSD 1TB",             22_000, 15, "Storage"),
            ("P008", "16GB DDR5 RAM",            14_500, 9,  "Storage"),
            ("P009", "Webcam 4K",                9_500, 7,  "Peripherals"),
            ("P010", "RGB Mouse Pad XL",          1_200, 50, "Accessories"),
        ]
        for pid, name, price, qty, cat in products:
            add_product(inventory, pid, name, price, qty, cat)

    # ── Stock updates ────────────────────────────────────────────────────────
    print("\n--- Stock operations ---")
    update_stock(inventory, "P001", -2)    # sold 2 GPUs
    update_stock(inventory, "P003", 20)    # restocked hubs
    update_stock(inventory, "P005", -2)    # sold 2 stands

    # ── Category search ──────────────────────────────────────────────────────
    print("\n--- Category search: Peripherals ---")
    peripherals = search_by_category(inventory, "Peripherals")
    for pid, info in peripherals.items():
        print(f"  {pid}: {info['name']} @ PKR {info['price']:,} (qty: {info['quantity']})")

    # ── Print full summary ───────────────────────────────────────────────────
    print_inventory_summary(inventory)

    # ── Export JSON report ───────────────────────────────────────────────────
    export_inventory_report(inventory)

    # ── Persist inventory ────────────────────────────────────────────────────
    save_inventory(inventory)
    print("[DONE] product_inventory_manager.py complete.\n")
