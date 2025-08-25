from typing import List, Dict, Any, Tuple
import threading
from .utils import text_to_embedding, cosine_similarity

class InMemoryVectorStore:
    def __init__(self):
        self._lock = threading.Lock()
        self._store: List[Dict[str, Any]] = []  # {id, text, metadata, embedding}

    def add_text(self, id: str, text: str, metadata: Dict = None, embedding: List[float] = None):
        if embedding is None:
            embedding = text_to_embedding(text)
        rec = {"id": id, "text": text, "metadata": metadata or {}, "embedding": embedding}
        with self._lock:
            self._store.append(rec)
        return rec

    def bulk_add(self, items: List[Dict[str, Any]]):
        with self._lock:
            for it in items:
                emb = it.get("embedding") or text_to_embedding(it["text"])
                self._store.append({
                    "id": it["id"],
                    "text": it["text"],
                    "metadata": it.get("metadata", {}),
                    "embedding": emb
                })

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        with self._lock:
            if not self._store:
                return []
            embeddings = [r["embedding"] for r in self._store]
            sims = cosine_similarity(query_embedding, embeddings)
            scored = []
            for r, s in zip(self._store, sims):
                scored.append((s, r))
            scored.sort(key=lambda x: x[0], reverse=True)
            top = scored[:top_k]
            return [{"score": float(s), "id": r["id"], "text": r["text"], "metadata": r["metadata"]} for s, r in top]
