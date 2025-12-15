from autogen import ConversableAgent

def create_carebot(llm_config):
    return ConversableAgent(
        name="CareBot",
        system_message="You are an empathetic mental health assistant.",
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=lambda x: True
    )
