# Day 1 — Learnings and Research Sources

## What I Learned Today

- AI is the ability of a computer to learn and make decisions like a human
- Narrow AI handles one specific task; General AI can do anything a human can
- AI is already being used in healthcare, finance, education, and marketing
- Machine Learning is a branch of AI where systems learn from data
- Deep Learning uses layers of neural networks to solve complex problems
- An AI Engineer builds, trains, deploys, and maintains AI systems
- Training means teaching the model using data; Inference means using
  that model to make predictions on new data
- NLP helps computers understand human language
- Computer Vision helps computers understand images and video
- Speech Recognition converts spoken words into text

---

## Research Sources

### Source 1 — Medium Article[08 june 2026]
**Title:** A Beginner's Guide to Artificial Intelligence  
**Link:** [https://medium.com/towards-data-science ](https://meetcyber.net/beginners-guide-to-artificial-intelligence-54b488002acc) 
**What I learned:** Clear explanation of what AI is and how it differs
from traditional programming

### Source 2 — Dev.to Article[08 june 2026]
**Title:** What is Artificial Intelligence?  
**Link:** [https://dev.to  ](https://dev.to/iamcymentho/what-is-artificial-intelligence-38lc)
**What I learned:** Real world examples of AI in daily life and
different domains

### Source 3 — Google AI Education[08 june 2026]
**Title:** Introduction to Machine Learning  
**Link:** https://developers.google.com/machine-learning/intro-to-ml  
**What I learned:** Difference between training and inference, and how
ML models learn from data

### Source 4 — IBM Think Blog[08 june 2026]
**Title:** What is Artificial Intelligence?  
**Link:** https://www.ibm.com/think/topics/artificial-intelligence  
**What I learned:** Types of AI, domains, and the role of AI engineers
in 2026

---

## Comparison Table — What is AI (Across 4 Sources)

| Aspect | Medium | Dev.to | Google AI | IBM |
|---|---|---|---|---|
| AI Definition | Learning from examples | Simulating human thinking | Finding patterns in data | Machines mimicking human intelligence |
| Narrow vs General AI | Mentioned briefly | Explained with examples | Not covered | Covered in detail |
| Real World Examples | Netflix, spam filter | Maps, face unlock | Image recognition | Healthcare, finance |
| AI Engineer Role | Not covered | Briefly mentioned | Focused on ML engineer | Covered in detail |

---

## My Own Understanding

After reading all four sources, AI to me is simply a computer system
that learns from experience instead of following fixed rules. The most
interesting thing I learned is the difference between training and
inference — training is like studying for an exam and inference is
like actually sitting the exam and answering questions.

---

# Day 2 — Python Basics: Variables and Data Types

## What I Learned Today

- Python has 4 basic data types: Integer, Float, Boolean, String
- Variables are dynamically typed and can change type anytime
- input() always returns a string regardless of what user types
- PEP 8 requires snake_case for variables, UPPERCASE for constants
- int() on a float removes the decimal part, it does not round
- True equals 1 and False equals 0 in Python
- type() checks the data type of any variable at runtime
- f-strings are the cleanest way to insert variables into text
- try-except handles errors without crashing the program

---

## Research Sources

### Source 1 — ChatGPT[09 june 2026]
**Topic:** Python data types explanation
**Key Takeaway:** Every value in Python has a type and type()
confirms it at runtime

### Source 2 — Gemini[09 june 2026]
**Topic:** PEP 8 variable naming conventions
**Key Takeaway:** snake_case for variables, UPPERCASE for constants,
descriptive names make code readable without extra comments

### Source 3 — Claude[09 june 2026]
**Topic:** Dynamic typing and type conversion
**Key Takeaway:** Python decides type automatically based on value
assigned; int(), float(), str() allow switching between types

### Source 4 — W3Schools[09 june 2026]
**Title:** Python Data Types
**Link:** https://www.w3schools.com/python/python_datatypes.asp
**Key Takeaway:** Practical examples of all data types and type
conversion with clear output demonstrations

---

## Comparison Table

| Concept | ChatGPT | Gemini | Claude | W3Schools |
|---|---|---|---|---|
| Data Types | Covered with examples | Covered | Covered in depth | Covered |
| Dynamic Typing | Explained | Briefly mentioned | Explained in depth | Not covered |
| Type Conversion | Covered | Covered | Covered in depth | Covered |
| PEP 8 Naming | Mentioned | Covered in detail | Mentioned | Not covered |
| Error Handling | Covered | Not covered | Covered | Not covered |

---

## Professional Coding Standard Learned

Self-documenting code means writing code that explains itself
through descriptive variable names, without needing extra comments.

Bad example:
x = 22
y = 30
z = x / y

Good example:
intern_age = 22
total_days = 30
daily_progress = intern_age / total_days

The second version needs no comment because the variable names
already explain what the code is doing.

---

# Day 3 — Conditional Statements and Logic

## What I Learned Today

- if-elif-else allows programs to make decisions based on conditions
- Only ONE block in an if-elif-else chain ever runs
- Always check the highest boundary first in elif chains
- Use == for comparison, never = inside an if statement
- Nested conditionals should not go deeper than 2 levels
- Every value in Python is either Truthy or Falsy
- try-except handles invalid inputs without crashing the program
- Flat elif chains are more readable than deeply nested if statements

---

## Research Sources

### Source 1 — ChatGPT[09 june 2026]
**Topic:** Boolean logic in programming
**Key Takeaway:** Every condition in Python evaluates to True or
False and truthy/falsy values allow non-boolean types to be used
in conditions naturally

### Source 2 — Gemini[09 june 2026]
**Topic:** Best practices for if-elif-else statements
**Key Takeaway:** Keep conditions flat, check most specific cases
first, and avoid deeply nested conditionals for readability

### Source 3 — Claude[09 june 2026]
**Topic:** Writing clean conditional statements in Python
**Key Takeaway:** Flat elif chains are always preferred over nested
ifs because they are easier to read, debug, and maintain

### Source 4 — Real Python Article[09 june 2026]
**Title:** Python Conditional Statements
**Link:** https://realpython.com/python-conditional-statements
**Key Takeaway:** Proper use of comparison operators and avoiding
the common mistake of using = instead of == in conditions

---

## Comparison Table — Conditional Statements (Across 4 Sources)

| Concept | ChatGPT | Gemini | Claude | Real Python |
|---|---|---|---|---|
| if-elif-else syntax | Covered | Covered | Covered | Covered in depth |
| Truthy/Falsy values | Covered in depth | Briefly mentioned | Covered | Covered |
| Nested conditionals | Covered | Covered | Covered in depth | Covered |
| Common pitfalls | Mentioned | Covered | Covered in depth | Covered in depth |
| Best practices | Covered | Covered in depth | Covered in depth | Covered |

---

## Personal Insight

The most valuable thing I learned today is the difference between
flat elif chains and nested if statements. Both can solve the same
problem but flat elif is always more readable. A good rule I will
follow: if I am nesting more than 2 levels deep, I need to rethink
my approach and restructure the logic.