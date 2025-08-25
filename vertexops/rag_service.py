from typing import List, Dict, Any
from .vector_store import InMemoryVectorStore
from .utils import text_to_embedding
import os
import httpx
import time

# Simple RAG orchestrator. Use a real LLM or Vertex AI in production.
class RAGService:
    def __init__(self, vector_store: InMemoryVectorStore):
        self.vs = vector_store
        self.OPENAI_KEY = os.getenv("OPENAI_API_KEY") or None

    async def generate_response(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        q_emb = text_to_embedding(query)
        hits = self.vs.search(q_emb, top_k=top_k)
        # Build context
        context_texts = [h["text"] for h in hits]
        context = "\n\n".join(context_texts)
        # If OPENAI_API_KEY is provided, call OpenAI (text-davinci-like) to generate response.
        if self.OPENAI_KEY:
            # Minimal OpenAI call using httpx to keep dependency low (you can swap to openai pkg)
            prompt = f"Use the following context to answer the query.\nContext:\n{context}\n\nQuery: {query}\n\nAnswer:"
            headers = {"Authorization": f"Bearer {self.OPENAI_KEY}"}
            # Note: this is simplified; configure model and params as needed
            async with httpx.AsyncClient(timeout=15.0) as client:
                # Using the OpenAI Completion API (legacy) - adjust if using Chat Completions API
                payload = {"model": "text-davinci-003", "prompt": prompt, "max_tokens": 256}
                r = await client.post("https://api.openai.com/v1/completions", json=payload, headers=headers)
                if r.status_code == 200:
                    data = r.json()
                    text = data["choices"][0]["text"].strip()
                    confidence = sum([h["score"] for h in hits]) / (len(hits) or 1)
                    return {"response_text": text, "source_docs": hits, "confidence_score": float(confidence)}
                else:
                    # fallback to local response
                    pass
        # Local deterministic fallback: combine and return
        time.sleep(0.1)
        response = f"[SIMULATED LLM ANSWER]\nQuery: {query}\nContext snippets:\n" + "\n---\n".join(context_texts[:3])
        confidence = sum([h["score"] for h in hits]) / (len(hits) or 1)
        return {"response_text": response, "source_docs": hits, "confidence_score": float(confidence)}
