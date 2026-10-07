"""
chatbot.py - the "brain" of the app.

This file talks to the Gemini API. It knows nothing about the web page,
so you can test it on its own (see test_chatbot.py).

Key ideas you will learn here:
1. System prompt   - instructions that shape how the AI behaves.
2. Memory          - we send previous messages with every request,
                     because the AI itself does not remember anything.
3. Streaming       - we show the reply word by word, like ChatGPT.
"""

from google import genai
from google.genai import types

# The model we use. "flash" models are fast and have a free tier.
MODEL_NAME = "gemini-3.8-flash"

# How many past messages to remember. More memory = better context,
# but also more tokens (slower and more expensive).
MAX_HISTORY_MESSAGES = 20

LANGUAGES = {
    "Auto-detect": None,
    "English": "English",
    "हिन्दी (Hindi)": "Hindi",
    "मराठी (Marathi)": "Marathi",
}


def build_system_prompt(language: str | None) -> str:
    """Create the instructions the AI follows for the whole conversation."""
    prompt = (
        "You are a friendly, helpful assistant. "
        "Give clear, accurate and concise answers. "
        "If you are not sure about something, say so honestly. "
        "Remember details the user shares earlier in the conversation "
        "(like their name) and use them naturally."
    )
    if language:
        prompt += (
            f" Always reply in {language}, even if the user writes in another "
            f"language. Use simple, everyday {language}."
        )
    else:
        prompt += (
            " Reply in the same language the user writes in. "
            "You understand English, Hindi, Marathi and Hinglish "
            "(Hindi written in English letters)."
        )
    return prompt


def trim_history(messages: list[dict], max_messages: int = MAX_HISTORY_MESSAGES) -> list[dict]:
    """Keep only the most recent messages so the request does not get too big."""
    return messages[-max_messages:]


def to_gemini_format(messages: list[dict]) -> list[types.Content]:
    """
    Convert our simple message list into the format Gemini expects.

    Our format:    {"role": "user" or "assistant", "content": "text"}
    Gemini format: role is "user" or "model", text goes inside "parts".
    """
    contents = []
    for msg in messages:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))
    return contents


class Chatbot:
    def __init__(self, api_key: str, model: str = MODEL_NAME):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def stream_reply(self, messages: list[dict], language: str | None = None, temperature: float = 0.7):
        """
        Send the conversation to Gemini and yield the reply piece by piece.

        `messages` must already include the user's newest message at the end.
        """
        recent = trim_history(messages)
        config = types.GenerateContentConfig(
            system_instruction=build_system_prompt(language),
            temperature=temperature,
        )
        stream = self.client.models.generate_content_stream(
            model=self.model,
            contents=to_gemini_format(recent),
            config=config,
        )
        for chunk in stream:
            if chunk.text:
                yield chunk.text
