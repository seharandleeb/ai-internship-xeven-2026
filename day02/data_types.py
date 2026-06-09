# data_types.py
# Author: Sehar Andleeb
# Day 2 - AI Engineer Internship at Xeven Solutions
# Purpose: Demonstrate Python data types with examples


# ─── INTEGER ───────────────────────────────────────
# Integers are whole numbers, positive or negative

age = 22
total_days = 30
current_day = 2

print("--- Integer Examples ---")
print(age)
print(total_days)
print(current_day)
print(type(age))


# ─── FLOAT ─────────────────────────────────────────
# Floats are numbers with decimal points

gpa = 3.85
temperature = 36.6
pi_value = 3.14159

print("\n--- Float Examples ---")
print(gpa)
print(temperature)
print(pi_value)
print(type(gpa))


# ─── BOOLEAN ───────────────────────────────────────
# Booleans are either True or False, nothing else

is_intern = True
is_course_complete = False
is_python_fun = True

print("\n--- Boolean Examples ---")
print(is_intern)
print(is_course_complete)
print(is_python_fun)
print(type(is_intern))


# ─── STRING ────────────────────────────────────────
# Strings are text, always written inside quotes

intern_name = "Sehar Andleeb"
company = "Xeven Solutions"
role = "AI Engineer Intern"

print("\n--- String Examples ---")
print(intern_name)
print(company)
print(role)
print(type(intern_name))


# ─── type() FUNCTION ───────────────────────────────
# type() checks what data type a variable is

print("\n--- Checking All Types ---")
print(type(age))
print(type(gpa))
print(type(is_intern))
print(type(intern_name))