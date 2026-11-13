A stateful multi-agent Retrieval-Augmented Generation (RAG) and bilingual semantic search engine supporting *English and Tamil* queries. Built with *LangGraph, **FastAPI, **FAISS, and **PyTorch*, this system combines deterministic routing, automated query self-correction, dense vector retrieval, and abstractive summarization.

---

## Key Features

* *Stateful Multi-Agent Orchestration (graph_agent.py):* Uses a LangGraph StateGraph pipeline with conditional routing to sanitize inputs, trigger automated query recovery when needed, and execute vector retrieval.
* *Bilingual Semantic Vector Search (build_vector_vault.py, index.faiss):* Indexes domain knowledge (knowledge.txt) into dense vector embeddings for sub-millisecond semantic retrieval across Tamil and English queries.
* *High-Throughput REST API (app.py, main.py):* Exposes production endpoints via *FastAPI* and *Uvicorn* for low-latency search, inference, and document summarization (summarizer.py).
* *Runtime Observability & Stress Profiling (agent_logger.py, stress_profiler.py):* Tracks execution paths, latency baselines, and agent state transitions in agent_runtime_audit.txt.

---

## Architecture Flow

text
[User Query (Tamil / English)]
              │
              ▼
 ┌─────────────────────────┐
 │ linguistic_sanitization │  ◄── Cleans & normalizes input text
 └────────────┬────────────┘
              │
      (Conditional Edge)
       ├── trigger_recovery ──► [ self_correction_node ] ──┐
       │                                                   ▼
       └── trigger_search   ────────────────────────► [ vector_vault_node ] ──► [ Response / Summary ]


---

## Tech Stack

* *Agentic Framework:* LangGraph, LangChain (LCEL)
* *Backend & API:* Python, FastAPI, Uvicorn
* *Vector Database & ML:* FAISS, PyTorch, Hugging Face Transformers
* *Testing & Profiling:* Talend API Tester, cURL, custom verification suites (test_agent.py, test_search_api.py, stress_profiler.py)

---

## Project Structure

* app.py / main.py — FastAPI application entry points and route handlers.
* graph_agent.py — LangGraph multi-agent state machine and conditional routing logic.
* build_vector_vault.py — Embedding generation and FAISS index builder (index.faiss, index.pkl).
* summarizer.py — Abstractive text summarization module for retrieved context.
* agent_logger.py — Audit logger recording agent execution traces to agent_runtime_audit.txt.
* stress_profiler.py — Latency and throughput benchmarking script.
* requirements.txt — Python dependencies.

---

## Quick Start

1. *Clone the repository:*
   bash
   git clone https://github.com
   cd Aisvarya20-tamil-search-engine
   

2. *Create a virtual environment and install dependencies:*
   bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   

3. *Build the FAISS vector index (if regenerating):*
   bash
   python build_vector_vault.py
   

4. *Start the FastAPI server:*
   bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   

---

## API Verification & Testing

### 1. Server Health Check (cURL)
Verify that the Uvicorn server and vector index are running cleanly:
bash
curl -X GET http://127.0.0

(You can also inspect the interactive Swagger UI at http://127.0.0.)

### 2. Testing via Talend API Tester
To test bilingual semantic search and inference endpoints using the *Talend API Tester* Chrome extension:

* *Method:* POST
* *Endpoint URL:* http://127.0.0 (or /query depending on your route in app.py)
* *Headers:*
  * Content-Type: application/json
  * Accept: application/json

*Example 1 — English Query Payload:*
json
{
  "query": "What is Retrieval-Augmented Generation and how does semantic search work?"
}


*Example 2 — Tamil Query Payload:*
json
{
  "query": "செயற்கை நுண்ணறிவு என்றால் என்ன?"
}


* *Expected Response:* 200 OK with retrieved semantic chunks, confidence score, and summarized output.
