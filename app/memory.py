import faiss
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict

MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_FILE = "memory.index"
DATA_FILE = "memory.json"

embedder = SentenceTransformer(MODEL_NAME)
dimension = 384

if os.path.exists(INDEX_FILE):
    index = faiss.read_index(INDEX_FILE)
else:
    index = faiss.IndexFlatL2(dimension)

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        memory_store: List[Dict[str, str]] = json.load(f)
else:
    memory_store = []


def _is_duplicate_memory(text: str, category: str, embedding: np.ndarray, distance_threshold: float = 0.15) -> bool:
    """
    Return True if this memory is essentially already stored.

    We use FAISS to look for very close neighbors. If we find a memory with
    the same category and very small L2 distance, we skip saving it to avoid
    repeating the same fact over and over.
    """
    if index.ntotal == 0:
        return False

    # Search the closest few neighbors for strong matches
    _, indices = index.search(embedding.astype("float32"), min(5, index.ntotal))
    for idx in indices[0]:
        if idx < len(memory_store):
            item = memory_store[idx]
            if item.get("category") == category and item.get("text") == text:
                return True

    return False


def save_memory(text: str, category: str = "general"):
    """
    Persist a new memory with FAISS indexing, but avoid saving exact
    duplicates so the memory file stays clean and non-repetitive.
    """
    embedding = embedder.encode([text])
    embedding_arr = np.array(embedding).astype("float32")

    # Skip if this is clearly a duplicate of what we already know
    if _is_duplicate_memory(text, category, embedding_arr):
        return

    index.add(embedding_arr)

    memory_store.append({
        "text": text,
        "category": category
    })

    faiss.write_index(index, INDEX_FILE)

    with open(DATA_FILE, "w") as f:
        json.dump(memory_store, f, indent=2)  # 👈 readable


async def get_relevant_facts(session_id: str, query: str, k: int = 3):
    """
    Retrieve the top-k semantically relevant memories for a query.

    We also de-duplicate results by text so the same memory does not show
    up multiple times in the system prompt.
    """
    if index.ntotal == 0:
        return ""

    query_embedding = embedder.encode([query])
    _, indices = index.search(
        np.array(query_embedding).astype("float32"), min(k, index.ntotal)
    )

    seen_texts = set()
    results = []
    for idx in indices[0]:
        if idx < len(memory_store):
            item = memory_store[idx]
            text = item.get("text") or ""
            if not text or text in seen_texts:
                continue

            seen_texts.add(text)
            results.append(f"[{item.get('category', 'GENERAL').upper()}] {text}")

    return "\n".join(results)

def clear_memory():
    """
    Clears all stored long-term memory.
    Used for benchmarking and testing.
    """
    global index, memory_store

    # Reset FAISS index
    index.reset()

    # Clear in-memory store
    memory_store.clear()

    # Remove persisted files if they exist
    if os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)

    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
