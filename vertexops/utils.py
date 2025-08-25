import hashlib
import numpy as np
from typing import List

# Deterministic dummy embeddings: convert text -> fixed-size vector via sha256 bytes
EMBED_DIM = 128

def text_to_embedding(text: str, dim: int = EMBED_DIM) -> List[float]:
    """
    Deterministic pseudo-embedding for local testing. Replace with real model embeddings.
    """
    h = hashlib.sha256(text.encode("utf-8")).digest()
    # Repeat bytes to ensure enough length
    buf = (h * ((dim // len(h)) + 1))[:dim]
    vec = np.frombuffer(buf, dtype=np.uint8).astype(float)
    # normalize and shift to roughly [-0.5, 0.5]
    vec = (vec / 255.0) - 0.5
    # convert to python list
    return vec.tolist()

def cosine_similarity(query_vec, matrix):
    import numpy as np
    q = np.array(query_vec)
    M = np.array(matrix)
    q_norm = np.linalg.norm(q) + 1e-12
    M_norms = np.linalg.norm(M, axis=1) + 1e-12
    sims = (M @ q) / (M_norms * q_norm)
    return sims.tolist()
