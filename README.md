# ESILV Smart Assistant  
### RAG-based Multi-Agent Academic Chatbot

## Project Overview

The **ESILV Smart Assistant** is a conversational academic assistant designed to help students access reliable and up-to-date institutional information.  
The system is based on a **Retrieval-Augmented Generation (RAG)** architecture and leverages a **multi-agent design** to provide accurate, document-grounded answers while minimizing hallucinations.

This project was developed as part of the **LLM and Generative AI** course at **ESILV (2025–2026)**.

---

## Objectives

- Provide an intelligent assistant for querying ESILV institutional documents
- Reduce hallucinations through document-grounded generation
- Implement a complete and reproducible RAG pipeline
- Support both local and cloud-based LLM inference
- Offer analytics and evaluation tools for system monitoring

---

## System Architecture

The system follows a modular, layered architecture:

- **User Interface**: Streamlit web application
- **Multi-Agent Orchestration**:
  - Orchestrator Agent
  - Retrieval Agent
  - Answer Generation Agent
- **RAG Pipeline**:
  - Document ingestion
  - Text cleaning and chunking
  - Embedding generation
  - Vector indexing (ChromaDB)
  - Similarity-based retrieval
  - Context-aware answer generation
- **Analytics Layer**:
  - Interaction logging
  - Metrics computation
  - Theme detection
  - Automated reporting

---

## Technologies Used

- **Python 3.10+**
- **Streamlit** – User interface
- **Retrieval-Augmented Generation (RAG)**
- **ChromaDB** – Vector database
- **Sentence Transformers** – Text embeddings
- **Ollama** – Local LLM inference (open-source models)
- **Google AI SDK (Gemini)** – Optional cloud-based inference
- **SQLite** – Analytics data storage

All tools and models used are **open-source or academic-friendly**, in compliance with course guidelines.

---

## Repository Structure

```
.
├── app.py                  # Streamlit application entry point
├── agents/                 # Multi-agent orchestration
│   ├── orchestrator.py
│   ├── retrieval_agent.py
│   └── answer_agent.py
│
├── ingestion/              # RAG ingestion pipeline
│   ├── extract_text.py
│   ├── scraping.py
│   ├── chunking.py
│   ├── build_index.py
│   └── pipeline.py
│
├── analytics/              # Evaluation and analytics
│   ├── db.py
│   ├── logger.py
│   ├── metrics.py
│   ├── themes.py
│   ├── report.py
│   └── seed_fake_data.py
│
├── data/
│   ├── raw/                # Raw documents (PDF, web)
│   ├── processed/          # Cleaned text
│   ├── chroma/             # Vector database
│   └── chunks.jsonl        # Chunked documents
│
├── notebooks/              # Evaluation notebooks
│   └── evaluation.ipynb    # Notebook demonstrating query examples, accuracy metrics, and latency plots
│
├── llm/                    # LLM clients and wrappers
│   └── ollama_client.py    # Local LLM inference client
│
├── pages/                  # Streamlit page modules
│   └── 1_Admin.py
│
├── assets/                 # UI assets and branding
├── requirements.txt
├── README.md
└── test.py
``` 
---

## Installation 
### 1. Clone repository
```
git clone <repository_url>
cd ESILV_SMART_ASSISTANT
```

### 2.Create a virtual environment 
```python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```pip install -r requirements.txt```

---

## Environment Variables
Create a .env file 
```
OLLAMA_MODEL=llama3
GOOGLE_API_KEY=your_api_key_here
VECTOR_DB_PATH=data/chroma
```

---

## Running the Application
### 1. Build the vetor database
```
python ingestion/pipeline.py
```

### 2.Launch the Streamlit app
```
streamlit run app.py
```
The application will be available at:
http://localhost:8501

---

## Analytics and Evaluation
The system automatically logs user interactions and computes:
- Response times
- Query statistics
- Retrieval usage
- Thematic distribution of queries
Analytics data are stored in a local database and can be summarized using automated report generated from the analytics/ module.

---

## Reproducibility
- All data processing steps are deterministic
- The vector database can be fully rebuilt from raw documents
- No proprietary datasets are required 
- The project runs on a standard Python environment

---

## Team
- Ornella Djuidje Kandem
- Cassie Doguet
- Léna Dubois
