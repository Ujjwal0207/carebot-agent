def route_message(message: str) -> str:
    msg = message.lower()

    # 🚨 SAFETY FIRST
    unsafe_patterns = [
        "kill myself",
        "end my life",
        "suicide",
        "harm myself"
    ]

    if any(p in msg for p in unsafe_patterns):
        return "safety"

    # ❤️ EMOTIONAL SUPPORT
    emotional_patterns = [
        "lost",
        "grief",
        "depressed",
        "sad",
        "anxious",
        "overwhelmed"
    ]

    if any(p in msg for p in emotional_patterns):
        return "care"

    # 🧠 PLANNING / TASKS
    planning_patterns = [
        "what should i do",
        "steps",
        "plan",
        "how can i"
    ]

    if any(p in msg for p in planning_patterns):
        return "planner"

    # 🤖 DEFAULT
    return "care"
