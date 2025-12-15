# 🧠 CareBot Agent  
### Multi-Agent AI Assistant using AutoGen + Ollama + FastAPI

🔗 **Repository:** https://github.com/Ujjwal0207/carebot-agent

CareBot Agent is a **production-style, multi-agent conversational AI system** built using **Microsoft AutoGen**, **FastAPI**, **WebSockets**, and **local LLMs via Ollama**.

This project demonstrates how real-world AI assistants are designed using **agent orchestration**, **intent routing**, **memory extraction**, and **safe LLM integration** — without relying on paid APIs.

---

## 🚀 What Is This Project?

CareBot is an **empathetic AI assistant** that can:

- Understand user intent (greeting, emotional support, planning, safety)
- Route messages intelligently
- Respond empathetically using a Care agent
- Generate structured guidance using planner logic
- Extract long-term memory automatically
- Run completely **locally** using Ollama
- Communicate in **real time** using WebSockets

This is **not a simple chatbot** — it is a **multi-agent AI system** designed with production constraints in mind.

---

## 🏗️ High-Level Architecture

User (Browser UI)
        |
        | WebSocket
        v
FastAPI Server (web/server.py)
        |
        v
run_agent()  ──► Router
        |           |
        |           ├── Safety Handling
        |           ├── Care Mode
        |           └── Planner Mode
        |
        v
RAG Context Builder (rag.py)
        |
        v
CareBot Agent (AutoGen + Ollama)
        |
        v
Memory Extractor Agent
        |
        v
Response → WebSocket → UI



## 🤖 Agents in This System

### 1️⃣ CareBot Agent
- Built with `ConversableAgent`
- Provides empathetic, human-like responses
- Uses system prompts to guide tone and behavior

### 2️⃣ Memory Extractor Agent
- Automatically decides **what is worth remembering**
- Outputs structured JSON
- Stores long-term memory safely

> ⚠️ AutoGen is used **correctly**:  
> `generate_reply()` is used for LLM calls (not agent-to-agent chat with Ollama).

---

## 🔀 Intent Routing

Messages are routed before LLM invocation:

| Intent | Example |
|------|--------|
| `safety` | “I want to harm myself” |
| `care` | “I feel lost and overwhelmed” |
| `planner` | “What should I do next?” |
| `greeting` | “Hi”, “Hello” |

This keeps responses safe, relevant, and predictable.

---

## 📚 RAG (Retrieval-Augmented Generation)

- Past memory is retrieved when relevant
- Injected only into **system context**
- Prevents prompt leakage
- Reduces hallucinations
- Improves conversational continuity

---

## ⚡ Real-Time WebSocket UI

- Instant responses
- “🤖 Thinking…” indicator
- No page reloads
- Ready for token streaming upgrades

---

## 🛠 Tech Stack

| Layer | Technology |
|----|-----------|
Backend | FastAPI |
Real-time | WebSockets |
Agents | Microsoft AutoGen |
LLM | Ollama (Llama3) |
Language | Python 3.9+ |
Frontend | HTML + JavaScript |
Memory | JSON (extensible to FAISS) |

---

## 📂 Project Structure

carebot-agent/
│
├── app/
│   ├── main.py                  # Core orchestration
│   ├── router.py                # Intent routing
│   ├── rag.py                   # Context builder
│   ├── memory.py                # Memory storage
│   ├── agent_care.py
│   ├── agent_memory_extractor.py
│   ├── safety.py
│   └── tools.py
│
├── web/
│   ├── server.py                # FastAPI + WebSocket
│   └── index.html               # UI
│
├── config/
│   └── llm_config.py            # Ollama config
│
├── memory.json
├── requirements.txt
└── README.md


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Ujjwal0207/carebot-agent.git
cd carebot-agent

2️⃣ Create Virtual Environment
python3 -m venv .venv
source .venv/bin/activate     # macOS/Linux
.venv\Scripts\activate        # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

🧠 Install Ollama (Local LLM)

Download Ollama:
👉 https://ollama.com

Pull a model:

ollama pull llama3


Keep Ollama running in the background.

⚙️ LLM Configuration

config/llm_config.py

config_list = [
    {
        "model": "llama3",
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama"
    }
]

▶️ Run the Application
uvicorn web.server:app --reload


Open in browser:
http://127.0.0.1:8000