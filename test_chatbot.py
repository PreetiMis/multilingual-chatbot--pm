"""
Tests for chatbot.py. They do NOT call the real API, so they are free and fast.

Run with:   pytest -v
"""

from chatbot import build_system_prompt, to_gemini_format, trim_history


def test_system_prompt_forces_chosen_language():
    prompt = build_system_prompt("Marathi")
    assert "Always reply in Marathi" in prompt


def test_system_prompt_auto_detect_mentions_same_language():
    prompt = build_system_prompt(None)
    assert "same language the user writes in" in prompt


def test_trim_history_keeps_latest_messages():
    messages = [{"role": "user", "content": str(i)} for i in range(30)]
    trimmed = trim_history(messages, max_messages=5)
    assert len(trimmed) == 5
    assert trimmed[-1]["content"] == "29"


def test_trim_history_short_list_unchanged():
    messages = [{"role": "user", "content": "hi"}]
    assert trim_history(messages) == messages


def test_assistant_role_becomes_model():
    messages = [
        {"role": "user", "content": "Mera naam Preeti hai"},
        {"role": "assistant", "content": "Namaste Preeti!"},
    ]
    contents = to_gemini_format(messages)
    assert [c.role for c in contents] == ["user", "model"]
    assert contents[1].parts[0].text == "Namaste Preeti!"
