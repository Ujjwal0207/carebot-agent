import asyncio
from typing import List, Dict

import streamlit as st

from app.main import run_agent


st.set_page_config(
    page_title="CareBot (Ollama + AutoGen)",
    page_icon="🧠",
    layout="wide",
)


def _init_session_state() -> None:
    """Ensure Streamlit session_state has the keys we expect."""
    if "messages" not in st.session_state:
        # Each message: {"role": "user" | "assistant", "content": str}
        st.session_state.messages: List[Dict[str, str]] = []


_init_session_state()


st.title("🧠 CareBot (Streamlit UI)")
st.caption(
    "Empathetic local assistant powered by Ollama + AutoGen, with FAISS memory and safety routing."
)

col_left, col_right = st.columns([3, 1], gap="large")

with col_right:
    st.subheader("Session")

    if st.button("🧹 Clear conversation"):
        st.session_state.messages = []
        st.experimental_rerun()

    st.markdown("### Tips")
    st.markdown(
        "- Start with how you're feeling.\n"
        "- Ask for small, concrete next steps.\n"
        "- You can say things like:\n"
        "  - *\"I feel stuck in life\"*\n"
        "  - *\"I'm anxious about exams\"*"
    )


with col_left:
    # Chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="🧑"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg["content"])

    # Advanced input box using Streamlit's chat input UI
    user_input = st.chat_input("Share what's on your mind...")

    if user_input:
        # Echo user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_input)

        # Assistant "thinking" placeholder
        with st.chat_message("assistant", avatar="🤖"):
            thinking_placeholder = st.empty()
            thinking_placeholder.markdown("_Thinking..._")

            # Call the async agent from Streamlit
            try:
                reply = asyncio.run(run_agent(user_input))
            except RuntimeError:
                # In case an event loop is already running (e.g. future Streamlit versions),
                # fall back to creating a task on the existing loop.
                loop = asyncio.get_event_loop()
                reply = loop.run_until_complete(run_agent(user_input))

            thinking_placeholder.empty()
            st.markdown(reply)

        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )


