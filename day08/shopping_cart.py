"""
shopping_cart.py
================
Day 8 - Task 2: Shopping Cart System
Week 2: Python Data Structures & Algorithms

Demonstrates list operations with structured data: storing items as
nested lists, CRUD operations, discount logic, itemized receipt
printing, and list slicing for recently added items.

Author  : Sehar Andleeb
Mentor  : Mubashir Sir (Sr. Machine Learning Engineer)
Company : Xeven Solutions
Date    : 2026
"""

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DISCOUNT_THRESHOLD = 100.00   # cart total above this triggers a discount
DISCOUNT_RATE      = 0.10     # 10% discount
RECENTLY_ADDED_N   = 3        # how many "recent" items to show via slicing

# Each item in the cart is stored as a list: [name, price, quantity]
ITEM_NAME     = 0
ITEM_PRICE    = 1
ITEM_QUANTITY = 2


# ---------------------------------------------------------------------------
# Core Functions
# ---------------------------------------------------------------------------

def add_item(cart: list, name: str, price: float, quantity: int = 1) -> None:
    """Add a new item to the cart, or increase quantity if it already exists.

    Args:
        cart     : The shopping cart (list of [name, price, quantity] lists).
        name     : Product name.
        price    : Unit price in dollars.
        quantity : Number of units to add (default: 1).

    Raises:
        ValueError: If price or quantity are not positive numbers.
    """
    if price <= 0:
        raise ValueError(f"Price must be positive. Got: {price}")
    if quantity <= 0:
        raise ValueError(f"Quantity must be positive. Got: {quantity}")

    # check if item already exists — update quantity instead of duplicating
    for item in cart:
        if item[ITEM_NAME].lower() == name.lower():
            item[ITEM_QUANTITY] += quantity
            print(f"  ✓ Updated '{name}' quantity → {item[ITEM_QUANTITY]}")
            return

    # item not found — append as a new entry
    cart.append([name, price, quantity])
    print(f"  ✓ Added '{name}'  ${price:.2f} x {quantity}")


def remove_item(cart: list, name: str) -> bool:
    """Remove an item completely from the cart by name.

    Args:
        cart : The shopping cart.
        name : Name of the item to remove.

    Returns:
        True if item was found and removed, False otherwise.
    """
    for i, item in enumerate(cart):
        if item[ITEM_NAME].lower() == name.lower():
            cart.pop(i)   # remove by index so both name and data are dropped
            print(f"  ✓ Removed '{name}' from cart")
            return True

    print(f"  ✗ Item '{name}' not found in cart.")
    return False


def update_quantity(cart: list, name: str, new_quantity: int) -> bool:
    """Set a new quantity for an existing cart item.

    Args:
        cart         : The shopping cart.
        name         : Name of the item to update.
        new_quantity : Replacement quantity. Pass 0 to effectively remove.

    Returns:
        True if updated successfully, False if item not found.

    Raises:
        ValueError: If new_quantity is negative.
    """
    if new_quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    for item in cart:
        if item[ITEM_NAME].lower() == name.lower():
            old_qty = item[ITEM_QUANTITY]
            item[ITEM_QUANTITY] = new_quantity
            print(f"  ✓ Updated '{name}' quantity: {old_qty} → {new_quantity}")
            return True

    print(f"  ✗ Item '{name}' not found in cart.")
    return False


def calculate_subtotal(cart: list) -> float:
    """Calculate the raw total before any discounts.

    Args:
        cart: The shopping cart.

    Returns:
        Sum of (price × quantity) for every item.
    """
    # list comprehension: compute each line total, then sum them all
    return sum(item[ITEM_PRICE] * item[ITEM_QUANTITY] for item in cart)


def calculate_total(cart: list) -> tuple:
    """Calculate the final total, applying a discount if eligible.

    A 10% discount is applied when the subtotal exceeds $100.

    Args:
        cart: The shopping cart.

    Returns:
        A tuple of (subtotal, discount_amount, final_total).
    """
    subtotal = calculate_subtotal(cart)

    # apply discount only when subtotal crosses the threshold
    if subtotal > DISCOUNT_THRESHOLD:
        discount_amount = subtotal * DISCOUNT_RATE
    else:
        discount_amount = 0.0

    final_total = subtotal - discount_amount
    return (subtotal, discount_amount, final_total)


