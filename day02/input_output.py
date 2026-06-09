"""
Script Purpose: Input and Output Operations
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 2 of 30

This script demonstrates how to use print() for output
and input() for taking user input. It also covers f-strings,
print formatting, and type conversion of user input.
"""


# ─── BASIC print() ─────────────────────────────────
# print() displays any value to the screen

print("--- Basic Print Examples ---")
print("Hello, World!")
print(100)
print(3.14)
print(True)


# ─── PRINT WITH SEPARATOR ──────────────────────────
# sep= controls what appears between multiple values
# default separator is a single space

print("\n--- Print with Separator ---")
print("Sehar", "Andleeb", sep="-")
print("Python", "AI", "Internship", sep=" | ")
print(1, 2, 3, 4, 5, sep=", ")


# ─── PRINT WITH END ────────────────────────────────
# end= controls what appears at the end of the line
# default is a new line character

print("\n--- Print with End ---")
print("Hello", end=" ")
print("World")
print("Day", end=": ")
print(2)


# ─── F-STRINGS ─────────────────────────────────────
# f-strings are the cleanest way to insert variables
# into text. Just put f before the quote and use {}

intern_name = "Sehar Andleeb"    # intern full name
current_day = 2                  # current day number
company = "Xeven Solutions"      # company name
total_days = 30                  # total days

print("\n--- F-String Examples ---")
print(f"My name is {intern_name}")
print(f"Today is Day {current_day} of {total_days}")
print(f"I am interning at {company}")
print(f"Progress: {current_day}/{total_days} days completed")


# ─── SINGLE LINE COMMENTS ──────────────────────────
# Single line comments start with #
# Use them to explain what a line of code does

age = 22        # age of the intern
gpa = 3.85      # current GPA


# ─── MULTI LINE COMMENTS ───────────────────────────
'''
Multi-line comments use triple quotes.
They are used to explain larger sections of code
or to write detailed notes about complex logic.
This is different from a docstring which describes
a function or class.
'''

print("\n--- Comments Demo ---")
print("Single line comments use #")
print("Multi line comments use triple quotes")


# ─── INPUT FROM USER ───────────────────────────────
# input() always returns a string
# We must convert it if we need a number

print("\n--- User Input ---")
user_name = input("Enter your name: ")
print(f"Hello {user_name}, welcome to AI internship!")

# Converting string input to integer for math
user_age = input("Enter your age: ")
user_age = int(user_age)             # convert string to int
birth_year = 2026 - user_age        # now we can do math

print(f"You are {user_age} years old")
print(f"You were born in approximately {birth_year}")
print(f"Type of user_age after conversion: {type(user_age)}")

# Converting string input to float
user_gpa = input("Enter your GPA: ")
user_gpa = float(user_gpa)          # convert string to float
print(f"Your GPA is {user_gpa}")
print(f"Type of user_gpa: {type(user_gpa)}")