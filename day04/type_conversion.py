"""
Day 4 - Script 1: Type Conversion
==================================
Topic   : Implicit and explicit type conversion in Python
Author  : Sehar Andleeb
Internship: Xeven Solutions AI Internship 2026
"""


# -- 1. Implicit Conversion (Python does it automatically) ------------------

integer_num = 10        # int
float_num   = 3.5       # float

result = integer_num + float_num   # Python quietly upgrades int -> float
print("-- Implicit Conversion --")
print(f"  {integer_num} (int) + {float_num} (float) = {result}")
print(f"  Result type : {type(result)}")   # <class 'float'>


# -- 2. Explicit Conversion — int() -----------------------------------------

print("\n-- int() Conversions --")
print(f"  int(3.9)     = {int(3.9)}")       # truncates, does NOT round
print(f"  int('42')    = {int('42')}")       # string digit -> integer
print(f"  int(True)    = {int(True)}")       # True  -> 1
print(f"  int(False)   = {int(False)}")      # False -> 0


# -- 3. Explicit Conversion — float() ---------------------------------------

print("\n-- float() Conversions --")
print(f"  float(7)     = {float(7)}")        # int -> float
print(f"  float('3.14')= {float('3.14')}")   # string -> float
print(f"  float('1e2') = {float('1e2')}")    # scientific notation works too


# -- 4. Explicit Conversion — str() -----------------------------------------

print("\n-- str() Conversions --")
age    = 22
height = 5.6
print(f"  str(22)      = '{str(age)}'")
print(f"  str(5.6)     = '{str(height)}'")
print("  Concatenation: 'Age is ' + str(age) = 'Age is " + str(age) + "'")


# -- 5. Real-World Scenario — user input is always a string -----------------

print("\n-- Real-World: input() always returns str --")
raw = "25"                          # simulate what input() gives you
age_int = int(raw)                  # must convert before doing math
print(f"  Raw input    : '{raw}'  (type: {type(raw).__name__})")
print(f"  After int()  : {age_int}  (type: {type(age_int).__name__})")
print(f"  Age in 5 yrs : {age_int + 5}")


# -- 6. Safe Conversion with try/except -------------------------------------

print("\n-- Safe Conversion (handles bad input) --")

test_values = ["42", "3.14", "hello", ""]

for value in test_values:
    try:
        converted = int(value)
        print(f"  int('{value}') -> {converted}  OK")
    except ValueError:
        print(f"  int('{value}') -> FAILED  Cannot convert '{value}' to int")


print("\nDay 4 | Script 1 complete — Type Conversion")