config_list = [
    {
        "model": "llama3",
        "api_type": "ollama",
        "base_url": "http://localhost:11434",
        # Slight temperature > 0 for more varied, less robotic replies.
        # Ollama's OpenAI-compatible API forwards this to the model.
        "temperature": 0.7,
    }
]
