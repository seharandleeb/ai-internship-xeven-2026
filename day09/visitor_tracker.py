"""
Day 9 - Task 2: Unique Visitor Tracker
=======================================
Uses Python sets to track website visitors by IP address.
Demonstrates set operations (union, intersection, difference)
for multi-day visitor analytics.

Author: Sehar Andleeb
Internship: Xeven Solutions - AI Engineering Internship 2026
Mentor: Mubashir Sir (Sr. Machine Learning Engineer)
"""

from __future__ import annotations

import random


# ─── Constants ────────────────────────────────────────────────────────────────
IP_POOL: tuple[str, ...] = tuple(
    f"192.168.{random.randint(0, 5)}.{i}" for i in range(1, 51)
)
DAYS: tuple[str, ...] = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")


# ─── Visitor log generator ────────────────────────────────────────────────────

def generate_daily_visitors(
    ip_pool: tuple[str, ...],
    visit_count: int,
    seed: int | None = None
) -> set[str]:
    """Randomly sample IPs from the pool to simulate a day's visitors.

    Using a set ensures duplicate visits from the same IP are ignored,
    just like a real unique-visitor counter.

    Args:
        ip_pool: All possible IP addresses.
        visit_count: Number of raw visits (may include duplicates).
        seed: Optional random seed for reproducibility.

    Returns:
        Set of unique IP addresses that visited on that day.
    """
    if seed is not None:
        random.seed(seed)

    # sample with replacement to simulate real repeated visits, then deduplicate
    raw_visits = [random.choice(ip_pool) for _ in range(visit_count)]
    return set(raw_visits)


# ─── Analytics functions ──────────────────────────────────────────────────────

def visitors_on_all_days(daily_logs: dict[str, set[str]]) -> set[str]:
    """Return IPs that visited every single tracked day (full intersection).

    Args:
        daily_logs: Mapping of day name → set of visitor IPs.

    Returns:
        Set of IPs present in all days.
    """
    if not daily_logs:
        return set()
    sets = list(daily_logs.values())
    result = sets[0]
    for s in sets[1:]:
        result = result & s          # intersection: visitors seen every day
    return result


def total_unique_visitors(daily_logs: dict[str, set[str]]) -> set[str]:
    """Return the union of all daily visitor sets (ever visited this week).

    Args:
        daily_logs: Mapping of day name → set of visitor IPs.

    Returns:
        Set of all unique IPs across the entire period.
    """
    result: set[str] = set()
    for visitor_set in daily_logs.values():
        result = result | visitor_set   # union: add everyone seen so far
    return result


def exclusive_visitors(
    daily_logs: dict[str, set[str]],
    day: str
) -> set[str]:
    """Return IPs that visited ONLY on the given day and no other day.

    Args:
        daily_logs: Mapping of day name → set of visitor IPs.
        day: The day whose exclusive visitors we want.

    Returns:
        Set of IPs unique to that day.

    Raises:
        KeyError: If the day is not in daily_logs.
    """
    if day not in daily_logs:
        raise KeyError(f"Day '{day}' not found in logs.")

    target = daily_logs[day]
    others: set[str] = set()
    for d, visitors in daily_logs.items():
        if d != day:
            others |= visitors          # collect all IPs from other days

    return target - others              # difference: target minus all others


def calculate_retention_rate(
    previous_day: set[str],
    current_day: set[str]
) -> float:
    """What fraction of yesterday's visitors also came back today?

    Args:
        previous_day: Visitor set for the previous day.
        current_day: Visitor set for the current day.

    Returns:
        Retention rate as a percentage (0–100), rounded to 1 decimal place.
    """
    if not previous_day:
        return 0.0
    returning = previous_day & current_day     # intersection = came back
    return round(len(returning) / len(previous_day) * 100, 1)


def calculate_growth_rate(
    previous_day: set[str],
    current_day: set[str]
) -> float:
    """Percentage change in unique visitor count day-over-day.

    Args:
        previous_day: Visitor set for the previous day.
        current_day: Visitor set for the current day.

    Returns:
        Growth rate as a percentage, rounded to 1 decimal place.
        Positive = growth, negative = decline.
    """
    if not previous_day:
        return 0.0
    delta = len(current_day) - len(previous_day)
    return round(delta / len(previous_day) * 100, 1)


