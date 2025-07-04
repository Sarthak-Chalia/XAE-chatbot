import streamlit as st
import os
import time
import base64
from langchain_together import ChatTogether
from langchain.schema import HumanMessage

# Set API Key
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY_HERE"  # Replace with your real key

# Initialize model
llm = ChatTogether(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    temperature=0.7
)

# Get response from model
def get_response(question: str):
    messages = [HumanMessage(content=question)]
    response = llm(messages)
    return response.content

# Page settings
st.set_page_config(page_title="Xae Chat 💬", page_icon="🤖", layout="centered")

# Optional: Uploadable background
uploaded_bg = st.file_uploader("Upload custom background", type=["jpg", "jpeg", "png"])
if uploaded_bg:
    bg_bytes = uploaded_bg.getvalue()
    encoded = base64.b64encode(bg_bytes).decode()
    st.markdown(f"""
    <style>
        html, body, [class*="css"] {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
    </style>
    """, unsafe_allow_html=True)

# Custom CSS (Times New Roman + colors intact)
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Times New Roman', Times, serif;
            color: #1a1a1a;
        }

        .main-title {
            text-align: center;
            font-size: 3em;
            color: #3A3A3A;
            font-weight: bold;
            margin-bottom: 0.5em;
            text-shadow: 1px 1px 2px #ffffff;
        }

        .logo {
            width: 150px;
            display: block;
            margin-left: auto;
            margin-right: auto;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }

        .chat-box {
            background-color: #fafafa;
            border-radius: 10px;
            padding: 1em;
            margin-top: 1em;
            margin-bottom: 1em;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            max-height: 400px;
            overflow-y: auto;
        }

        .user-message {
            background-color: #D1E8FF;
            color: #0D47A1;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 0.5em;
        }

        .bot-message {
            background-color: #F3E5F5;
            color: #4A148C;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 1em;
        }

        .clear-button {
            background-color: #e53935;
            color: white;
            border-radius: 8px;
            padding: 0.5em 1em;
            font-size: 1em;
            margin-top: 10px;
        }

        .clear-button:hover {
            background-color: #c62828;
        }
    </style>
""", unsafe_allow_html=True)

# Logo and title
st.markdown('<img src="https://i.pinimg.com/736x/b3/7d/a5/b37da5a54f093a8f0b581ca9f10765a7.jpg" class="logo" />', unsafe_allow_html=True)
st.markdown('<div class="main-title">Xae Chatbot 🤖✨</div>', unsafe_allow_html=True)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Chat History Box ---
with st.container():
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)
    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f'<div class="user-message"><b>You:</b> {msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message"><b>Xae:</b> {msg}</div>', unsafe_allow_html=True)
    typing_placeholder = st.empty()
    st.markdown('</div>', unsafe_allow_html=True)

# --- Input Box (at bottom always) ---
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input("Your message", placeholder="Type your question here...", key="chat_input", label_visibility="collapsed")
with col2:
    ask_button = st.button("🔍", use_container_width=True)

# --- Process New Message ---
if ask_button and user_input.strip():
    with st.spinner("Thinking..."):
        try:
            st.session_state.chat_history.append(("You", user_input))
            answer = get_response(user_input)

            # Typing animation in placeholder
            display = ""
            for char in answer:
                display += char
                typing_placeholder.markdown(f'<div class="bot-message"><b>Xae:</b> {display}</div>', unsafe_allow_html=True)
                time.sleep(0.01)

            st.session_state.chat_history.append(("Xae", answer))
            typing_placeholder.empty()
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# --- Clear Chat ---
if st.button("🧹 Clear Chat", use_container_width=True):
    st.session_state.chat_history = []
    st.experimental_rerun()
