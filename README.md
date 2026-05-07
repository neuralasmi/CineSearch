# CineSearch — AI Content Discovery Engine

Semantic search and Q&A across a movie/series catalog using Retrieval-Augmented Generation (RAG).

## What It Does
- Ingest movie metadata and plot summaries as documents
- Chunk text with LangChain's RecursiveCharacterTextSplitter
- Embed chunks via sentence-transformers (all-MiniLM-L6-v2)
- FAISS vector index for sub-50ms similarity search
- Generate answers with Ollama (Llama3) grounded in retrieved context
- FastAPI streaming API with Server-Sent Events
- Docker Compose: one command local setup

## Architecture
[Ingester] -> [Chunker] -> [Embedder] -> [FAISS Index]
                                           |
[User Query] -> [Retriever] -> [Grounded Generator] -> [Streaming Response]

## Tech Stack
Python | LangChain | FAISS | sentence-transformers | Ollama (Llama3) | FastAPI | Docker

## Quick Start
```bash
git clone https://github.com/neuralasmi/CineSearch
cd CineSearch
docker-compose up --build
# Visit http://localhost:8000/docs for interactive API
```

## API Endpoints
- POST /ingest -- Ingest documents into the vector store
- POST /query -- Ask a question, get a streaming RAG response  
- GET /health -- Health check
