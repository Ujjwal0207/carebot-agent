import faiss
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

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
        memory_store = json.load(f)
else:
    memory_store = []


def save_memory(text: str, category: str = "general"):
    embedding = embedder.encode([text])
    index.add(np.array(embedding).astype("float32"))

    memory_store.append({
        "text": text,
        "category": category
    })

    faiss.write_index(index, INDEX_FILE)
    with open(DATA_FILE, "w") as f:
        json.dump(memory_store, f)


async def get_relevant_facts(session_id: str, query: str, k: int = 3):
    if index.ntotal == 0:
        return ""

    query_embedding = embedder.encode([query])
    distances, indices = index.search(
        np.array(query_embedding).astype("float32"), k
    )

    results = []
    for idx in indices[0]:
        if idx < len(memory_store):
            item = memory_store[idx]
            results.append(f"[{item['category'].upper()}] {item['text']}")

    return "\n".join(results)
