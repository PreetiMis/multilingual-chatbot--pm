"""
app.py - the web page, built with Streamlit.

Run it with:   streamlit run app.py

Streamlit re-runs this whole file from top to bottom every time you click
or type something. That is why we store the chat in `st.session_state`:
it is the one place that survives between re-runs.
"""

import json
import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from chatbot import LANGUAGES, MAX_HISTORY_MESSAGES, Chatbot

# Load GEMINI_API_KEY from the .env file (never write keys directly in code).
load_dotenv()

st.set_page_config(page_title="Multilingual AI Chatbot", page_icon="💬")


def get_api_key() -> str | None:
    """Look for the key in .env first, then in Streamlit Cloud secrets."""
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None


# ---------- Sidebar: settings ----------
with st.sidebar:
    st.header("⚙️ Settings")
    language_label = st.selectbox("Reply language", list(LANGUAGES.keys()))
    temperature = st.slider(
        "Creativity (temperature)", 0.0, 1.0, 0.7, 0.1,
        help="Low = focused and factual. High = more creative and varied.",
    )
    st.caption(f"🧠 Remembers the last {MAX_HISTORY_MESSAGES} messages")

    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.get("messages"):
        st.download_button(
            "💾 Download chat",
            data=json.dumps(st.session_state.messages, ensure_ascii=False, indent=2),
            file_name=f"chat_{datetime.now():%Y%m%d_%H%M}.json",
            mime="application/json",
            use_container_width=True,
        )

# ---------- Main page ----------
st.title("💬 Multilingual AI Chatbot")
st.caption("Chat in English, हिन्दी or मराठी. I remember our conversation.")

api_key = get_api_key()
if not api_key:
    st.error("No API key found. Add GEMINI_API_KEY to your .env file (see README).")
    st.stop()

# Create the chat history once per browser session.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show all previous messages.
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Wait for new input.
if user_input := st.chat_input("Type your message... / अपना संदेश लिखें..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            bot = Chatbot(api_key)
            reply = st.write_stream(
                bot.stream_reply(
                    st.session_state.messages,
                    language=LANGUAGES[language_label],
                    temperature=temperature,
                )
            )
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as error:
            # Remove the unanswered message so the user can try again.
            st.session_state.messages.pop()
            st.error(f"Something went wrong: {error}")
