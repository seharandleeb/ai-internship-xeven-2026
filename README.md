# AI Engineer Internship — Xeven Solutions 2026

A 30-day internship program at Xeven Solutions focused on building
practical skills in Python, Machine Learning, and AI development
through daily hands-on work.

---

## Intern Details

| Field      | Details            |
| ---------- | ------------------ |
| Name       | Sehar Andleeb      |
| Role       | AI Engineer Intern |
| Company    | Xeven Solutions    |
| Duration   | 2 months           |
| Start Date | June 8, 2026       |

---

## Tools and Technologies

- Python 3.13
- VS Code
- Git and GitHub
- UV Virtual Environment
- Jupyter Notebook
- Groq API (free tier) — Llama 3.3
- LangChain (LCEL) — chains, document loaders
- Hugging Face `sentence-transformers` & FAISS — embeddings + semantic search (Day 17)
- FastAPI + Uvicorn — REST APIs, Pydantic validation, Swagger docs (Day 24)

---

## Project Structure

```
ai-internship-xeven-2026/
├── README.md                  # Overview + daily progress table
├── LEARNINGS.md               # Daily ~200-word learning summaries
├── requirements.txt           # Shared dependencies
├── .gitignore                 # Ignores logs, __pycache__, scratch files
│
├── day01/                     # AI fundamentals + environment setup
│   ├── app.py
│   ├── day01.ipynb
│   └── images/                 # Setup verification screenshots
├── day02/                     # Variables, data types, I/O
│   ├── calculator.py
│   ├── data_types.py
│   ├── input_output.py
│   ├── type_conversion.py
│   ├── variables.py
│   └── day02.ipynb
├── day03/                     # Conditionals & decision logic
│   ├── age_verification.py
│   ├── grade_calculator.py
│   ├── number_classifier.py
│   ├── simple_grade_calculator.py
│   └── day03.ipynb
├── day04/                     # Operators & precedence
│   ├── advanced_calculator.py
│   ├── login_system.py
│   ├── operator_precedence.py
│   ├── type_conversion.py
│   ├── day04_operators_notebook.ipynb
│   └── practical/
│       ├── task1_advanced_login.py
│       └── task2_calculator.py
├── day05/                     # ML concepts
│   ├── decision_tree.py
│   ├── ml_concepts.py
│   ├── regression_vs_classification.py
│   ├── day05.ipynb
│   └── practical_tasks/
│       ├── decision_tree_simulator.py
│       └── transcript.md
├── day06/                     # Lists & list operations
│   ├── list_basics.py
│   ├── list_operations.py
│   ├── student_management.py
│   ├── day06.ipynb
│   └── practical_task/
│       ├── grade_tracker.py
│       ├── list_slicing.py
│       └── student_management.py
├── day07/                     # Week 1 review
│   └── FEEDBACK_WEEK1.md
├── day08/                     # Data structures in practice
│   ├── data_cleaning_pipeline.py
│   ├── shopping_cart.py
│   ├── student_grade_manager.py
│   └── day08.ipynb
├── day09/                     # Validation & regex
│   ├── email_validation.py
│   ├── geographic_coordinates.py
│   ├── visitor_tracker.py
│   └── day09.ipynb
├── day10/                     # Dictionaries & JSON persistence
│   ├── configuration_manager.py
│   ├── product_inventory_manager.py
│   ├── student_information_system.py
│   ├── *.json                 # Config/inventory/student data files
│   └── day10.ipynb
├── day11/                     # Loops & iteration pipelines
│   ├── data_processing_pipeline.py
│   ├── number_analysis_system.py
│   ├── pattern_generators.py
│   └── day11.ipynb
├── day12/                     # Functions Fundamentals
│   ├── math_utils.py
│   ├── text_processing.py
│   ├── validators.py
│   └── day12.ipynb
├── day13/                     # Advanced Functions
│   ├── flexible_logger.py         # *args/**kwargs logger
│   ├── data_transformer.py        # lambda + map/filter/sorted
│   ├── comprehensions_toolkit.py  # list/dict comprehensions
│   └── day13.ipynb
├── day14/                     # Week 2 Review & Mini-Project
│   ├── data_structures_cheatsheet.py  # Task 1: List/Tuple/Set/Dict
│   ├── contact_manager.py             # Task 2: Contact Management System
│   └── day14.ipynb
├── day15/                     # Introduction to LLMs — Week 3 Start
│   ├── task1_openai_setup.py      # Basic API call + temperature experiment
│   ├── task2_parameter_exploration.py  # temperature/max_tokens/top_p tests
│   ├── task3_chatbot.py           # Chatbot with history + error handling
│   └── day15.ipynb                # Concepts, research, task demonstrations
├── day16/                     # LangChain Setup & First Chains
│   ├── task1_setup_first_chain.py   # ChatGroq setup + first LCEL chain
│   ├── task2_document_loaders.py    # Text/PDF/CSV/Web loaders + generic loader
│   ├── task3_document_qa_chain.py   # Document Q&A chain (LCEL) + context guard
│   ├── day16.ipynb                  # Concepts, research table, task demos
│   └── samples/                     # Auto-created sample.txt / .csv / .pdf
└── day17/                     # Text Embeddings & Semantic Search
│   ├── day17.ipynb                             # Concepts, research table, task demos, FAISS bonus
│   └── scripts/
│      ├── day17_task1_embeddings_compare.py   # cosine from scratch + similarity heatmap
│      ├── day17_task2_semantic_search.py      # 60-sentence semantic search engine
│      ├── day17_task3_document_similarity.py  # clustering + near-duplicate finder + t-SNE
│      └── outputs/                            # Auto-generated heatmap + t-SNE plots
├── day18/
│   ├── scripts/
│   │   ├── task1_compare_chunking.py
│   │   ├── task2_chunk_size_experiment.py
│   │   └── task3_smart_processor.py
│   └── day18.ipynb
├── day19/
│   ├── day19.ipynb
│   ├── LEARNINGS.md
│   └── scripts/
│       ├── task1_technique_comparison.py
│       ├── task2_template_library.py
│       ├── task3_output_control.py
│       └── outputs/
│           ├── task1_results.json
│           ├── prompt_templates.json
│           ├── task2_render_report.json
│           └── task3_robustness.json
├── day20/                     # Structured Outputs with Pydantic
│   ├── scripts/
│   │   ├── task1_pydantic_models.py      # Person/Product + validators
│   │   ├── task2_structured_pipeline.py  # Article pipeline (retry/fallback)
│   │   ├── task3_entity_extraction.py    # Company→Employee[] + accuracy
│   │   └── outputs/                       # Auto-generated JSON reports
│   └── day20.ipynb                        # Theory, research table, demos
├── day21/                     # Week 3 Review — integrated Document Analyzer
│   ├── day21.ipynb                     # Architecture, live demo, research table
│   ├── architecture.md                 # System diagram + component explanation
│   ├── REFLECTION.md                   # What worked / what I'd do differently
│   ├── FEEDBACK_WEEK3.md               # Feedback received + Week 4 action items
│   ├── LEARNINGS.md                    # ~200-word Day 21 summary
│   └── scripts/
│       ├── app.py                  ← Streamlit UI (what you run)
│       ├── document_loader.py          # Load PDF/text + auto-create samples
│       ├── chunker.py                  # RecursiveCharacterTextSplitter (tuned)
│       ├── embeddings_index.py         # MiniLM/offline embeddings + FAISS search
│       ├── entity_extraction.py        # Pydantic v2 + Groq structured output
│       ├── analyzer.py                 # Orchestrates load→chunk→index→search→extract
│       ├── run_demo.py                 # CLI entry point (--live flag)
│       ├── analyze_my_doc.py           # Run the pipeline on your own PDF/text
│       ├── verify_pipeline.py          # 6 offline wiring assertions
│       └── outputs/                    # Auto-generated analysis_report.json
├── day22/
│   ├── scripts/
│   │   ├── task1_faiss_operations.py
│   │   ├── task2_document_library.py
│   │   ├── task3_vector_store_comparison.py
│   │   └── outputs/
│   │       ├── task1/faiss_index/
│   │       ├── task2/stats.json
│   │       └── task3/comparison_report.json
│   ├── day22.ipynb
├── day23/
│   ├── scripts/
│   │   ├── task1_simple_rag.py
│   │   ├── task2_enhanced_rag.py
│   │   ├── task3_multi_doc_rag.py
│   │   └── outputs/
│   ├── dashboard/
│   │   ├── app.py
│   │   ├── templates/index.html
│   │   └── static/style.css
│   └── day23.ipynb
├── day24/                     # Advanced Context Management & FastAPI
│   ├── api/
│   │   ├── main.py                 # Task 2: first FastAPI app (health, items, Pydantic body)
│   │   └── rag_api.py              # Task 3: RAG wrapped in POST /ask (lifespan startup)
│   ├── scripts/
│   │   ├── rag_core.py             # Offline embedder + FAISS store + retrieval
│   │   ├── rag_chain.py            # Retrieval + Groq answer layer
│   │   ├── conversation_memory.py  # Message-list memory (recent verbatim + summary)
│   │   ├── conversational_rag.py   # Task 1: conversational RAG with memory
│   │   └── outputs/
│   └── day24.ipynb                 # Concepts, two research tables, documented runs
```

