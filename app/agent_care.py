from autogen import ConversableAgent


def create_carebot(llm_config):
    """
    Factory for the main CareBot agent.

    Changes made:
    - Slightly richer system instructions for more grounded, varied answers.
    - We still keep the same API so the rest of the project does not break.
    """
    return ConversableAgent(
        name="CareBot",
        system_message=(
            "You are an empathetic, grounded mental health assistant. "
            "Respond in a warm, natural tone and keep answers concise but meaningful. "
            "Offer specific, practical suggestions when helpful (e.g., small steps, questions). "
            "Avoid repeating the same sentence verbatim across turns and do not give medical diagnoses."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=lambda _: False,
    )
