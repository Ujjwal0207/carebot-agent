import json
import os

from app.agent_care import create_carebot
from app.agent_memory_extractor import create_memory_extractor
from app.router import route_message
from app.rag import build_context
from app.memory import save_memory
from config.llm_config import config_list

os.environ["TOKENIZERS_PARALLELISM"] = "false"

llm_config = {"config_list": config_list}

carebot = create_carebot(llm_config)
memory_extractor = create_memory_extractor(llm_config)


def planner_prompt(user_message: str) -> str:
    return f"""
You are a planning assistant.
Output short bullet-point steps only.
No emotional language.
No repetition.

User message:
{user_message}
"""


async def run_agent(user_message: str) -> str:
    session_id = "web-session"

    routed = route_message(user_message)

    if routed == "safety":
        return (
            "I'm really glad you shared this. "
            "You don’t have to face this alone."
        )

    # ✅ FIX 1: await build_context
    context = await build_context(session_id, user_message)
    system_msg = {"role": "system", "content": context["system"]}

    user_content = user_message
    if routed == "planner":
        plan = planner_prompt(user_message)
        user_content = f"""
User message:
{user_message}

Planner suggestions:
{plan}

Respond empathetically and practically.
"""

    # ✅ FIX 2: generate_reply WITHOUT await
    reply = carebot.generate_reply(
        messages=[
            system_msg,
            {"role": "user", "content": user_content}
        ]
    )

    # ✅ FIX 3: handle None safely (CRITICAL)
    if not reply:
        reply = (
            "I’m here with you. "
            "Can you tell me a bit more about what you’re experiencing?"
        )

    final_response = reply.strip()

    # ✅ Memory extraction (safe)
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
