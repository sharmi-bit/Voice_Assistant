
import io
import os
import re

import groq
import streamlit as st
from dotenv import load_dotenv
from gtts import gTTS

# ---------- 1. Load settings from the .env file ----------
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_STT_MODEL = os.getenv("GROQ_STT_MODEL", "whisper-large-v3-turbo")
TTS_LANGUAGE = os.getenv("TTS_LANGUAGE", "en")

SYSTEM_PROMPT = (
    "You are a helpful AI assistant. Answer clearly in short, conversational "
    "sentences. Do not use markdown, lists or emojis, because answers are read aloud."
)
NO_TRANSCRIPT_NOTE = (
    "I couldn't understand that voice message. Please record it again "
    "or type your message instead."
)

client = groq.Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
USER_AVATAR = "🧑"
ASSISTANT_AVATAR = "🤖"


def chat_box(role):
    """Zigzag layout: user messages sit on the LEFT, assistant replies on the RIGHT."""
    if role == "user":
        left, _ = st.columns([4, 1])
        return left.chat_message("user", avatar=USER_AVATAR)
    _, right = st.columns([1, 4])
    return right.chat_message("assistant", avatar=ASSISTANT_AVATAR)


# ---------- 2. Ask the AI (Groq) ----------
def ask_ai(history):
    """Send the conversation to Groq and return the reply text."""
    if client is None:
        return "GROQ_API_KEY is missing. Add it to .env and restart the app."

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    usable = [m for m in history if not m.get("skip")]
    messages += [{"role": m["role"], "content": m["content"]} for m in usable[-20:]]

    try:
        response = client.chat.completions.create(model=GROQ_MODEL, messages=messages)
        return response.choices[0].message.content.strip()
    except groq.AuthenticationError:
        return "Your Groq API key is not valid. Check GROQ_API_KEY."
    except groq.RateLimitError:
        return "Groq's rate limit was reached. Please wait a moment and try again."
    except groq.APIConnectionError:
        return "I can't reach Groq. Please check your internet connection."
    except Exception as error:
        return f"Groq returned an error: {error}"


# ---------- 3. Text-to-speech with gTTS ----------
def text_to_speech(text):
    """Turn text into MP3 audio bytes. Returns None if it fails (e.g. no internet)."""
    clean = re.sub(r"[*_#`>~]", "", text)
    try:
        buffer = io.BytesIO()
        gTTS(text=clean, lang=TTS_LANGUAGE).write_to_fp(buffer)
        return buffer.getvalue()
    except Exception:
        return None


# ---------- 4. Speech-to-text with Groq Whisper ----------
def transcribe(audio_bytes):
    """Convert recorded audio to text. Returns None if it fails."""
    if client is None:
        return None
    try:
        result = client.audio.transcriptions.create(
            file=("voice.wav", audio_bytes), model=GROQ_STT_MODEL)
        return result.text.strip()
    except Exception:
        return None


# ---------- 5. Handle one message (typed or voice) ----------
def handle_message(text, user_audio=None):
    with chat_box("user"):
        if user_audio:
            st.audio(user_audio, format="audio/wav")
        if text:
            st.write(text)
    st.session_state.messages.append({
        "role": "user", "content": text or "(voice message)",
        "audio": user_audio, "skip": not text,
    })
    audio = None
    with chat_box("assistant"):
        if text:
            with st.spinner("Thinking..."):
                reply = ask_ai(st.session_state.messages)
        else:
            reply = NO_TRANSCRIPT_NOTE
        st.write(reply)

        if speak_replies:
            with st.spinner("Preparing voice..."):
                audio = text_to_speech(reply)
            if not audio:
                st.caption("Voice output needs an internet connection (gTTS).")

    st.session_state.messages.append({
        "role": "assistant", "content": reply, "audio": audio, "skip": not text,
    })
    if audio:
        st.session_state.autoplay_index = len(st.session_state.messages) - 1
    st.rerun()


# ---------- 6. The page ----------
st.title("AI Assistant")
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mic_key" not in st.session_state:
    st.session_state.mic_key = 0          
if "autoplay_index" not in st.session_state:
    st.session_state.autoplay_index = None

speak_replies = st.checkbox("Read replies aloud", value=True)
if st.button("Clear conversation"):
    st.session_state.messages = []
    st.rerun()

# Show earlier messages
for i, message in enumerate(st.session_state.messages):
    with chat_box(message["role"]):
        if message["role"] == "user":
            if message.get("audio"):
                st.audio(message["audio"], format="audio/wav")
            if not message.get("skip"):
                st.write(message["content"])
        else:
            st.write(message["content"])
            if message.get("audio"):
                st.audio(message["audio"], format="audio/mp3",
                         autoplay=(i == st.session_state.autoplay_index))
st.session_state.autoplay_index = None    
typed = st.chat_input("Type your message...")
recording = st.audio_input("Record a voice message",
                           key=f"mic_{st.session_state.mic_key}")
if recording:
    st.caption("Press play on the recorder to listen. Happy with it? Press Send. "
               "Not happy? Record again.")
    if st.button("Send voice message"):
        audio_bytes = recording.getvalue()
        st.session_state.mic_key += 1   
        with st.spinner("Listening to your message..."):
            transcript = transcribe(audio_bytes)
        handle_message(transcript, audio_bytes)

if typed:
    handle_message(typed)