Each `dayXX/` folder contains the day's task scripts and a `dayXX.ipynb`
notebook that explains the concepts and demonstrates every task with
executed output.

> **Day 17 note:** This day uses local embeddings (`sentence-transformers`,
> model `all-MiniLM-L6-v2`, 384-dim) and FAISS, since Groq has no embeddings
> endpoint. Run it inside a **Python 3.12** environment — `faiss-cpu` does not
> yet ship a wheel for Python 3.13. Extra packages: `langchain-huggingface`,
> `sentence-transformers`, `faiss-cpu`, `scikit-learn`, `matplotlib`.

---

## Daily Progress

| Day | Topic | Key Files | Status |
|-----|-------|-----------|--------|
| 01 | Python basics, Git & GitHub setup | `app.py`, `day01.ipynb` | ✅ Done |
| 02 | Variables, Data Types, I/O, Type Conversion | `variables.py`, `data_types.py`, `calculator.py`, `day02.ipynb` | ✅ Done |
| 03 | Conditional Statements and Logic | `age_verification.py`, `grade_calculator.py`, `number_classifier.py`, `day03.ipynb` | ✅ Done |
| 04 | Operators, Precedence, Type Conversion | `advanced_calculator.py`, `login_system.py`, `operator_precedence.py`, `day04.ipynb` | ✅ Done |
| 05 | ML Concepts — Supervised, Unsupervised, Decision Trees | `ml_concepts.py`, `decision_tree.py`, `regression_vs_classification.py`, `day05.ipynb` | ✅ Done |
| 06 | Python Data Structures — Lists | `list_basics.py`, `list_operations.py`, `student_management.py`, `day06.ipynb` | ✅ Done |
| 07 | Week 1 Review and Self-Assessment | `FEEDBACK_WEEK1.md`, `day07.ipynb` | ✅ Done |
| 08 | Tuples, Sets, Advanced List Operations | `data_cleaning_pipeline.py`, `shopping_cart.py`, `student_grade_manager.py`, `day08.ipynb` | ✅ Done |
| 09 | Dictionaries and Hashmaps | `geographic_coordinates.py`, `visitor_tracker.py`, `email_validation.py`, `day09.ipynb` | ✅ Done |
| 10 | Dictionaries & JSON | `student_info_system.py`, `inventory_manager.py`, `config_manager.py`, `day10.ipynb` | ✅ Done |
| 11 | Loops & Iteration | `data_processing_pipeline.py`, `pattern_generators.py`, `number_analysis_system.py`, `day11.ipynb` | ✅ Done |
| 12 | Functions Fundamentals | `math_utils.py`, `text_processing.py`, `validators.py`, `day12.ipynb` | ✅ Done |
| 13 | Advanced Functions (`*args`/`**kwargs`, lambda, comprehensions) | `flexible_logger.py`, `data_transformer.py`, `comprehensions_toolkit.py`, `day13.ipynb` | ✅ Done |
| 14 | Week 2 Review & Mini-Project (Contact Management System) | `data_structures_cheatsheet.py`, `contact_manager.py`, `day14.ipynb` | ✅ Done |
| 15 | Introduction to LLMs — Transformer architecture, API integration, Chatbot | `task1_openai_setup.py`, `task2_parameter_exploration.py`, `task3_chatbot.py`, `day15.ipynb` | ✅ Done |
| 16 | LangChain Setup & First Chains — LCEL, document loaders, Q&A chain | `task1_setup_first_chain.py`, `task2_document_loaders.py`, `task3_document_qa_chain.py`, `day16.ipynb` | ✅ Done |
| 17 | Text Embeddings & Semantic Search — cosine from scratch, semantic search, clustering & near-duplicate detection | `day17_task1_embeddings_compare.py`, `day17_task2_semantic_search.py`, `day17_task3_document_similarity.py`, `day17.ipynb` | ✅ Done |
| 18 | Text Splitters & Chunking Strategies — fixed vs recursive comparison, optimal chunk-size experiment, smart type-aware processor | `task1_compare_chunking.py`, `task2_chunk_size_experiment.py`, `task3_smart_processor.py`, `day18.ipynb` | ✅ Done |
| 19 | Prompt Engineering — technique comparison, template library, output control | task1_technique_comparison.py, task2_template_library.py, task3_output_control.py, day19.ipynb | ✅ Done |
| 20 | Structured Outputs with Pydantic — model suite + validators, LLM→structured pipeline (retry/fallback), nested multi-entity extraction with accuracy scoring | `task1_pydantic_models.py`, `task2_structured_pipeline.py`, `task3_entity_extraction.py`, `day20.ipynb` | ✅ Done |
| 21 | Week 3 Review — integrated Document Analyzer (load → chunk → FAISS semantic search → Pydantic extraction → report) + technical presentation | `run_demo.py`, `analyzer.py`, `embeddings_index.py`, `entity_extraction.py`, `day21.ipynb` | ✅ Done |
| 22 | Vector Stores & Databases — FAISS operations, document library with metadata, FAISS vs Chroma comparison | `task1_faiss_operations.py`, `task2_document_library.py`, `task3_vector_store_comparison.py`, `day22.ipynb` | ✅ Done |
| 23 | RAG Pipeline Development — simple RAG, enhanced RAG with custom prompts, multi-document RAG | `task1_simple_rag.py`, `task2_enhanced_rag.py`, `task3_multi_doc_rag.py`, `day23.ipynb` | ✅ Done |
| 24 | Advanced Context Management & FastAPI — conversational RAG with memory (recent-verbatim + summarized-older pruning), FastAPI fundamentals (path/query params, Pydantic validation, Swagger docs), RAG wrapped in `POST /ask` with lifespan startup + HTTP error handling | `rag_core.py`, `conversation_memory.py`, `conversational_rag.py`, `main.py`, `rag_api.py`, `day24.ipynb` | ✅ Done |
---

