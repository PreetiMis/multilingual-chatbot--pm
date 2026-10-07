# 💬 Multilingual AI Chatbot with Memory

A chatbot that talks in **English, Hindi and Marathi**, remembers your conversation, and streams replies word by word. Built with Python, Streamlit and Google's Gemini API.

**🔗 Live demo:** [add your Streamlit Cloud link here]

![Demo](demo.gif)
<!-- Record a short GIF of the app and save it as demo.gif in this folder -->

## ✨ Features

- **Multilingual:** auto-detects your language, or forces replies in English, हिन्दी or मराठी (also understands Hinglish)
- **Conversation memory:** remembers the last 20 messages, so it knows your name and earlier questions
- **Streaming replies:** text appears word by word, like ChatGPT
- **Creativity control:** a temperature slider from factual to creative
- **Download chat:** save the conversation as JSON
- **Tested:** unit tests with pytest, no API calls needed

## 🏗️ How it works

```
User types a message
      │
      ▼
app.py (Streamlit UI) ── stores chat in session_state
      │
      ▼
chatbot.py ── adds system prompt (language rules)
          ── trims history to the last 20 messages
          ── converts to Gemini format
      │
      ▼
Gemini API (gemini-2.5-flash) ── streams the reply back
```

**Why memory needs code:** LLMs do not remember anything between requests. To give the bot "memory", the app sends the recent conversation with every new message. Trimming old messages keeps requests fast and cheap.

## 🚀 Run it locally

1. **Clone and enter the project**
   ```bash
   git clone https://github.com/<your-username>/multilingual-chatbot.git
   cd multilingual-chatbot
   ```
2. **Create a virtual environment and install packages**
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   # source venv/bin/activate   # Mac / Linux
   pip install -r requirements.txt
   ```
3. **Add your free API key** from [Google AI Studio](https://aistudio.google.com/apikey)
   ```bash
   copy .env.example .env       # Windows  (Mac/Linux: cp .env.example .env)
   ```
   Then open `.env` and paste your key.
4. **Run**
   ```bash
   streamlit run app.py
   ```
5. **Test**
   ```bash
   pytest -v
   ```

## 📁 Project structure

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit web interface |
| `chatbot.py` | Gemini API logic: system prompt, memory, streaming |
| `test_chatbot.py` | Unit tests |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for your API key |

## 🛠️ Tech stack

Python · Google Gemini API (`google-genai`) · Streamlit · pytest · python-dotenv

## 🔮 Future improvements

- Voice input and output (speech-to-text in Hindi/Marathi)
- Save chats to a database (SQLite) so they survive a page refresh
- Summarize old messages instead of dropping them, for longer memory
- Add Claude / OpenAI as switchable model options

## 👩‍💻 Author

**[Your Name]** · [LinkedIn](https://linkedin.com/in/yourname) · [GitHub](https://github.com/yourname)
