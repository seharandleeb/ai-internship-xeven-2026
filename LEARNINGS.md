# Day 7 — Week 1 Review and Self Assessment

## What I Learned Today

- Reviewed all concepts from Days 1 to 6 and identified weak areas
- Self-assessment builds metacognition — knowing what you know is as important as knowing it
- Git branching and commit hygiene matter as much as the code itself
- Writing a feedback document forces you to articulate gaps clearly
- Consistent daily commits create a professional portfolio automatically
- The FEEDBACK_WEEK1.md exercise showed me I am stronger in conditionals than in list slicing
- Week 2 action items: practice list comprehensions daily, write more modular functions
- Documentation is a first-class engineering skill, not an afterthought

---

## Research Sources

### Source 1 — ChatGPT
**Topic:** How to write a self-assessment as a developer
**Date:** June 2026
**Key Takeaway:** Effective self-assessment identifies three things — what you can do independently, what you need help with, and what your next goal is

### Source 2 — Claude
**Topic:** Week 1 Python review — gaps and strengths
**Date:** June 2026
**Key Takeaway:** Revisiting earlier code with fresh eyes reveals style issues that were invisible when first written — always review before committing

---

## Personal Insight

Writing FEEDBACK_WEEK1.md was uncomfortable because it forced honesty about my gaps. But that discomfort is exactly why it is valuable. A developer who cannot honestly evaluate their own work cannot improve systematically. Week 2 starts with a clear target, not just momentum.

---

---

# Day 8 — Tuples, Sets and Advanced List Operations

## What I Learned Today

- Tuples are ordered and immutable — use for fixed data like coordinates and DB configs
- Single-element tuple needs a trailing comma: `(42,)` not `(42)`
- Named tuples from `collections` give field names without writing a full class
- `{}` creates an empty dict, NOT an empty set — must use `set()` explicitly
- Sets store only unique elements and membership testing is O(1) vs list O(n)
- Four set operators: `|` union, `&` intersection, `-` difference, `^` symmetric difference
- Frozensets are immutable sets — they can be used as dictionary keys
- List slicing with step: `data[::2]` every 2nd, `data[::-1]` reverses the list
- `enumerate()` replaces `range(len(...))` — always use it when you need index + value
- `zip()` pairs two parallel lists and `dict(zip(keys, values))` builds a dict cleanly
- `sorted()` returns a new list; `sort()` mutates in place — easy to confuse
- This O(1) vs O(n) distinction is why LLM tokenisers handle 50k tokens instantly

---

## Research Sources

### Source 1 — ChatGPT
**Topic:** Tuples vs lists — when to use each
**Date:** June 2026
**Key Takeaway:** Tuples are not just immutable lists — they carry semantic meaning that this data should not change, making code intentions clearer to other developers

### Source 2 — Gemini
**Topic:** Python set operations with real examples
**Date:** June 2026
**Key Takeaway:** Set algebra maps directly to real problems — finding common skills between teams, deduplicating IDs, checking permissions

### Source 3 — Claude
**Topic:** Advanced list operations and comprehensions
**Date:** June 2026
**Key Takeaway:** List comprehensions are not just syntactic sugar — Python internally optimises them to run faster than equivalent for loops with append

### Source 4 — Real Python
**Title:** Python's tuple data type — a deep dive
**URL:** https://realpython.com/python-tuple
**Date:** June 2026
**Key Takeaway:** Tuples are hashable when their contents are hashable, which is why they can serve as dictionary keys — a property lists can never have

---

## Comparison Table

| Concept | ChatGPT | Gemini | Claude | Real Python |
|---|---|---|---|---|
| Tuples vs Lists | Covered | Covered | Covered | Best — deep dive |
| Named Tuples | Mentioned | Covered | Covered | Covered |
| Set Operations | Covered | Best — examples | Covered | Covered |
| List Comprehension | Covered | Covered | Best — code | Covered |
| Performance O(1) vs O(n) | Covered | Mentioned | Covered | Covered |
| Frozensets | Mentioned | Covered | Covered | Covered |

---

## Personal Insight

The biggest insight today was connecting O(1) set lookups to real AI engineering. LLM tokenisers maintain a vocabulary dictionary of 50,000+ tokens and look up each one in constant time. If they used a list instead, every token lookup would scan the entire vocabulary. Understanding why data structures exist at the performance level, not just the syntax level, is what makes the difference between writing code and engineering systems.