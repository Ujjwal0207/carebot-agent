from autogen import ConversableAgent

def create_memorybot(llm_config):
    return ConversableAgent(
        name="MemoryBot",
        system_message="Summarize important user facts.",
        llm_config=llm_config,
        human_input_mode="NEVER"
    )