## How to Run

Clone the repository:

```
git clone https://github.com/seharandleeb/ai-internship-xeven-2026.git
```

Navigate to the folder:

```
cd ai-internship-xeven-2026
```

Activate the virtual environment:

```
.venv\Scripts\activate
```

Install dependencies:

```
uv pip install -r requirements.txt
```

Run a script:

```
cd day15
python task1_openai_setup.py
```

> **Day 17 only:** create a Python 3.12 environment for the embeddings stack
> (`uv venv .venv312 --python 3.12`), activate it, then
> `uv pip install langchain-huggingface sentence-transformers faiss-cpu langchain-community numpy scikit-learn matplotlib`.
> Run the scripts from inside `day17/scripts/` (they save plots to `outputs/`
> relative to that folder). The first run downloads the MiniLM model once
> (~80 MB), then caches it.

> **Day 21 (integrated Document Analyzer):** use the same Python 3.12 env
> (`.venv312`). From `day21/scripts/`:
> `python run_demo.py` runs the pipeline **offline** (deterministic embedder
> + offline extraction stub, no model download / no API key);
> `python run_demo.py --live` runs the **real** stack (MiniLM embeddings +
> Groq `llama-3.3-70b-versatile` structured extraction, needs `GROQ_API_KEY`
> in a local `.env`); `python verify_pipeline.py` runs the six offline wiring
> checks; and `python analyze_my_doc.py <file> "<query>"` runs the pipeline
> on your own PDF/text file. Outputs land in `day21/scripts/outputs/`.

> **Day 24 (Context Management & FastAPI):** the RAG scripts use FAISS, so run
> them in the Python 3.12 env (`.venv312`); the Task 2 FastAPI basics use no
> FAISS and run in the default `.venv` (3.13). Install per env with
> `uv pip install fastapi uvicorn`.
> **Morning** — from `day24/scripts/` in `.venv312`:
> `python conversational_rag.py` runs the conversational RAG with memory
> (recent-verbatim + summarized-older pruning; needs `GROQ_API_KEY` in a local
> `.env`).
> **Afternoon** — from `day24/api/`: `python -m uvicorn main:app --reload`
> (in `.venv`) serves the basics API, and `python -m uvicorn rag_api:app --reload`
> (in `.venv312`) serves the RAG `POST /ask` endpoint. Visit
> `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

---

## Goals

- Strengthen Python programming foundations
- Learn core Machine Learning concepts
- Work with real datasets
- Build and evaluate ML models
- Gain practical project experience

---

## What is AI and the Role of an AI Engineer

Artificial Intelligence, or AI, is the ability of a computer to think
and learn like a human. Instead of being told exactly what to do, an
AI system learns from examples and experiences, just like how a child
learns to recognize a cat after seeing many cats.

We already use AI every single day without realizing it. When Netflix
suggests a show you might like, when Google Maps finds the fastest
route, when your phone unlocks with your face, or when Gmail filters
out spam — that is all AI working behind the scenes.

An AI Engineer is the person who builds these intelligent systems.
They collect and clean data, train the AI to learn from it, test
whether it is working correctly, and then deploy it so real people can
use it.

---

## Contact

- GitHub: https://github.com/seharandleeb
- Company: Xeven Solutions
- Email: seharm518@gmail.com