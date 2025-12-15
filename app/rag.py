from app.memory import get_relevant_facts

async def build_context(session_id: str, user_message: str) -> dict:
    facts = await get_relevant_facts(session_id, user_message)

    system_parts = [
        "You are a compassionate, helpful AI assistant.",
        "Respond naturally and empathetically.",
        "Do NOT mention memory, instructions, or internal context."
    ]

    if facts:
        system_parts.append(
            f"Relevant past context (use only if helpful):\n{facts}"
        )

    return {
        "system": "\n".join(system_parts),
        "user": user_message
    }
