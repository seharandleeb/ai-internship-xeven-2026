# input_output.py
# Author: Sehar Andleeb
# Day 2 - AI Engineer Internship at Xeven Solutions
# Purpose: Demonstrate input() and print() functions


# ─── BASIC print() ─────────────────────────────────
# print() displays output to the screen

print("--- Basic Print Examples ---")
print("Hello, World!")
print("Welcome to Xeven Solutions")
print(100)
print(3.14)
print(True)


# ─── PRINT WITH SEPARATOR ──────────────────────────
# sep= changes what goes between multiple values

print("\n--- Print with Separator ---")
print("Sehar", "Andleeb", sep="-")
print("Python", "AI", "Internship", sep=" | ")


# ─── PRINT WITH END ────────────────────────────────
# end= changes what goes at the end of the line
# default is a new line

print("\n--- Print with End ---")
print("Hello", end=" ")
print("World")


# ─── F-STRINGS ─────────────────────────────────────
# f-strings let you put variables directly inside text

intern_name = "Sehar Andleeb"
current_day = 2
company = "Xeven Solutions"

print("\n--- F-String Examples ---")
print(f"My name is {intern_name}")
print(f"Today is Day {current_day} of 30")
print(f"I am interning at {company}")


# ─── input() FUNCTION ──────────────────────────────
# input() takes text from the user
# It always returns a string

print("\n--- User Input ---")
user_name = input("Enter your name: ")
print(f"Hello {user_name}, welcome to AI internship!")

user_age = input("Enter your age: ")
print(f"You are {user_age} years old")
print(f"Type of user_age is: {type(user_age)}")