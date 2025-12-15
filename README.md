# CareBot Agent 🤖

A **multi-agent conversational AI system** with **long-term memory**, **retrieval-augmented generation (RAG)**, and **empathetic reasoning**, built using open-source tools.

This project demonstrates how production-grade AI assistants are designed using **modular agents**, **vector databases**, and **real-time communication**.

---

## ✨ Key Features

- 🧠 **Automatic Long-Term Memory**
  - Important user facts are extracted automatically
  - Stored using FAISS + SentenceTransformers
  - No hard-coded memory rules

- 🤝 **Multi-Agent Architecture**
  - CareBot → empathetic responses
  - PlannerBot → practical action steps
  - MemoryExtractor → decides what to remember

- 🔍 **RAG (Retrieval-Augmented Generation)**
  - Past memories are retrieved based on semantic similarity
  - Only relevant context is injected into prompts

- ⚡ **Real-Time Streaming (WebSockets)**
  - Token-by-token responses (ChatGPT-like UX)

- 🔐 **Safety-Aware Routing**
  - User intent determines which agent responds

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    User --> WebSocket
    WebSocket --> Router
    Router --> CareBot
    Router --> PlannerBot

    CareBot --> MemoryExtractor
    PlannerBot --> MemoryExtractor

    MemoryExtractor --> FAISS[(FAISS Vector DB)]
    FAISS --> RAG
    RAG --> CareBot
