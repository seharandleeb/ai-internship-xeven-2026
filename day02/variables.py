# variables.py
# Author: Sehar Andleeb
# Day 2 - AI Engineer Internship at Xeven Solutions
# Purpose: Demonstrate variable naming conventions and dynamic typing


# ─── PEP 8 VARIABLE NAMING ─────────────────────────
# Always use snake_case: lowercase with underscores
# Names should be descriptive and meaningful

intern_name = "Sehar Andleeb"
company_name = "Xeven Solutions"
internship_duration = 30
current_day = 2

print("--- PEP 8 Variable Naming ---")
print(intern_name)
print(company_name)
print(internship_duration)
print(current_day)


# ─── CONSTANTS ─────────────────────────────────────
# Constants are written in UPPERCASE_WITH_UNDERSCORES
# Their value should never change during the program

MAX_DAYS = 30
COMPANY_NAME = "Xeven Solutions"

print("\n--- Constants ---")
print(MAX_DAYS)
print(COMPANY_NAME)


# ─── DYNAMIC TYPING ────────────────────────────────
# In Python, a variable can change its type anytime
# This is called dynamic typing

my_variable = 10
print("\n--- Dynamic Typing ---")
print(my_variable)
print(type(my_variable))

my_variable = 3.14
print(my_variable)
print(type(my_variable))

my_variable = "Now I am a string"
print(my_variable)
print(type(my_variable))

my_variable = True
print(my_variable)
print(type(my_variable))


# ─── MULTIPLE ASSIGNMENT ───────────────────────────
# You can assign values to multiple variables in one line

x, y, z = 10, 20, 30
print("\n--- Multiple Assignment ---")
print(x)
print(y)
print(z)


# ─── SAME VALUE TO MULTIPLE VARIABLES ──────────────
a = b = c = 100
print("\n--- Same Value to Multiple Variables ---")
print(a)
print(b)
print(c)