def get_recently_added(cart: list, n: int = RECENTLY_ADDED_N) -> list:
    """Return the last N items added using list slicing.

    Items are stored in insertion order, so the most recently added
    items are at the end of the list.

    Args:
        cart : The shopping cart.
        n    : Number of recent items to return (default: 3).

    Returns:
        A sliced list containing the last n items.
    """
    # negative slicing: cart[-n:] grabs the last n elements
    return cart[-n:]


# ---------------------------------------------------------------------------
# Display Helpers
# ---------------------------------------------------------------------------

def display_cart(cart: list) -> None:
    """Print the full cart contents in a clean table format.

    Args:
        cart: The shopping cart.
    """
    if not cart:
        print("  (Cart is empty)")
        return

    print(f"\n  {'Item':<22} {'Price':>8} {'Qty':>5} {'Subtotal':>10}")
    print(f"  {'-'*22} {'-'*8} {'-'*5} {'-'*10}")
    for item in cart:
        line_total = item[ITEM_PRICE] * item[ITEM_QUANTITY]
        print(f"  {item[ITEM_NAME]:<22} ${item[ITEM_PRICE]:>7.2f} {item[ITEM_QUANTITY]:>5} ${line_total:>9.2f}")
    print()


def print_receipt(cart: list) -> None:
    """Print a fully itemized receipt with discount and final total.

    Args:
        cart: The shopping cart.
    """
    subtotal, discount, final_total = calculate_total(cart)

    print("\n" + "=" * 45)
    print("         XEVEN SOLUTIONS STORE")
    print("              RECEIPT")
    print("=" * 45)

    # itemized lines
    for item in cart:
        line_total = item[ITEM_PRICE] * item[ITEM_QUANTITY]
        print(f"  {item[ITEM_NAME]:<22} ${line_total:>7.2f}")
        print(f"    ({item[ITEM_QUANTITY]} x ${item[ITEM_PRICE]:.2f})")

    print("-" * 45)
    print(f"  {'Subtotal':<30} ${subtotal:>7.2f}")

    if discount > 0:
        print(f"  {'Discount (10% off > $100)':<30} -${discount:>6.2f}")

    print("=" * 45)
    print(f"  {'TOTAL':<30} ${final_total:>7.2f}")
    print("=" * 45)

    if discount > 0:
        print("  🎉 You saved ${:.2f} today!".format(discount))

    print()


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 55)
    print("   SHOPPING CART SYSTEM — Day 8, Task 2")
    print("=" * 55)

    # --- Initialize empty cart ---
    cart = []

    # --- Add items ---
    print("\n[1] Adding items to cart...")
    add_item(cart, "Python Crash Course (Book)",  35.99, 1)
    add_item(cart, "Mechanical Keyboard",          89.99, 1)
    add_item(cart, "USB-C Hub",                    24.99, 2)
    add_item(cart, "Monitor Stand",                45.00, 1)
    add_item(cart, "Sticky Notes Pack",             4.99, 3)
    add_item(cart, "Laptop Sleeve",                19.99, 1)

    display_cart(cart)

    # --- Update quantity ---
    print("[2] Updating quantity...")
    update_quantity(cart, "Sticky Notes Pack", 5)

    # --- Remove an item ---
    print("\n[3] Removing an item...")
    remove_item(cart, "USB-C Hub")

    # --- Add a duplicate (should merge, not duplicate) ---
    print("\n[4] Adding duplicate item (should merge quantity)...")
    add_item(cart, "Laptop Sleeve", 19.99, 2)

    # --- Show recently added (list slicing) ---
    print(f"\n[5] Recently Added Items (last {RECENTLY_ADDED_N} via slicing)")
    print("-" * 40)
    recent = get_recently_added(cart)
    for item in recent:
        print(f"  • {item[ITEM_NAME]:<22} ${item[ITEM_PRICE]:.2f}")

    # --- Show subtotal before receipt ---
    print(f"\n[6] Cart subtotal: ${calculate_subtotal(cart):.2f}")
    subtotal, discount, total = calculate_total(cart)
    if discount > 0:
        print(f"    Discount eligible! (>${DISCOUNT_THRESHOLD:.0f} threshold met)")
    else:
        print(f"    No discount (total under ${DISCOUNT_THRESHOLD:.0f})")

    # --- Final receipt ---
    print("\n[7] Printing Final Receipt...")
    print_receipt(cart)

    # --- Edge case: empty cart ---
    print("[8] Testing empty cart edge case...")
    empty_cart = []
    display_cart(empty_cart)
    print(f"    Subtotal of empty cart: ${calculate_subtotal(empty_cart):.2f}")

    print("=" * 55)
    print("   shopping_cart.py — COMPLETE")
    print("=" * 55)
