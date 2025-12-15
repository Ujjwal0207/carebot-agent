import asyncio
import uuid
import os

from app.agent_care import create_carebot
from app.agent_planner import create_plannerbot
from app.router import route_message
from app.rag import build_context
from app.memory import save_memory
from config.llm_config import config_list

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# ----------------------------
# Create agents ONCE (IMPORTANT)
# ----------------------------
llm_config = {"config_list": config_list}

carebot = create_carebot(llm_config)
plannerbot = create_plannerbot(llm_config)


# ----------------------------
# Helper: extract text from ChatResult
# ----------------------------
def extract_text(chat_result) -> str:
    if hasattr(chat_result, "chat_history") and chat_result.chat_history:
        return chat_result.chat_history[-1]["content"]
    return "No response generated."


# ----------------------------
# This is what FastAPI calls
# ----------------------------
async def run_agent(user_message: str) -> str:
    session_id = "web-session"

    # Save memory (FAISS)
    save_memory(
        "User lost their mother and feels emotionally lost",
        category="emotional"
    )

    # Build RAG context
    context = await build_context(session_id, user_message)

    # Route message
    routed = route_message(user_message)

    final_prompt = context

    message = {
        "role": "user",
        "content": final_prompt
    }

    # Correct Autogen chat usage
    if routed == "planner":
        chat_result = await plannerbot.a_initiate_chat(
            carebot,
            message=message,
            max_turns=1
        )
    else:
        chat_result = await carebot.a_initiate_chat(
            plannerbot,
            message=message,
            max_turns=1
        )

    # 🔥 RETURN ONLY TEXT (THIS FIXES YOUR UI)
    return extract_text(chat_result)


# ----------------------------
# CLI test (optional)
# ----------------------------
async def main():
    reply = await run_agent(
        "I still feel lost after my mother's death. What should I do?"
    )
    print("\nAGENT RESPONSE:\n")
    print(reply)


if __name__ == "__main__":
    asyncio.run(main())
