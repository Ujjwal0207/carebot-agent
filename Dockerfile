FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8000

# For Docker talking to Ollama on your host (macOS/Windows)
ENV OLLAMA_BASE_URL=http://host.docker.internal:11434

CMD ["uvicorn", "web.server:app", "--host", "0.0.0.0", "--port", "8000"]