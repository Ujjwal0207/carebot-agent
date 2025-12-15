from autogen import ConversableAgent

def create_carebot(llm_config):
    return ConversableAgent(
        name="CareBot",
        system_message=(
            "You are an empathetic mental health assistant. "
            "Respond warmly, naturally, and helpfully. "
            "Do not repeat the same sentence verbatim."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=lambda _: False
    )
