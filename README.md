
# ESILV Smart Assistant

Description
-----------

ESILV Smart Assistant is a prototype conversational assistant developed as a university project. It combines a Retrieval-Augmented Generation (RAG) system to answer factual questions from a document collection with specialized agents (orchestrator, retrieval, answer) to manage the dialogue. The project also includes an ML experiment pipeline in the notebook `Projet_ML.ipynb` demonstrating a genetic programming workflow (DEAP) coupled with active learning and ensemble learning for a classification task (dataset `atlas-higgs.csv`).

Key points
----------

- Web interface: Streamlit application (`app.py`) providing the chatbot UI.
- Agent architecture: see `agents/` (orchestrator, retrieval_agent, answer_agent).
- RAG: modules under `rag/` (context retrieval, answer service).
- ML experiments: notebook `Projet_ML.ipynb` (preprocessing, GP via DEAP, active learning, ensemble).
- Analytics & tracking: `analytics/` (DB, logging, leads, metrics).

Repository structure
--------------------

- `app.py`: Streamlit app (UI, routing, agents integration).
- `agents/`: orchestrator, retrieval and answer agents.
- `rag/`: RAG components (retrieval, answer service).
- `llm/`: LLM client (e.g., `ollama_client.py`).
- `ingestion/`, `data/`, `processed/`: scripts and files for ingestion and data preparation.
- `analytics/`: utilities for metrics collection, logging and lead handling.
- `notebooks/` and `Projet_ML.ipynb`: ML experimentation notebook.

Main dependencies
-----------------

The project uses (non-exhaustive):

- Python >= 3.8
- `streamlit` (UI)
- `numpy`, `pandas`, `scikit-learn` (preprocessing, metrics)
- `matplotlib`, `seaborn`
- `deap` (genetic programming)
- `modAL` (active learning)
- `chromadb` / other indexing systems if you use a vector DB for RAG (optional)

A `requirements.txt` file is provided to quickly install the main dependencies.

Installation
------------

1. Create a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Notes:
- Some specific packages (e.g., `deap`, `modAL`) may require additional installation steps. The notebook includes `!pip install ...` cells for `deap` and `modAL`.

Data
----

The notebook `Projet_ML.ipynb` expects the file `atlas-higgs.csv`. Place this file at the repository root (or adjust the path inside the notebook) before running the cells.

Run the Streamlit application
----------------------------

The chatbot UI is served by `app.py`. To run the app locally:

```bash
streamlit run app.py
```

The app expects an `assets/` folder containing `chatbot_head.png` (used as the logo), and relies on the `agents` and `rag` modules to generate responses.

Run the ML experiment notebook
-----------------------------

The notebook `Projet_ML.ipynb` contains the full experimental pipeline (preprocessing, GP via DEAP, active learning, ensemble). To reproduce the experiments:

1. Install the dependencies (see `requirements.txt`), especially `deap` and `modAL`.
2. Open the notebook with Jupyter / JupyterLab / VS Code and run the cells in order.

Note: The notebook samples 10% of the dataset by default to reduce computational cost. Some cells perform inline package installation (`!pip install deap`, `!pip install -q modAL-python`).

Architecture and agents
-----------------------

- `agents/orchestrator.py`: detects intent (contact / rag / clarification) and delegates to `retrieval_agent` or `answer_agent`.
- `agents/retrieval_agent.py`: queries the index/document store to retrieve relevant contexts (sources, similarities).
- `agents/answer_agent.py`: builds responses using retrieved context (RAG) or returns clarification answers.

RAG & indexing
--------------

The `rag/` submodule contains components for context retrieval and the answer service. Depending on your local setup you can use a vector DB (Chroma, FAISS, etc.) or a simple store.

Analytics / Tracking
--------------------

The `analytics/` folder contains utilities to:

- initialize a SQLite tracking DB (`db.py`),
- log interactions (`logger.py`),
- save leads (`leads.py`) and detect the theme of a question (`themes.py`).

Tests
----

A `test.py` file exists at the repository root for quick tests. Run it with:

```bash
python test.py
```

Reproducibility best practices
-----------------------------

- Run the notebook and the app in the same Python environment (matching package versions).
- Install `deap` and `modAL` before executing the corresponding notebook cells.
- Ensure the dataset `atlas-higgs.csv` is available before running `Projet_ML.ipynb`.

Contributing
------------

1. Fork the repository
2. Create a feature branch
3. Open a Pull Request with a description of changes

Contact
-------

For questions about the project, contact the repository owner or open an issue.

License
-------

Specify the desired license here (e.g., MIT) if applicable.
