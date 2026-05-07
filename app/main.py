from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
from app.embed import embed_texts
from app.retriever import retriever

app = FastAPI(title="CineSearch", version="1.0.0")

class Query(BaseModel):
    question: str
    top_k: int = 5

class IngestItem(BaseModel):
    text: str
    source: str = "doc"

@app.get("/health")
async def health():
    return {"status": "healthy", "indexed": len(retriever.documents) if hasattr(retriever, 'documents') else 0}

@app.post("/ingest")
async def ingest(item: IngestItem):
    emb = embed_texts([item.text])
    retriever.add_documents([item.text], emb)
    return {"status": "ingested", "total": len(retriever.documents)}

@app.post("/query")
async def query(q: Query):
    async def stream():
        results = retriever.search(q.question, q.top_k)
        context = "\n".join([f"[{i+1}] {doc}" for i, (doc, score) in enumerate(results)])
        response = f"CineSearch AI: Based on {len(results)} retrieved documents, answering your question about '{q.question}'..."
        for word in response.split():
            yield f"data: {word} \n\n"
            await asyncio.sleep(0.04)
        yield "data: [DONE]\n\n"
    return StreamingResponse(stream(), media_type="text/event-stream")
