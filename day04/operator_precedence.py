"""
Day 4 - Script 2: Operator Precedence
=======================================
Topic   : How Python evaluates expressions with multiple operators
Author  : Sehar Andleeb
Internship: Xeven Solutions AI Internship 2026

Precedence order (high to low):
    ()   -> Parentheses
    **   -> Exponentiation
    *, / , //, % -> Multiplication, Division, Floor Division, Modulo
    +, - -> Addition, Subtraction
"""


# -- 1. Basic Precedence Examples -------------------------------------------

print("-- Basic Precedence --")

expr1 = 2 + 3 * 4          # * runs before +
expr2 = (2 + 3) * 4        # parentheses force + first
expr3 = 2 ** 3 + 1         # ** runs before +
expr4 = 10 - 4 / 2         # / runs before -

print(f"  2 + 3 * 4      = {expr1}   (multiplication first)")
print(f"  (2 + 3) * 4   = {expr2}   (parentheses override)")
print(f"  2 ** 3 + 1     = {expr3}   (exponent first)")
print(f"  10 - 4 / 2     = {expr4}   (division first)")


# -- 2. Division Types ------------------------------------------------------

print("\n-- Division Types --")

a = 17
b = 5

true_div  = a / b       # always returns float
floor_div = a // b      # rounds down to nearest integer
modulo    = a % b       # remainder after floor division

print(f"  {a} / {b}   = {true_div}    (true division  -> float)")
print(f"  {a} // {b}  = {floor_div}     (floor division -> int)")
print(f"  {a} % {b}   = {modulo}      (modulo         -> remainder)")


# -- 3. Modulo Real-World Uses ----------------------------------------------

print("\n-- Modulo Use Cases --")

number = 47

# Check even or odd
if number % 2 == 0:
    print(f"  {number} is even")
else:
    print(f"  {number} is odd")

# Check divisibility
print(f"  {number} divisible by 3? {number % 3 == 0}")
print(f"  {number} divisible by 5? {number % 5 == 0}")

# Extract last digit
print(f"  Last digit of {number}: {number % 10}")


# -- 4. Exponentiation ------------------------------------------------------

print("\n-- Exponentiation --")

print(f"  2 ** 10  = {2 ** 10}       (2 to the power 10)")
print(f"  9 ** 0.5 = {9 ** 0.5}       (square root of 9)")
print(f"  27 ** (1/3) = {27 ** (1/3):.4f}  (cube root of 27)")


# -- 5. Complex Expression — Step by Step -----------------------------------

print("\n-- Complex Expression Breakdown --")

# Expression: 100 - 2 ** 3 * 4 + 10 / 2
# Step 1: 2 ** 3       = 8
# Step 2: 8 * 4        = 32
# Step 3: 10 / 2       = 5.0
# Step 4: 100 - 32     = 68
# Step 5: 68 + 5.0     = 73.0

expression = 100 - 2 ** 3 * 4 + 10 / 2

print(f"  100 - 2 ** 3 * 4 + 10 / 2")
print(f"  Step 1: 2 ** 3       = 8")
print(f"  Step 2: 8 * 4        = 32")
print(f"  Step 3: 10 / 2       = 5.0")
print(f"  Step 4: 100 - 32     = 68")
print(f"  Step 5: 68 + 5.0     = {expression}")


# -- 6. Common Mistake — Associativity of ** --------------------------------

print("\n-- Exponent Associativity (right to left) --")

# 2 ** 3 ** 2  is evaluated as  2 ** (3 ** 2)  =  2 ** 9  =  512
# NOT as  (2 ** 3) ** 2  =  8 ** 2  =  64

right_assoc = 2 ** 3 ** 2
left_forced = (2 ** 3) ** 2

print(f"  2 ** 3 ** 2    = {right_assoc}   (right to left: 2 ** 9)")
print(f"  (2 ** 3) ** 2  = {left_forced}    (forced left:   8 ** 2)")


print("\nDay 4 | Script 2 complete — Operator Precedence")