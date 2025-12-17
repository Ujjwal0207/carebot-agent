from app.memory import store_memory, retrieve_memory

def test_memory_retrieval():
    store_memory("user prefers vegetarian food")
    results = retrieve_memory("food preference")
    assert len(results) > 0
