"""
Script Purpose: Variables and PEP 8 Naming Conventions
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 2 of 30

This script demonstrates proper variable naming following
PEP 8 standards, dynamic typing, and multiple assignment.
It also shows how variables can change type in Python.
"""


# ─── PEP 8 NAMING CONVENTIONS ──────────────────────
# snake_case for variables and functions
# UPPERCASE for constants
# Descriptive names that explain the purpose

intern_name = "Sehar Andleeb"        # full name of intern
company_name = "Xeven Solutions"     # company name
current_day = 2                      # current day of internship
total_days = 30                      # total internship days
daily_hours = 8.5                    # working hours per day
is_active = True                     # internship is active

print("--- PEP 8 Variable Naming ---")
print(f"Intern   : {intern_name}")
print(f"Company  : {company_name}")
print(f"Day      : {current_day} of {total_days}")
print(f"Hours    : {daily_hours} per day")
print(f"Active   : {is_active}")


# ─── CONSTANTS ─────────────────────────────────────
# Constants never change during the program
# Always written in UPPERCASE_WITH_UNDERSCORES

MAX_DAYS = 30                        # maximum internship days
MIN_HOURS = 8                        # minimum daily hours
COMPANY_NAME = "Xeven Solutions"     # company never changes

print("\n--- Constants ---")
print(f"Max Days    : {MAX_DAYS}")
print(f"Min Hours   : {MIN_HOURS}")
print(f"Company     : {COMPANY_NAME}")


# ─── DYNAMIC TYPING ────────────────────────────────
# Python automatically decides the type based on value
# Same variable can hold different types at different times

my_variable = 100                    # starts as integer
print("\n--- Dynamic Typing ---")
print(f"Value: {my_variable} | Type: {type(my_variable)}")

my_variable = 3.14                   # now becomes float
print(f"Value: {my_variable} | Type: {type(my_variable)}")

my_variable = "Now I am a string"    # now becomes string
print(f"Value: {my_variable} | Type: {type(my_variable)}")

my_variable = True                   # now becomes boolean
print(f"Value: {my_variable} | Type: {type(my_variable)}")


# ─── MULTIPLE ASSIGNMENT ───────────────────────────
# Assign values to multiple variables in one line

x, y, z = 10, 20, 30
print("\n--- Multiple Assignment ---")
print(f"x = {x}, y = {y}, z = {z}")


# ─── SAME VALUE TO MULTIPLE VARIABLES ──────────────
# All three variables get the same value

a = b = c = 100
print("\n--- Same Value Assignment ---")
print(f"a = {a}, b = {b}, c = {c}")


# ─── SWAPPING VARIABLES ────────────────────────────
# Python allows swapping without a temporary variable

first = "Hello"
second = "World"

print("\n--- Swapping Variables ---")
print(f"Before swap: first = {first}, second = {second}")

first, second = second, first        # swap in one line

print(f"After swap : first = {first}, second = {second}")