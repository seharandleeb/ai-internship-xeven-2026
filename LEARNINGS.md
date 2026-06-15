# Internship LEARNINGS — Daily Log

---

# Day 1 — Introduction to AI

## What I Learned Today
AI is a computer's ability to learn and make decisions like a human. Narrow AI handles one specific task, while General AI could do anything a human can. AI already powers healthcare, finance, education, and marketing. Machine Learning is the branch of AI where systems learn from data instead of fixed rules, and Deep Learning uses layered neural networks for complex problems. An AI Engineer builds, trains, deploys, and maintains these systems. The core distinction I grasped was training (teaching a model on data) versus inference (using the trained model to predict on new data). I also learned the three big application domains: NLP for understanding language, Computer Vision for images and video, and Speech Recognition for converting speech to text.

## Research Sources
Medium (Beginner's Guide to AI), Dev.to (What is AI), Google AI (Intro to ML), IBM Think Blog (What is AI) (consulted June 9, 2026).


**Clearest Explanation:** IBM Think Blog — it covered AI types, application domains, and the AI Engineer role in the most depth.

## Personal Insight
AI is simply a system that learns from experience rather than following fixed rules. The clearest analogy I found: training is like studying for an exam, and inference is like sitting the exam and answering questions.

---

# Day 2 — Python Basics: Variables and Data Types

## What I Learned Today
Python has four basic data types: integer, float, boolean, and string. Variables are dynamically typed and can change type at any time. `input()` always returns a string regardless of what the user types, so values must be converted with `int()` or `float()` before math. PEP 8 requires snake_case for variables and UPPERCASE for constants. `int()` on a float truncates rather than rounds, so `int(3.9)` gives 3. `True` equals 1 and `False` equals 0. `type()` checks any variable's type at runtime, and f-strings are the cleanest way to insert variables into text. `try-except` handles errors without crashing the program.

## Research Sources
ChatGPT (data types), Gemini (PEP 8 naming), Claude (dynamic typing & conversion), W3Schools (Python Data Types) (consulted June 9, 2026).


**Clearest Explanation:** Claude — explained dynamic typing and type conversion most concretely with runnable examples.

## Personal Insight
Self-documenting code explains itself through descriptive names without extra comments. Writing `intern_age = 22` and `total_days = 30` makes the logic obvious, whereas `x` and `y` force the reader to guess. Good variable names are the cheapest documentation a developer can write, and they pay off every time the code is reread.

---

# Day 3 — Conditional Statements and Logic

## What I Learned Today
The `if-elif-else` structure lets programs make decisions, and only one block in the chain ever runs. The highest boundary should be checked first in elif chains to avoid logic errors. I learned to always use `==` for comparison and never `=` inside a condition, a classic beginner mistake. Nested conditionals should not exceed two levels deep, because flat elif chains are far more readable than deeply nested ifs. Every value in Python is either truthy or falsy, which lets non-boolean types be used directly in conditions. Wrapping input handling in `try-except` keeps the program alive when users enter invalid data.

## Research Sources
ChatGPT (boolean logic), Gemini (if-elif best practices), Claude (clean conditionals), Real Python (Conditional Statements) (consulted June 9, 2026).


**Clearest Explanation:** Real Python — gave the most thorough treatment of common pitfalls (= vs ==) and best practices.

## Personal Insight
The most valuable lesson was the difference between flat elif chains and nested ifs. Both solve the same problem, but flat elif is always more readable, debuggable, and maintainable. My rule going forward: if I am nesting more than two levels deep, I need to stop and restructure the logic rather than push through with another indentation level.

---

# Day 4 — Operators and Type Conversion

## What I Learned Today
Python has seven operator types: arithmetic, comparison, logical, assignment, bitwise, identity, and membership. Precedence follows PEMDAS — parentheses, exponents, multiply/divide, add/subtract. Floor division `//` always rounds down and `%` gives the remainder. Exponentiation is right-associative, so `2 ** 3 ** 2` equals `2 ** 9`, which is 512, not 64. The logical operators `and`, `or`, `not` drive multi-condition checks. Because `input()` returns a string, values must be converted before math, and `int()` truncates rather than rounds. Wrapping conversions in `try/except` handles invalid input gracefully. I also practiced a systematic debugging approach: read the error, print the variable and its type, trace its origin, then apply the right conversion.

## Research Sources
ChatGPT, Gemini, Claude, plus practical operator-precedence references (consulted June 9, 2026).


**Clearest Explanation:** Claude — the step-by-step debugging workflow and safe-conversion tips were the most actionable.

## Personal Insight
Type errors are the most common beginner mistake, and the fix is rarely complex once you can see the variable's actual type. Printing `print(x, type(x))` turned debugging from guesswork into a repeatable process. A small Git lesson stuck too: never join two commands without a separator — run `git add .` and `git commit` separately.

---

# Day 5 — Machine Learning Concepts

## What I Learned Today
Machine Learning is the branch of AI where computers learn from data without being explicitly programmed. Supervised learning uses labeled data to predict, unsupervised learning finds hidden patterns without labels, and reinforcement learning learns through rewards and penalties. Regression predicts continuous values like price or temperature, while classification predicts discrete categories like spam or not spam. Decision trees decide by asking a series of questions, with the root node as the first question and leaf nodes as final answers. Feature engineering directly shapes model quality, and overfitting occurs when a model learns its training data too well and fails to generalize.

## Research Sources
ChatGPT (ML types), Gemini (decision trees), Claude (three ML types with code), Medium (Jagriti Bansal), Dev.to (Marcelo Gobea) (consulted June 10, 2026).


**Clearest Explanation:** Claude — provided runnable code for all three ML types, making the concepts most concrete.

## Personal Insight
The most valuable distinction was regression versus classification. I used to think they were the same, but now I see clearly that regression predicts a number and classification predicts a category. That single difference changes how you frame every ML problem — it determines your model choice, your loss function, and how you measure success.

---

# Day 6 — Python Data Structures: Lists

## What I Learned Today
Lists are ordered, mutable collections that can hold mixed data types. Indexing starts at 0 and negative indexing starts at -1 from the end. Slicing uses `start:end:step`, and the end index is never included. `append()` adds one item, `extend()` adds many, and `insert()` places at a position. `remove()` deletes by value, `pop()` by index, and `clear()` empties the list. `sort()` mutates the original while `sorted()` returns a new list. List comprehension builds lists in one clean, readable line. `IndexError` and `ValueError` are handled with `try-except`, and parallel lists use the same index to represent related data.

## Research Sources
ChatGPT (list operations), Gemini (slicing visuals), Claude (comprehension & errors), Medium (Anastasiia Sydorenko) (consulted June 10, 2026).


**Clearest Explanation:** ChatGPT — the append O(1) vs insert O(n) explanation was the clearest and most impactful.

## Personal Insight
`append()` is always faster than `insert()` because `insert()` shifts every element after the insertion point. When building a list of a million items, appending is dramatically faster than inserting at position 0 each time. Understanding the performance of basic operations — not just their syntax — is what separates a good programmer from an average one.

---

# Day 7 — Week 1 Review and Self-Assessment

## What I Learned Today
I reviewed every concept from Days 1 to 6 and identified my weak areas. Self-assessment builds metacognition: knowing what you know is as important as knowing it. Git branching and commit hygiene matter as much as the code itself, and consistent daily commits build a professional portfolio automatically. Writing the FEEDBACK_WEEK1.md document forced me to articulate my gaps clearly — it revealed I am stronger in conditionals than in list slicing. My Week 2 action items are to practice list comprehensions daily and write more modular functions. Documentation, I now see, is a first-class engineering skill rather than an afterthought.

## Research Sources
ChatGPT (developer self-assessment), Claude (Week 1 review — gaps and strengths) (consulted June 10, 2026).


**Clearest Explanation:** Claude — the 'review with fresh eyes' framing made the value of self-assessment clearest.

## Personal Insight
Writing FEEDBACK_WEEK1.md was uncomfortable because it forced honesty about my gaps, but that discomfort is exactly why it was valuable. A developer who cannot honestly evaluate their own work cannot improve systematically. Revisiting earlier code with fresh eyes also exposed style issues that were invisible when I first wrote them. Week 2 now starts with a clear target, not just momentum.

---

# Day 8 — Tuples, Sets, and Advanced List Operations

## What I Learned Today
Tuples are ordered and immutable, ideal for fixed data like coordinates and configs, and a single-element tuple needs a trailing comma: `(42,)`. Named tuples give field names without writing a full class. `{}` creates an empty dict, not a set — you must use `set()`. Sets store only unique elements and offer O(1) membership testing versus O(n) for lists. The four set operators are union `|`, intersection `&`, difference `-`, and symmetric difference `^`. Frozensets are immutable and can serve as dict keys. `enumerate()` replaces `range(len(...))`, and `zip()` pairs parallel lists cleanly.

## Research Sources
ChatGPT (tuples vs lists), Gemini (set operations), Claude (advanced lists), Real Python (tuple deep dive) (consulted June 10, 2026).


**Clearest Explanation:** Real Python — the tuple deep dive (hashability enabling dict keys) was the clearest explanation.

## Personal Insight
The biggest insight was connecting O(1) set lookups to real AI engineering. LLM tokenizers maintain a vocabulary of 50,000+ tokens and look up each in constant time; a list would force a full scan on every lookup. Understanding why data structures exist at the performance level, not just the syntax level, is what turns writing code into engineering systems.

---

# Day 9 — Tuples and Sets (Applied Projects)

## What I Learned Today
Tuple packing and unpacking makes geographic data elegant — `city, lat, lon = coord` reads like plain English and eliminates index errors. The Haversine formula works on radians, so degrees must be converted first — a reminder that domain knowledge matters alongside syntax. Named tuples give attribute access without class overhead, perfect for read-only records. A `frozenset` is the right type for a domain allowlist: immutable, hashable, and O(1). Pre-compiling regex at module level is a real performance win. Set intersection computes retention, while symmetric difference surfaces users who appeared on exactly one of two days.

## Research Sources
ChatGPT (Haversine), Gemini (frozenset use cases), Claude (set analytics), Real Python (Sets guide) (consulted June 10, 2026).


**Clearest Explanation:** Claude — framing set algebra as analytics (retention, churn, growth) was the clearest.

## Personal Insight
Day 9 shifted my thinking from "what syntax do I use" to "what contract am I expressing." Choosing a tuple for coordinates states these values are facts that should not change. Choosing a frozenset for valid domains communicates that this list is a policy, not a variable. This is what self-documenting code really means — the type itself carries intent, before a single comment is written.

---

# Day 10 — Dictionaries & JSON (Applied Projects)

## What I Learned Today
Dictionaries are hash tables, so lookup, insertion, and deletion are O(1) on average. `.get(key, default)` is the most important habit for crash-proof code — it returns a fallback instead of raising `KeyError`. Nested dictionaries model structured records far more naturally than parallel lists, and `.items()` is the idiomatic way to iterate keys and values together. Dictionary comprehensions express transform-and-filter in one line. Python dicts map one-to-one onto JSON, which is why `json.dump`/`load` feel seamless; the trailing `s` in `dumps`/`loads` means "string." Passing `indent=2` produces human-readable output for hand-edited config files.

## Research Sources
ChatGPT (dict memory/hashing), Gemini (nested vs parallel), Claude (.get patterns), Real Python (Working With JSON) (consulted June 11, 2026).


**Clearest Explanation:** Claude — the .get() vs d[key] 'required vs optional intent' framing was the clearest lesson.

## Personal Insight
A dictionary is really a contract about access patterns — reaching for one says "I will look things up by name, instantly." The `.get()` versus `d[key]` choice was the deepest lesson: it encodes intent. `config.get("timeout", 30)` says a setting is optional, while `config["api_key"]` says the program should stop if it is missing. Because a dict and a JSON object share the same shape, persistence became a natural extension of choosing the right structure.

---

# Day 11 — Loops & Iteration

> Draft — verify against your actual Day 11 scripts (Data Pipeline, Pattern Generators, Number Analysis) and adjust specifics.

## What I Learned Today
`for` loops iterate over sequences while `while` loops run until a condition turns false. `range(start, stop, step)` generates number sequences without building a list in memory. `enumerate()` gives index and value together, replacing the clumsy `range(len(...))` pattern, and `zip()` walks multiple sequences in parallel. `break` exits a loop early, `continue` skips to the next iteration, and an `else` clause on a loop runs only if no `break` fired. Nested loops handle grids and pattern generation, but each added level multiplies the work, so deep nesting signals a need to rethink the approach. Building a data pipeline showed how iteration chains cleaning, transforming, and aggregating steps over a dataset.

## Research Sources
ChatGPT (for vs while), Gemini (enumerate & zip), Claude (break/continue/else), Real Python (Python for Loops) (consulted June 11, 2026).


**Clearest Explanation:** Claude — break/continue/else behaviour and the cost-of-nesting framing were clearest.

## Personal Insight
Loops taught me to think about cost, not just correctness. A nested loop over two large lists is O(n²), and recognizing that early is the difference between a pipeline that scales and one that stalls. Choosing `enumerate()` and `zip()` over manual indexing also made the code read like a description of intent rather than a mechanical counter.

---

# Day 12 — Functions Fundamentals (Applied Projects)

## What I Learned Today
A parameter is the placeholder in the `def` line; an argument is the value passed at call time. `print()` only displays a value while `return` hands it back — a function with no `return` silently returns `None`. Default parameters make arguments optional, but a mutable default like `items=[]` is shared across calls, so the safe pattern is `items=None`. `*args` collects extra positional arguments into a tuple and `**kwargs` collects keyword arguments into a dict. Python resolves names by the LEGB rule, and reassigning a global needs the `global` keyword. Returning a tuple hands back multiple values cleanly.

## Research Sources
ChatGPT (definition & returns), Gemini (argument types), Claude (scope & LEGB), Dev.to — Cynthia Peters (Python functions) (consulted June 12, 2026).


**Clearest Explanation:** Claude — the LEGB rule plus the global-keyword explanation and practical tips were most concrete.

## Personal Insight
Today crystallized why "one function, one job" matters. Building `process_text()` by chaining small helpers like `remove_punctuation()` and `title_case()` made each piece independently testable and kept the logic readable. The validation suite drove home a second lesson: returning a `(is_valid, error_message)` tuple is cleaner than raising exceptions for ordinary invalid input. Splitting the work across three scripts and using the notebook as documentation made the day feel like real engineering.

---

# Day 13 — Advanced Functions

## What I Learned Today
Today I moved from defining functions to using them flexibly. I learned
how `*args` collects extra positional arguments into a tuple and `**kwargs`
collects keyword arguments into a dict, and that the same `*`/`**` syntax
also unpacks a list or dict back into a call. I practiced lambda functions
as short, anonymous callbacks inside `map()`, `filter()`, and `sorted()`,
and learned to reach for a named `def` whenever the logic grows. I also
learned list and dictionary comprehensions as concise, faster replacements
for the build-a-list-in-a-loop pattern, using them to flatten nested lists,
transpose a matrix, invert a dict, and count word frequency. Benchmarking
showed the list comprehension running about twice as fast as lambda+map,
because its loop runs in optimized C with no per-item call overhead.

## Research Sources
Consulted ChatGPT, Gemini, Claude, and a Real Python article on advanced
functions (consulted June 13, 2026).

**Clearest Explanation:** Claude — it tied each construct to a concrete
when-to-use-it rule and explained *why* comprehensions are faster.

## Personal Insight
The biggest shift was realising these features are about expressing intent
clearly, not just writing less code. Choosing a comprehension over a loop,
or a lambda over a full function, is a readability decision as much as a
performance one — and knowing when *not* to use them is the real skill.

---

# Day 14 — Week 2 Review & Mini-Project

## What I Learned Today
Today I consolidated Week 2 by building a complete Contact Management
System that combines every data structure I have learned. I created a
cheat sheet comparing list, tuple, set, and dict across mutability,
ordering, and time complexity, which clarified why fast membership
checks belong to sets and dicts (O(1)) rather than lists (O(n)). I then
applied that directly: the contact manager uses a dict keyed by id, a
set for each contact's tags, and a list for notes — each structure
chosen for its strengths. I implemented CRUD functions, partial-match
search with a dict comprehension, tag handling with set operations, and
JSON save/load. The biggest lesson came from persistence: Python sets
are not JSON-serializable, so I convert each tag set to a sorted list on
save and back to a set on load, wrapped in try/except.

## Research Sources
Consulted ChatGPT, Gemini, Claude, and a Real Python Big-O article
(consulted June 14, 2026).

**Clearest Explanation:** Claude — it connected data-model choices to
Big-O behaviour and flagged the JSON set issue before I hit it.

## Personal Insight
Building one system from many small pieces taught me that choosing the
right data structure upfront is a design decision that shapes how clean
every later function turns out.

---

# Day 15 — Introduction to Large Language Models

## What I Learned Today

Today began Week 3 (AI & LangChain) with a full deep-dive into Large
Language Models. I learned how the Transformer architecture processes
entire sequences in parallel using self-attention, where Query, Key, and
Value matrices let every token attend to every other token simultaneously
— solving long-range dependency issues that crippled older RNNs. I
understood the three training phases: pre-training (learning general
language from trillions of tokens), supervised fine-tuning (adapting to
a specific task), and RLHF (aligning outputs to human preferences). On
the practical side, I integrated the Groq API (free tier, Llama3-8b
model) and ran three sets of experiments: temperature at 0.0/0.7/1.5
showing how randomness scales; max_tokens at 15/50/200 confirming that
finish_reason='length' signals truncation; and top_p at 0.1/0.5/0.9
demonstrating vocabulary breadth changes. I also built a full chatbot
with a system message persona (Zara), multi-turn conversation history,
error handling for rate limits and connection failures, and per-turn
token tracking. The biggest realisation: LLMs have no internal state —
the entire conversation history must be re-sent with every API call,
which directly drives token usage.

## Research Sources

ChatGPT (GPT-4o) via chat.openai.com — API parameter trade-offs;
Gemini via gemini.google.com — Q/K/V attention visualisation; Claude
via claude.ai — LLM limitations and RLHF; Jay Alammar, The Illustrated
Transformer (jalammar.github.io/illustrated-transformer/) and OpenAI
Tokenizer (platform.openai.com/tokenizer) (consulted June 13, 2026).

**Clearest Explanation:** Jay Alammar's Illustrated Transformer — the
animated step-by-step diagrams make the Q/K/V attention computation
intuitive where text descriptions alone leave it abstract.

## Personal Insight

Working with a real LLM API for the first time made everything concrete.
When I saw finish_reason='length' after setting max_tokens=15 and watched
the response cut off mid-sentence, the abstract idea of token limits
became a real engineering constraint. The chatbot task also permanently
changed how I think about AI memory — there is no magic, just a growing
list being re-sent every turn. That immediately made me think about
efficiency: every extra turn costs more tokens. Using Groq's free tier
also taught me that the API interface is standardised enough that
switching providers only requires changing three lines of code, which
shows how well the industry has converged on OpenAI's API structure.

---

# Day 16 — LangChain Setup & First Chains

## What I Learned
LangChain is a framework for building LLM applications: it hides raw API
plumbing behind reusable components — Models, Prompts, Chains, and Memory. I
wrapped Groq's `llama-3.3-70b-versatile` with `ChatGroq` and built my first
chain using **LCEL**, where the `|` operator pipes Runnables into a
`RunnableSequence` (`prompt | model | parser`). The same pipe gives `.invoke`,
`.stream`, and `.batch` for free. I practised the four core document loaders —
`TextLoader`, `PyPDFLoader`, `CSVLoader`, `WebBaseLoader` — and learned they all
emit the same `Document` shape (`page_content` + `metadata`), which let me write
one generic `load_any()` dispatcher and a format-agnostic Q&A chain. I also
added a character budget that truncates oversized documents so I stay inside the
model's context window.

## Research Sources (consulted 2026-06-14)
- ChatGPT, Gemini, Claude — concept cross-check (see notebook comparison table)
- LangChain 1.0 release notes / official docs (release policy, LCEL)
- A practitioner article on the 1.0 rewrite and package split

**Clearest Explanation:** LCEL is just Unix pipes for LLM steps — each
component's output becomes the next one's input.

## Personal Insight
Truncation is a band-aid; the real fix is retrieval (chunk + embed + vector
store), which is exactly where the roadmap heads next.

---

# Day 17 — Text Embeddings & Semantic Search

## What I Learned
Embeddings turn text into dense vectors so that meaning becomes geometry:
semantically similar sentences land close together in high-dimensional space.
I implemented cosine similarity from scratch — `(a·b)/(‖a‖‖b‖)` — and used it to
confirm that *dog* and *puppy* score high while *dog* and *car* score low. I
built a 60-sentence semantic search engine that ranks results by meaning rather
than keywords, and a document tool that clusters articles by a cosine threshold
and flags near-duplicates above 0.95. Since Groq has no embeddings endpoint, I
used the free local model `all-MiniLM-L6-v2` (384 dims) via
`langchain-huggingface`, then mirrored the from-scratch search with a real
FAISS vector store.

## Research Sources (consulted 14 Jun 2026)
ChatGPT, Gemini, Claude, plus OpenAI's "New embedding models" post and
Pinecone's "What are Vector Embeddings" article. Full comparison table is in
`day17.ipynb`.

**Clearest Explanation:** an embedding model maps text to a point in space where
distance ≈ difference in meaning, so we compare points with cosine similarity.

## Personal Insight
Seeing the query words *absent* from the top search hits made semantic search
click — it's matching ideas, not strings. That reframes how I'll build RAG. I
also learned thresholds are model-dependent: a loose paraphrase scored 0.62
(related) while a near-identical rewrite scored 0.966 (duplicate), so clustering
and de-duplication need different cut-offs, and textbook OpenAI-calibrated
values don't transfer unchanged to a local 384-dim model.

---

# Day 18 — Text Splitters & Chunking Strategies

## What I Learned
Chunking is the step that decides how good retrieval can ever be — it
runs right before the Day 17 embedding + FAISS stage. I learned why we
chunk (LLM context limits, embedding-model input caps, and retrieval
precision) and compared four strategies: fixed-size, sentence-based,
recursive, and semantic. I built three things: a comparison of
`CharacterTextSplitter` (blunt fixed 500-char cuts) vs
`RecursiveCharacterTextSplitter` (500/50, structure-aware); a chunk-size
experiment across 200/500/1000/2000 chars measuring chunk count and
vector-store footprint; and a smart processor that detects document
type and routes `.md` to `MarkdownHeaderTextSplitter`, `.py` to
`PythonCodeTextSplitter`, and prose to the recursive splitter, attaching
source/section/token metadata to every chunk. Real result: the fixed
splitter cut 2 of 5 chunks mid-word; recursive cut 0 of 6. Storage fell
from ~26 KB (200 chars) to ~3 KB (2000 chars) on the same document.

## Research Sources (consulted 15 Jun 2026)
ChatGPT, Gemini, Claude, plus Firecrawl's 2026 chunking guide and
Weaviate's RAG chunking guide. Full comparison table is in the notebook.

**Clearest Explanation:** Start with recursive splitting at ~400–512
tokens and 10–20% overlap; only reach for semantic chunking once you've
measured that the simple default is the bottleneck. (Firecrawl)

## Personal Insight
The threshold lesson from Day 17 carried straight over: parameters must
fit the actual model. A ~0.45 similarity cutoff is "on topic" for
`all-MiniLM-L6-v2`, where textbook 0.9 returns nothing. Chunking is a
design choice, not preprocessing — overlap is the cheap insurance that
keeps an idea alive when it straddles a boundary.

---

# Day 19 — Prompt Engineering Mastery

## What I Learned
I compared three prompting techniques on a 3-class sentiment task (20
labeled samples) and measured each on accuracy, latency, and approximate
token cost. On the live Groq run, zero-shot scored 90%, few-shot 100%, and
CoT 95% — few-shot gave the biggest lift while CoT cost ~2x the tokens and
latency for no gain here. **Zero-shot** is the cheapest baseline and enough
for easy, common tasks. **Few-shot** (3 examples) is the biggest practical lever: it
locks the output format and lifts consistency on borderline cases.
**Chain-of-Thought** adds reasoning steps that help ambiguous inputs but
costs more tokens and latency, so I reserve it for hard cases. I built a
JSON prompt-template library for summarization, extraction, generation, and
analysis — each with a system message, a `{text}/{format}/{constraints}/`
`{examples}` user template, and an output spec — then wrote a renderer that
only fills known placeholders so JSON braces survive. For output control I
wrote validators (schema check, markdown-table checker, code-gen check) and
proved them on 11 good/edge/malformed cases. Everything uses LangChain LCEL
(`prompt | model | parser`) with `ChatGroq`, key read from `.env`.

## Research Sources (consulted 15 Jun 2026)
ChatGPT, Gemini, Claude, plus DAIR Prompt Engineering Guide, IBM Think
(zero-shot), and DigitalOcean prompt-engineering best practices.

**Clearest Explanation:** DigitalOcean — vague asks yield vague output;
specificity plus format and constraints is most of the battle.

## Personal Insight
Validators matter more than clever prompts: a strict schema turns a flaky
model into a dependable component, because bad output is caught, not shipped.