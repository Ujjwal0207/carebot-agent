def route_message(message: str):
    if "plan" in message.lower() or "what should i do" in message.lower():
        return "planner"
    return "care"
