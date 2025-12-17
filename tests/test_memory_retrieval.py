import asyncio
from app.memory import save_memory, get_relevant_facts

def test_memory_retrieval():
    """Test that stored memories can be retrieved via semantic search."""
    # Store a memory
    save_memory("user prefers vegetarian food", category="preference")
    
    # Retrieve relevant memories
    async def check_retrieval():
        results = await get_relevant_facts("web-session", "food preference", k=3)
        assert results != "", "Memory retrieval should return results"
        assert "vegetarian" in results.lower(), "Retrieved memory should contain stored information"
        return results
    
    results = asyncio.run(check_retrieval())
    assert len(results) > 0, "Memory retrieval should not be empty"
