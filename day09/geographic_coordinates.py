"""
Day 9 - Task 1: Geographic Coordinates System
==============================================
Demonstrates tuple usage for storing geographic data,
distance calculation using the Haversine formula,
and tuple immutability enforcement.

Author: Sehar Andleeb
Internship: Xeven Solutions - AI Engineering Internship 2026
Mentor: Mubashir Sir (Sr. Machine Learning Engineer)
"""

import math
from typing import Optional


# ─── Type alias for clarity ───────────────────────────────────────────────────
Coordinate = tuple[str, float, float]   # (city_name, latitude, longitude)


# ─── Constants ────────────────────────────────────────────────────────────────
EARTH_RADIUS_KM: float = 6371.0

CITIES: tuple[Coordinate, ...] = (
    ("Lahore",       31.5497,  74.3436),
    ("Karachi",      24.8607,  67.0011),
    ("Islamabad",    33.6844,  73.0479),
    ("Peshawar",     34.0151,  71.5249),
    ("Quetta",       30.1798,  66.9750),
    ("Multan",       30.1575,  71.5249),
    ("Faisalabad",   31.4504,  73.1350),
    ("Rawalpindi",   33.5651,  73.0169),
    ("Hyderabad",    25.3960,  68.3578),
    ("Gujranwala",   32.1877,  74.1945),
)


# ─── Helper utilities ─────────────────────────────────────────────────────────

def degrees_to_radians(degrees: float) -> float:
    """Convert decimal degrees to radians.

    Args:
        degrees: Angle in decimal degrees.

    Returns:
        Equivalent angle in radians.
    """
    return degrees * (math.pi / 180)


def calculate_haversine_distance(coord_a: Coordinate, coord_b: Coordinate) -> float:
    """Calculate the great-circle distance between two geographic coordinates.

    Uses the Haversine formula, which accounts for Earth's curvature.

    Args:
        coord_a: First coordinate tuple (city_name, latitude, longitude).
        coord_b: Second coordinate tuple (city_name, latitude, longitude).

    Returns:
        Distance in kilometres (rounded to 2 decimal places).
    """
    # Unpack latitude and longitude from each coordinate tuple
    _, lat1, lon1 = coord_a
    _, lat2, lon2 = coord_b

    # Convert degrees → radians
    lat1_rad = degrees_to_radians(lat1)
    lat2_rad = degrees_to_radians(lat2)
    delta_lat = degrees_to_radians(lat2 - lat1)
    delta_lon = degrees_to_radians(lon2 - lon1)

    # Haversine formula
    a = (math.sin(delta_lat / 2) ** 2
         + math.cos(lat1_rad) * math.cos(lat2_rad)
         * math.sin(delta_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance_km = EARTH_RADIUS_KM * c
    return round(distance_km, 2)


def find_closest_city(
    target: tuple[float, float],
    cities: tuple[Coordinate, ...]
) -> tuple[str, float]:
    """Find the city in the dataset closest to the given coordinate.

    Args:
        target: A (latitude, longitude) tuple for the query location.
        cities: Tuple of city coordinate tuples to search.

    Returns:
        A tuple of (city_name, distance_km) for the nearest city.

    Raises:
        ValueError: If the cities collection is empty.
    """
    if not cities:
        raise ValueError("The cities collection must not be empty.")

    # Build a temporary coordinate tuple so we can reuse calculate_haversine_distance
    query_coord: Coordinate = ("query_point", target[0], target[1])

    closest_city: str = ""
    min_distance: float = float("inf")

    for city_coord in cities:
        dist = calculate_haversine_distance(query_coord, city_coord)
        if dist < min_distance:
            min_distance = dist
            closest_city = city_coord[0]   # city_name is index 0

    return (closest_city, round(min_distance, 2))


def display_all_cities(cities: tuple[Coordinate, ...]) -> None:
    """Pretty-print all cities with their coordinates.

    Args:
        cities: Tuple of city coordinate tuples.
    """
    print("\n City Coordinate Database")
    print("─" * 45)
    print(f"{'City':<15} {'Latitude':>10} {'Longitude':>12}")
    print("─" * 45)
    for city_name, lat, lon in cities:
        print(f"{city_name:<15} {lat:>10.4f}° {lon:>10.4f}°")
    print("─" * 45)
    print(f"  Total cities stored: {len(cities)}\n")


def demonstrate_immutability() -> None:
    """Show that tuple coordinates are immutable by catching the TypeError."""
    print(" Demonstrating Tuple Immutability")
    print("─" * 45)

    sample: Coordinate = ("Lahore", 31.5497, 74.3436)
    print(f"  Original tuple: {sample}")
    print("  Attempting: sample[1] = 99.9999  ...")

    try:
        sample[1] = 99.9999          # type: ignore[index]  # intentional error
    except TypeError as exc:
        print(f"   TypeError caught → {exc}")

    print("  Tuple remains unchanged:", sample, "\n")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    """Entry point: run all geographic coordinate demonstrations."""

    print("=" * 55)
    print("   Day 9 – Task 1: Geographic Coordinates System")
    print("=" * 55)

    # 1. Display the city database
    display_all_cities(CITIES)

    # 2. Calculate distance between two specific cities
    lahore  = CITIES[0]   # ("Lahore",   31.5497, 74.3436)
    karachi = CITIES[1]   # ("Karachi",  24.8607, 67.0011)

    distance = calculate_haversine_distance(lahore, karachi)
    print(f" Distance Calculation")
    print("─" * 45)
    print(f"  {lahore[0]} → {karachi[0]}: {distance} km\n")

    # 3. Multi-city distance matrix (selective)
    print(" Distance Matrix (first 4 cities)")
    print("─" * 55)
    sample_cities = CITIES[:4]
    header = f"{'':12}" + "".join(f"{c[0]:>12}" for c in sample_cities)
    print(header)
    for city_a in sample_cities:
        row = f"{city_a[0]:<12}"
        for city_b in sample_cities:
            if city_a == city_b:
                row += f"{'—':>12}"
            else:
                d = calculate_haversine_distance(city_a, city_b)
                row += f"{d:>12.1f}"
        print(row)
    print()

    # 4. Find closest city to a custom coordinate
    test_points: list[tuple[str, tuple[float, float]]] = [
        ("DHA Lahore (33°N, 74°E)",  (33.0, 74.0)),
        ("Arabian Sea  (22°N, 65°E)", (22.0, 65.0)),
        ("KPK Region   (34°N, 72°E)", (34.0, 72.0)),
    ]

    print(" Closest City Finder")
    print("─" * 55)
    for label, point in test_points:
        closest, dist_km = find_closest_city(point, CITIES)
        print(f"  Query: {label}")
        print(f"    → Closest city: {closest}  ({dist_km} km away)\n")

    # 5. Demonstrate immutability
    demonstrate_immutability()

    print(" Task 1 complete.\n")


if __name__ == "__main__":
    main()
