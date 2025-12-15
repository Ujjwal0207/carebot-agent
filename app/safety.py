CRISIS_KEYWORDS = [
    "suicide",
    "kill myself",
    "end my life",
    "hopeless",
    "give up"
]

def safety_check(message: str):
    text = message.lower()
    for word in CRISIS_KEYWORDS:
        if word in text:
            return {
                "safe": False,
                "response": (
                    "I'm really sorry you're feeling this way. "
                    "You are not alone. Please consider reaching out "
                    "to a trusted person or a mental health professional."
                )
            }
    return {"safe": True}
