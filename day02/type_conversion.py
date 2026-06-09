"""
Script Purpose: Type Conversion Between Data Types
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 2 of 30

This script demonstrates how to convert between different
data types in Python using int(), float(), str(), and bool().
It also shows practical real world examples of when and why
type conversion is needed.
"""


# ─── STRING TO INTEGER ─────────────────────────────
# Use int() to convert a string to an integer
# Only works if the string contains a whole number

age_as_string = "22"                 # this is text, not a number
age_as_integer = int(age_as_string)  # now it is a real number

print("--- String to Integer ---")
print(f"Before: {age_as_string} | Type: {type(age_as_string)}")
print(f"After : {age_as_integer} | Type: {type(age_as_integer)}")


# ─── STRING TO FLOAT ───────────────────────────────
# Use float() to convert a string to a decimal number

gpa_as_string = "3.85"               # this is text
gpa_as_float = float(gpa_as_string)  # now it is a decimal number

print("\n--- String to Float ---")
print(f"Before: {gpa_as_string} | Type: {type(gpa_as_string)}")
print(f"After : {gpa_as_float} | Type: {type(gpa_as_float)}")


# ─── INTEGER TO FLOAT ──────────────────────────────
# Use float() to add decimal point to a whole number

whole_number = 30                    # integer
decimal_number = float(whole_number) # becomes 30.0

print("\n--- Integer to Float ---")
print(f"Before: {whole_number} | Type: {type(whole_number)}")
print(f"After : {decimal_number} | Type: {type(decimal_number)}")


# ─── FLOAT TO INTEGER ──────────────────────────────
# Use int() to remove decimal part
# Important: it removes, does not round

pi = 3.99
pi_as_int = int(pi)                  # becomes 3, not 4

print("\n--- Float to Integer ---")
print(f"Before: {pi} | Type: {type(pi)}")
print(f"After : {pi_as_int} | Type: {type(pi_as_int)}")
print("Note: 3.99 becomes 3, not 4 — decimal is removed not rounded")


# ─── INTEGER TO STRING ─────────────────────────────
# Use str() to convert a number into text

current_day = 2                      # integer
day_as_string = str(current_day)     # becomes "2"

print("\n--- Integer to String ---")
print(f"Before: {current_day} | Type: {type(current_day)}")
print(f"After : {day_as_string} | Type: {type(day_as_string)}")


# ─── BOOLEAN CONVERSIONS ───────────────────────────
# True equals 1, False equals 0 in Python
# Empty values are False, non-empty are True

print("\n--- Boolean Conversions ---")
print(f"int(True)    = {int(True)}")
print(f"int(False)   = {int(False)}")
print(f"float(True)  = {float(True)}")
print(f"bool(1)      = {bool(1)}")
print(f"bool(0)      = {bool(0)}")
print(f"bool('hello')= {bool('hello')}")  # non-empty string is True
print(f"bool('')     = {bool('')}")       # empty string is False


# ─── PRACTICAL EXAMPLE ─────────────────────────────
# Real world use case — user enters numbers as strings
# We must convert them to do calculations
# We also handle errors in case user enters invalid input

print("\n--- Practical Example ---")

try:
    length = input("Enter length of rectangle: ")
    width = input("Enter width of rectangle: ")

    # Convert string input to float for calculation
    length = float(length)               # convert to float
    width = float(width)                 # convert to float

    area = length * width                # now math works correctly
    perimeter = 2 * (length + width)     # calculate perimeter

    print(f"Length    : {length}")
    print(f"Width     : {width}")
    print(f"Area      : {area}")
    print(f"Perimeter : {perimeter}")

except ValueError:
    # This runs if user enters empty or non-numeric input
    print("Invalid input. Please enter numbers only.")