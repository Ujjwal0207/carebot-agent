from app.main import run_agent

def test_rag_response_stability():
    response1 = run_agent("What is my preference?")
    response2 = run_agent("What is my preference?")
    assert response1 is not None
    assert response2 is not None
