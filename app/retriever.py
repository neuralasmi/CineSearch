import faiss
import numpy as np
from app.embed import embed_texts

class Retriever:
    def __init__(self, dim: int = 384):
        self.index = faiss.IndexFlatL2(dim)
        self.documents = []

    def add_documents(self, texts: list[str], embeddings: np.ndarray):
        self.index.add(embeddings.astype('float32'))
        self.documents.extend(texts)

    def search(self, query: str, top_k: int = 5) -> list[tuple[str, float]]:
        q_emb = embed_texts([query]).astype('float32')
        D, I = self.index.search(q_emb, top_k)
        return [(self.documents[i], float(D[0][j])) for j, i in enumerate(I[0]) if i < len(self.documents)]

retriever = Retriever()
