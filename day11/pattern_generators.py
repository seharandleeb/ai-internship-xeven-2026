"""
Day 11 - Task 2: Pattern Generators
=====================================
Nested loops for multiplication tables, pyramid patterns, matrix
operations (transpose, row/column sums, diagonal elements), and
an ASCII art generator.

Author: Sehar Andleeb
Date: 2026-06-11
Internship: Xeven Solutions AI Engineering Internship 2026
"""

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
TABLE_SIZE    = 10    # Multiplication table dimension
PYRAMID_ROWS  = 7     # Height of pyramid patterns
MATRIX_ROWS   = 4
MATRIX_COLS   = 4


# ---------------------------------------------------------------------------
# Section 1 – Multiplication Table
# ---------------------------------------------------------------------------

def print_multiplication_table(size: int = TABLE_SIZE) -> None:
    """
    Print a formatted multiplication table using nested for loops.

    Time complexity: O(n²) — each of the n rows iterates n columns.

    Args:
        size: Dimension of the table (size × size).
    """
    print(f"\n{'='*60}")
    print(f"  MULTIPLICATION TABLE ({size}×{size})  —  O(n²) nested loops")
    print(f"{'='*60}")

    # Header row
    header = "     " + "  ".join(f"{c:3}" for c in range(1, size + 1))
    print(header)
    print("  " + "-" * (len(header) - 2))

    # Outer loop: rows
    for row in range(1, size + 1):
        row_values = f"  {row:2} |"
        # Inner loop: columns  ← this is the O(n²) part
        for col in range(1, size + 1):
            row_values += f"  {row * col:3}"
        print(row_values)

    print()


# ---------------------------------------------------------------------------
# Section 2 – Pyramid Patterns
# ---------------------------------------------------------------------------

def print_right_triangle(rows: int = PYRAMID_ROWS) -> None:
    """
    Print a right-aligned triangle of asterisks.

    Args:
        rows: Number of rows in the triangle.
    """
    print("Right Triangle:")
    for row in range(1, rows + 1):                 # outer loop: row count
        print("  " + "*" * row)                    # inner operation: repeat char


def print_pyramid(rows: int = PYRAMID_ROWS) -> None:
    """
    Print a centred pyramid of asterisks.

    Args:
        rows: Number of rows in the pyramid.
    """
    print("\nCentred Pyramid:")
    for row in range(1, rows + 1):
        spaces = " " * (rows - row)                # leading spaces
        stars  = "*" * (2 * row - 1)              # odd count: 1, 3, 5 …
        print(f"  {spaces}{stars}")


def print_number_triangle(rows: int = PYRAMID_ROWS) -> None:
    """
    Print a triangle where each row contains its row-number repeated.

    Args:
        rows: Number of rows.
    """
    print("\nNumber Triangle:")
    for row in range(1, rows + 1):                 # outer: each row
        row_str = ""
        for _ in range(row):                       # inner: repeat digit
            row_str += str(row) + " "
        print(f"  {row_str.strip()}")


def print_hollow_diamond(rows: int = PYRAMID_ROWS) -> None:
    """
    Print a hollow diamond pattern using nested conditionals.

    Args:
        rows: Half-height of the diamond (top half has `rows` rows).
    """
    print("\nHollow Diamond:")
    full_height = 2 * rows - 1
    for i in range(full_height):
        # Map i to distance from centre (0 = top, rows-1 = widest)
        dist = abs(i - (rows - 1))
        spaces = " " * dist
        width  = 2 * (rows - dist) - 1

        if width == 1:
            print(f"  {spaces}*")          # tip of diamond
        else:
            inner = " " * (width - 2)
            print(f"  {spaces}*{inner}*")


def demonstrate_patterns() -> None:
    """Run all pattern generators in sequence."""
    print(f"\n{'='*60}")
    print("  PATTERN GENERATORS  —  Nested Loops Demo")
    print(f"{'='*60}")
    print_right_triangle()
    print_pyramid()
    print_number_triangle()
    print_hollow_diamond()


# ---------------------------------------------------------------------------
# Section 3 – Matrix Operations
# ---------------------------------------------------------------------------

def create_sample_matrix(rows: int = MATRIX_ROWS, cols: int = MATRIX_COLS) -> list[list[int]]:
    """
    Create a deterministic sample matrix filled with sequential integers.

    Args:
        rows: Number of rows.
        cols: Number of columns.

    Returns:
        2-D list (list of lists) filled with integers starting at 1.
    """
    matrix = []
    value  = 1
    for _ in range(rows):               # outer loop: rows
        row = []
        for _ in range(cols):           # inner loop: columns
            row.append(value)
            value += 1
        matrix.append(row)
    return matrix


def print_matrix(matrix: list[list[int]], label: str = "Matrix") -> None:
    """
    Pretty-print a 2-D matrix.

    Args:
        matrix: 2-D list of integers.
        label:  Display label shown above the matrix.
    """
    print(f"\n  {label}:")
    for row in matrix:
        print("    " + "  ".join(f"{v:4}" for v in row))


