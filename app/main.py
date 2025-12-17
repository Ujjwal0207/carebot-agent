import json
import os
from collections import defaultdict, deque

from app.agent_care import create_carebot
from app.agent_memory_extractor import create_memory_extractor
from app.router import route_message
from app.rag import build_context
from app.memory import save_memory
from config.llm_config import config_list

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# We wrap the raw config_list exactly as AutoGen expects.
llm_config = {"config_list": config_list}

carebot = create_carebot(llm_config)
memory_extractor = create_memory_extractor(llm_config)

# ----------------------------
# 🔧 SHORT-TERM MEMORY
# ----------------------------
CHAT_HISTORY = defaultdict(lambda: deque(maxlen=6))

# 🔧 ANTI-REPETITION CACHE (PER-SESSION)
LAST_RESPONSE_CACHE = {}


def planner_prompt(user_message: str) -> str:
    """
    Helper prompt for the internal planning mode.

    NOTE: This does not call the model directly. It just builds
    structured text that we feed into the main CareBot so the
    final reply stays coherent and empathetic.
    """
    return f"""
You are a planning assistant.
Give short bullet-point steps only.
No emotional language.
No repetition.

User message:
{user_message}
"""


async def run_agent(user_message: str) -> str:
    # For now we treat the browser as a single shared session.
    # If you add authentication later, you can plug in a real user/session id here.
    session_id = "web-session"

    # 1️⃣ ROUTING
    routed = route_message(user_message)

    if routed == "safety":
        return (
            "I'm really glad you shared this. "
            "You don’t have to face this alone.\n\n"
            "If things feel overwhelming, please consider reaching out "
            "to someone you trust or a mental health professional."
        )

    # 2️⃣ SYSTEM CONTEXT (RAG + MEMORY)
    context = await build_context(session_id, user_message)
    system_msg = {"role": "system", "content": context["system"]}

    # =====================================================
    # 👋 GREETING HANDLING (NO EMOTIONAL LOOP)
    # =====================================================
    if routed == "greeting":
        reply = carebot.generate_reply(
            messages=[
                system_msg,
                {
                    "role": "user",
                    "content": (
                        "The user greeted you casually. "
                        "Reply briefly and friendly. "
                        "DO NOT ask emotional questions."
                    )
                }
            ]
        )

        # AutoGen can sometimes return dicts / lists; normalize to a string.
        if isinstance(reply, dict):
            reply = reply.get("content") or json.dumps(reply)
        elif isinstance(reply, list):
            # Join any message-like objects into a readable string.
            reply = " ".join(
                (
                    (m.get("content") if isinstance(m, dict) else str(m))
                    for m in reply
                )
            )

        final_response = str(reply).strip()
        LAST_RESPONSE_CACHE[session_id] = final_response
        return final_response

    # 3️⃣ USER CONTENT
    if routed == "planner":
        plan = planner_prompt(user_message)
        user_content = f"""
User message:
{user_message}

Planner suggestions:
{plan}

Respond empathetically and practically.
"""
    else:
        user_content = user_message

    # 4️⃣ MESSAGE BUILD (WITH CHAT HISTORY)
    messages = [system_msg]
    messages.extend(CHAT_HISTORY[session_id])
    messages.append({"role": "user", "content": user_content})

    # 5️⃣ LLM CALL (AutoGen – correct usage)
    reply = carebot.generate_reply(messages=messages)

    # ---------------------------------------------------------
    # Robust normalization: AutoGen may return a string, dict,
    # or list of message-like objects depending on config.
    # We always convert it into a clean string here so the rest
    # of the pipeline (memory + streaming) can rely on it.
    # ---------------------------------------------------------
    if isinstance(reply, dict):
        reply = reply.get("content") or json.dumps(reply)
    elif isinstance(reply, list):
        reply = " ".join(
            (
                (m.get("content") if isinstance(m, dict) else str(m))
                for m in reply
            )
        )

    if not reply or not isinstance(reply, str):
        reply = (
            "I’m here with you. "
            "Can you tell me a bit more about what’s been on your mind?"
        )

    final_response = reply.strip()

    # =====================================================
    # 🔁 ANTI-REPETITION FIX (CRITICAL)
    # =====================================================
    last = LAST_RESPONSE_CACHE.get(session_id)
    if last and final_response.lower() == last.lower():
        final_response = (
            "Thanks for sharing that. "
            "What part of this feels hardest for you right now?"
        )

    LAST_RESPONSE_CACHE[session_id] = final_response

    # 6️⃣ UPDATE SHORT-TERM MEMORY
    CHAT_HISTORY[session_id].append({"role": "user", "content": user_message})
    CHAT_HISTORY[session_id].append(
        {"role": "assistant", "content": final_response}
    )

    # 7️⃣ LONG-TERM MEMORY EXTRACTION (SAFE)
    try:
        memory_reply = memory_extractor.generate_reply(
            messages=[
                {
                    "role": "user",
                    "content": f"""
Conversation:
User: {user_message}
Assistant: {final_response}
"""
                }
            ]
        )

        if memory_reply:
            parsed = json.loads(memory_reply)
            if parsed.get("save"):
                save_memory(
                    parsed["summary"],
                    parsed.get("category", "general")
                )
    except Exception:
        pass

    return final_response
