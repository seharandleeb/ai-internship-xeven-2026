"""
Script Purpose: Data Types Explorer
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 2 of 30

This script demonstrates all four basic Python data types:
Integer, Float, Boolean, and String.
It also shows how to check types using type() function
and how to convert between different data types.
"""


# ─── INTEGER ───────────────────────────────────────
# Integers are whole numbers, positive or negative

age = 22                  # age of the intern
total_days = 30           # total internship duration
current_day = 2           # today is day 2

print("--- Integer Examples ---")
print(f"Age: {age}")
print(f"Total Days: {total_days}")
print(f"Current Day: {current_day}")
print(f"Type: {type(age)}")


# ─── FLOAT ─────────────────────────────────────────
# Floats are numbers with decimal points

gpa = 3.85                # grade point average
temperature = 36.6        # body temperature in celsius
pi_value = 3.14159        # value of pi

print("\n--- Float Examples ---")
print(f"GPA: {gpa}")
print(f"Temperature: {temperature}")
print(f"Pi Value: {pi_value}")
print(f"Type: {type(gpa)}")


# ─── BOOLEAN ───────────────────────────────────────
# Booleans are either True or False, nothing else

is_intern = True          # currently an intern
is_complete = False       # internship not complete yet
is_python_fun = True      # python is fun

print("\n--- Boolean Examples ---")
print(f"Is Intern: {is_intern}")
print(f"Is Complete: {is_complete}")
print(f"Is Python Fun: {is_python_fun}")
print(f"Type: {type(is_intern)}")


# ─── STRING ────────────────────────────────────────
# Strings are text, always written inside quotes

intern_name = "Sehar Andleeb"     # full name
company = "Xeven Solutions"       # company name
role = "AI Engineer Intern"       # current role

print("\n--- String Examples ---")
print(f"Name: {intern_name}")
print(f"Company: {company}")
print(f"Role: {role}")
print(f"Type: {type(intern_name)}")


# ─── TYPE CONVERSION ───────────────────────────────
# Converting between data types when needed

# Integer to String
day_number = 2
day_as_string = str(day_number)       # int converted to string

# String to Float
score_as_string = "9.5"
score_as_float = float(score_as_string)   # string converted to float

# Float to Integer — decimal part is removed, not rounded
pi = 3.99
pi_as_int = int(pi)                   # float converted to int

print("\n--- Type Conversion ---")
print(f"Integer to String: {day_number} → {day_as_string}")
print(f"Type after conversion: {type(day_as_string)}")

print(f"\nString to Float: {score_as_string} → {score_as_float}")
print(f"Type after conversion: {type(score_as_float)}")

print(f"\nFloat to Integer: {pi} → {pi_as_int}")
print(f"Note: decimal is removed, not rounded")
print(f"Type after conversion: {type(pi_as_int)}")


# ─── SUMMARY ───────────────────────────────────────
print("\n--- All Types Summary ---")
print(f"int    → {age}          → {type(age)}")
print(f"float  → {gpa}         → {type(gpa)}")
print(f"bool   → {is_intern}        → {type(is_intern)}")
print(f"str    → {intern_name} → {type(intern_name)}")