def transpose_matrix(matrix: list[list[int]]) -> list[list[int]]:
    """
    Transpose a matrix (swap rows and columns) using nested loops.

    Time complexity: O(rows × cols).

    Args:
        matrix: Original 2-D list.

    Returns:
        Transposed 2-D list.
    """
    rows = len(matrix)
    cols = len(matrix[0])
    # Pre-allocate result grid
    transposed = [[0] * rows for _ in range(cols)]

    for r in range(rows):         # iterate original rows
        for c in range(cols):     # iterate original columns
            transposed[c][r] = matrix[r][c]   # flip indices

    return transposed


def sum_rows_and_cols(matrix: list[list[int]]) -> tuple[list[int], list[int]]:
    """
    Compute the sum of each row and each column.

    Args:
        matrix: 2-D list of integers.

    Returns:
        Tuple of (row_sums, col_sums).
    """
    rows = len(matrix)
    cols = len(matrix[0])

    row_sums = []
    for row in matrix:                         # outer: each row
        row_sums.append(sum(row))              # built-in sum over a row

    col_sums = [0] * cols
    for r in range(rows):                      # outer: each row
        for c in range(cols):                  # inner: each column
            col_sums[c] += matrix[r][c]

    return row_sums, col_sums


def get_diagonal_elements(matrix: list[list[int]]) -> tuple[list[int], list[int]]:
    """
    Extract main diagonal and anti-diagonal elements.
    Works on square matrices only.

    Args:
        matrix: Square 2-D list.

    Returns:
        Tuple of (main_diagonal, anti_diagonal).
    """
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("Diagonal extraction requires a square matrix.")

    main_diag  = []
    anti_diag  = []
    for i in range(n):
        main_diag.append(matrix[i][i])           # top-left → bottom-right
        anti_diag.append(matrix[i][n - 1 - i])  # top-right → bottom-left

    return main_diag, anti_diag


def demonstrate_matrix_operations() -> None:
    """Run all matrix operations and display results."""
    print(f"\n{'='*60}")
    print("  MATRIX OPERATIONS  —  Nested Loops  (O(n²))")
    print(f"{'='*60}")

    original = create_sample_matrix()
    print_matrix(original, "Original")

    # Transpose
    transposed = transpose_matrix(original)
    print_matrix(transposed, "Transposed")

    # Row and column sums
    row_sums, col_sums = sum_rows_and_cols(original)
    print(f"\n  Row sums    : {row_sums}")
    print(f"  Column sums : {col_sums}")

    # Diagonal elements (requires square matrix)
    main_d, anti_d = get_diagonal_elements(original)
    print(f"\n  Main diagonal  (↘) : {main_d}")
    print(f"  Anti diagonal  (↙) : {anti_d}")


# ---------------------------------------------------------------------------
# Section 4 – ASCII Art Generator
# ---------------------------------------------------------------------------

def generate_ascii_art(width: int = 30, height: int = 10) -> None:
    """
    Generate a bordered ASCII art canvas with a simple inner pattern.

    The canvas uses nested loops:
    - Outer loop iterates rows.
    - Inner loop iterates columns.
    - Conditionals decide which character to place at each position.

    Args:
        width:  Width of the canvas in characters.
        height: Height of the canvas in rows.
    """
    print(f"\n{'='*60}")
    print("  ASCII ART GENERATOR  —  Nested Loops + Conditionals")
    print(f"{'='*60}")

    for row in range(height):                    # outer loop: rows
        line = ""
        for col in range(width):                 # inner loop: columns

            # Border conditions
            is_top_bottom = (row == 0 or row == height - 1)
            is_left_right = (col == 0 or col == width - 1)

            # Diagonal stripe condition
            is_stripe = ((row + col) % 6 == 0)

            # Decide character
            if is_top_bottom or is_left_right:
                char = "#"    # border
            elif is_stripe:
                char = "/"    # diagonal stripe
            else:
                char = " "    # empty interior

            line += char

        print("  " + line)

    print()

    # ----- Name Banner -----
    print("  Name banner (each letter is a nested-loop sub-grid):")
    _print_banner("SEHAR")


def _print_banner(text: str) -> None:
    """
    Print a simple block-letter banner for the given text.

    Each letter is 5×5 pixels defined as a list of 5 strings.
    Uses nested loops to iterate rows and columns of each letter.

    Args:
        text: Uppercase string to render.
    """
    # Minimal 5-row pixel font (S, E, H, A, R)
    PIXEL_FONT = {
        "S": [" ###", "#   ", " ## ", "   #", "### "],
        "E": ["####", "#   ", "### ", "#   ", "####"],
        "H": ["#  #", "#  #", "####", "#  #", "#  #"],
        "A": [" ## ", "#  #", "####", "#  #", "#  #"],
        "R": ["### ", "#  #", "### ", "# # ", "#  #"],
        " ": ["    ", "    ", "    ", "    ", "    "],
    }

    LETTER_ROWS = 5

    # Build each row across all letters
    for row_idx in range(LETTER_ROWS):              # outer: pixel rows
        line = "  "
        for char in text:                           # inner: each character
            letter_def = PIXEL_FONT.get(char.upper(), PIXEL_FONT[" "])
            line += letter_def[row_idx] + " "
        print(line)
    print()


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print_multiplication_table()
    demonstrate_patterns()
    demonstrate_matrix_operations()
    generate_ascii_art()
