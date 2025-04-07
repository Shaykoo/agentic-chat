# FastAPI + RAG Backend

This backend powers a Retrieval-Augmented Generation (RAG) system using FastAPI, LangChain, and Ollama. It handles file uploads, creates vector embeddings, and queries context-aware responses.

## Endpoints

- `POST /query`: Ask a question using `user_id` and `query`.
- `POST /upload`: Upload PDF files for embedding.

## Running

```bash
uvicorn app.main:app --reload
