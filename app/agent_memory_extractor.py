from autogen import ConversableAgent

def create_memory_extractor(llm_config):
    return ConversableAgent(
        name="MemoryExtractor",
        system_message=(
            "Extract long-term user facts.\n"
            "Respond ONLY in valid JSON."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=lambda _: True
    )
