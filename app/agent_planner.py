# app/agent_planner.py

def planner_prompt(user_message: str) -> str:
    return f"""
You are a planning assistant.
Give short bullet-point steps only.
No emotional language.
No repetition.

User message:
{user_message}
"""
