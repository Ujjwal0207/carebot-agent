def route_message(message: str) -> str:
    msg = message.lower().strip()

    # 🚨 SAFETY
    unsafe_patterns = [
        "kill myself",
        "end my life",
        "suicide",
        "harm myself"
    ]
    if any(p in msg for p in unsafe_patterns):
        return "safety"

    # 👋 GREETING (IMPORTANT FIX)
    greetings = ["hi", "hello", "hey", "hii"]
    if msg in greetings:
        return "greeting"

    # 🧠 PLANNING
    planning_patterns = [
        "what should i do",
        "steps",
        "plan",
        "how can i"
    ]
    if any(p in msg for p in planning_patterns):
        return "planner"

    # ❤️ EMOTIONAL
    emotional_patterns = [
        "lost",
        "grief",
        "depressed",
        "sad",
        "anxious",
        "overwhelmed",
        "stuck",
        "lonely"
    ]
    if any(p in msg for p in emotional_patterns):
        return "care"

    # 🤖 DEFAULT
    return "care"
