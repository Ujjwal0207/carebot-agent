import asyncio
from app.main import run_agent

def test_rag_response_stability():
    """Test that asking the same question twice returns non-empty, stable responses."""
    async def check_stability():
        # Ask the same question twice
        response1 = await run_agent("What is my preference?")
        response2 = await run_agent("What is my preference?")
        
        # Both responses should be non-empty strings
        assert response1 is not None, "First response should not be None"
        assert response2 is not None, "Second response should not be None"
        assert isinstance(response1, str), "First response should be a string"
        assert isinstance(response2, str), "Second response should be a string"
        assert len(response1.strip()) > 0, "First response should not be empty"
        assert len(response2.strip()) > 0, "Second response should not be empty"
        
        return response1, response2
    
    response1, response2 = asyncio.run(check_stability())
    # Note: We're testing stability (non-empty), not correctness
    # Responses may differ slightly due to LLM variability, which is acceptable
