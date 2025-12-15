from autogen import ConversableAgent

def create_plannerbot(llm_config):
    return ConversableAgent(
        name="PlannerBot",
        system_message="You suggest small, practical steps to help the user.",
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=lambda x: True
    )
