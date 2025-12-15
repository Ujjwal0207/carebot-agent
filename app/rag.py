from app.memory import get_relevant_facts

async def build_context(session_id: str, user_message: str) -> str:
    facts = await get_relevant_facts(session_id, user_message)

    if facts:
        memory_block = f"""
Relevant past information:
{facts}
"""
    else:
        memory_block = ""

    return f"""
{memory_block}

User message:
{user_message}

---

Instruction:
You are a compassionate, helpful AI assistant.
Use the relevant past information ONLY if it helps.
Do NOT repeat or list the memory.
Respond naturally and empathetically to the user.
Only output your final answer.
"""
