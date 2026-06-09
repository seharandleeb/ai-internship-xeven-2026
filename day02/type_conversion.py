# type_conversion.py
# Author: Sehar Andleeb
# Day 2 - AI Engineer Internship at Xeven Solutions
# Purpose: Demonstrate type conversion between data types


# ─── STRING TO INTEGER ─────────────────────────────
# Use int() to convert a string to an integer

age_as_string = "22"
age_as_integer = int(age_as_string)

print("--- String to Integer ---")
print(age_as_string)
print(type(age_as_string))
print(age_as_integer)
print(type(age_as_integer))


# ─── STRING TO FLOAT ───────────────────────────────
# Use float() to convert a string to a float

gpa_as_string = "3.85"
gpa_as_float = float(gpa_as_string)

print("\n--- String to Float ---")
print(gpa_as_string)
print(type(gpa_as_string))
print(gpa_as_float)
print(type(gpa_as_float))


# ─── INTEGER TO FLOAT ──────────────────────────────
# Use float() to convert an integer to a float

whole_number = 30
decimal_number = float(whole_number)

print("\n--- Integer to Float ---")
print(whole_number)
print(type(whole_number))
print(decimal_number)
print(type(decimal_number))


# ─── FLOAT TO INTEGER ──────────────────────────────
# Use int() to convert float to integer
# Note: it removes the decimal part, does not round

pi = 3.99
pi_as_int = int(pi)

print("\n--- Float to Integer ---")
print(pi)
print(pi_as_int)
print("Note: decimal part is removed, not rounded")


# ─── INTEGER TO STRING ─────────────────────────────
# Use str() to convert a number to a string

current_day = 2
day_as_string = str(current_day)

print("\n--- Integer to String ---")
print(current_day)
print(type(current_day))
print(day_as_string)
print(type(day_as_string))


# ─── BOOLEAN CONVERSIONS ───────────────────────────
# True = 1, False = 0 in Python

print("\n--- Boolean Conversions ---")
print(int(True))
print(int(False))
print(float(True))
print(bool(1))
print(bool(0))
print(bool("hello"))
print(bool(""))


# ─── PRACTICAL EXAMPLE ─────────────────────────────
# input() always returns string
# We must convert it to int for calculations

print("\n--- Practical Example ---")
user_input = input("Enter a number: ")
converted = int(user_input)
result = converted * 2
print(f"Your number doubled is: {result}")