# ─── Display helpers ──────────────────────────────────────────────────────────

def print_section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'─' * 55}")
    print(f"  {title}")
    print(f"{'─' * 55}")


def display_daily_summary(daily_logs: dict[str, set[str]]) -> None:
    """Print per-day visitor counts.

    Args:
        daily_logs: Mapping of day name → set of visitor IPs.
    """
    print_section(" Daily Unique Visitor Counts")
    for day, visitors in daily_logs.items():
        bar = "█" * (len(visitors) // 2)    # simple ASCII bar chart
        print(f"  {day:<12}: {len(visitors):>3} visitors  {bar}")


def display_week_analytics(daily_logs: dict[str, set[str]]) -> None:
    """Display full weekly analytics report.

    Args:
        daily_logs: Mapping of day name → set of visitor IPs.
    """
    days_list = list(daily_logs.keys())

    # ── Growth & Retention ──────────────────────────────────────────────────
    print_section(" Day-over-Day Growth & Retention")
    print(f"  {'Day':<12} {'Visitors':>9} {'Growth':>9} {'Retention':>11}")
    print(f"  {'─'*12} {'─'*9} {'─'*9} {'─'*11}")

    for i, day in enumerate(days_list):
        count = len(daily_logs[day])
        if i == 0:
            growth = retention = "—"
        else:
            prev = daily_logs[days_list[i - 1]]
            curr = daily_logs[day]
            g = calculate_growth_rate(prev, curr)
            r = calculate_retention_rate(prev, curr)
            growth    = f"{g:+.1f}%"
            retention = f"{r:.1f}%"
        print(f"  {day:<12} {count:>9} {growth:>9} {retention:>11}")

    # ── Set Operations Summary ───────────────────────────────────────────────
    print_section(" Set Operation Highlights")
    all_ever  = total_unique_visitors(daily_logs)
    all_every = visitors_on_all_days(daily_logs)

    print(f"  Total unique visitors (union) this week : {len(all_ever)}")
    print(f"  Visitors present on EVERY day (∩ all)  : {len(all_every)}")

    # Pairwise intersections for first vs last day
    first_day = daily_logs[days_list[0]]
    last_day  = daily_logs[days_list[-1]]
    common_fl = first_day & last_day
    print(f"  Common: {days_list[0]} ∩ {days_list[-1]}              : {len(common_fl)}")

    # Symmetric difference between first and last day
    sym_diff = first_day ^ last_day
    print(f"  Sym-diff {days_list[0]} △ {days_list[-1]}           : {len(sym_diff)}")

    # ── Exclusive visitors ───────────────────────────────────────────────────
    print_section(" Visitors Exclusive to Each Day (seen no other day)")
    for day in days_list:
        excl = exclusive_visitors(daily_logs, day)
        print(f"  {day:<12}: {len(excl):>3} exclusive visitors")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    """Entry point: simulate a week of website traffic and analyse it."""

    print("=" * 55)
    print("   Day 9 – Task 2: Unique Visitor Tracker")
    print("=" * 55)

    # Simulate daily visitor logs with fixed seeds for reproducibility
    seeds = [42, 7, 99, 13, 55]
    visit_counts = [40, 35, 45, 38, 50]   # raw hits per day (includes repeats)

    daily_logs: dict[str, set[str]] = {}
    for day, seed, count in zip(DAYS, seeds, visit_counts):
        daily_logs[day] = generate_daily_visitors(IP_POOL, count, seed=seed)

    # Display results
    display_daily_summary(daily_logs)
    display_week_analytics(daily_logs)

    # ── Demonstrate core set operations explicitly ───────────────────────────
    print_section("🔬 Explicit Set Operations Demo (Mon vs Tue)")
    mon = daily_logs["Monday"]
    tue = daily_logs["Tuesday"]

    print(f"  Monday visitors   : {len(mon)}")
    print(f"  Tuesday visitors  : {len(tue)}")
    print(f"  Union     (∪)     : {len(mon.union(tue))}")
    print(f"  Intersection (∩)  : {len(mon.intersection(tue))}")
    print(f"  Mon - Tue (diff)  : {len(mon.difference(tue))}")
    print(f"  Sym-diff  (△)     : {len(mon.symmetric_difference(tue))}")

    print("\n Task 2 complete.\n")


if __name__ == "__main__":
    main()
