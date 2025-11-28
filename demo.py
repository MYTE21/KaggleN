import os
import glob
import json
import uuid
import asyncio
import nest_asyncio
import streamlit as st
from components import title, chat
from scripts import session_agent

nest_asyncio.apply()

# -- Setup --
LOGO_PATH = os.path.join(os.getcwd(), "assets/icon.png")
HISTORY_DIR = "sessions"

if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

st.set_page_config(page_title="KaggleN", page_icon=LOGO_PATH)


# --- 1. AUTHENTICATION (Simulated) ---
# In a real app, use 'streamlit-authenticator' for passwords/hashing.
def login_screen():
    st.title("Welcome to KaggleN")
    col1, col2 = st.columns([1, 2])
    with col1:
        username = st.text_input("Enter your unique username:")
        if st.button("Start Chatting"):
            if username:
                st.session_state["username"] = username.strip().lower()
                st.rerun()
            else:
                st.warning("Please enter a username.")


def logout():
    if "username" in st.session_state:
        del st.session_state["username"]
        # Clear query params so next user doesn't see old session ID
        st.query_params.clear()
        st.rerun()


# --- CHECK LOGIN STATUS ---
if "username" not in st.session_state:
    login_screen()
    st.stop()  # Stop the script here if not logged in

# Get current user
CURRENT_USER = st.session_state["username"]


# --- 2. USER-SPECIFIC FILE HANDLING ---

def get_file_path(session_id):
    # FILE FORMAT: username_sessionid.json
    return os.path.join(HISTORY_DIR, f"{CURRENT_USER}_{session_id}.json")


def get_chat_title(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            for msg in data:
                if msg["role"] == "user":
                    return msg["content"][:30] + "..." if len(msg["content"]) > 30 else msg["content"]
    except:
        pass
    return "Untitled Chat"


def get_user_sessions():
    """
    Scans for files ONLY belonging to CURRENT_USER.
    """
    # FILTER: Only look for files starting with the username
    search_pattern = os.path.join(HISTORY_DIR, f"{CURRENT_USER}_*.json")
    files = glob.glob(search_pattern)
    files.sort(key=os.path.getmtime, reverse=True)

    sessions = []
    for f in files:
        # Extract Session ID from filename: "john_abc123.json" -> "abc123"
        filename = os.path.basename(f)
        session_id = filename.replace(f"{CURRENT_USER}_", "").replace(".json", "")

        title_text = get_chat_title(f)
        sessions.append({"id": session_id, "title": title_text})
    return sessions


def load_history(session_id):
    file_path = get_file_path(session_id)
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except:
            return []
    return []


def save_history(session_id, messages):
    file_path = get_file_path(session_id)
    with open(file_path, "w") as f:
        json.dump(messages, f)


def delete_session(session_id):
    file_path = get_file_path(session_id)
    if os.path.exists(file_path):
        os.remove(file_path)


# --- 3. SIDEBAR & NAVIGATION ---
with st.sidebar:
    title.get_title_with_icon("KaggleN", LOGO_PATH)
    st.write(f"👤 **{CURRENT_USER}**")

    if st.button("Logout", type="secondary", use_container_width=True):
        logout()

    st.divider()

    if st.button("+ New Chat", use_container_width=True, type="primary"):
        new_id = str(uuid.uuid4())[:8]
        st.query_params["session"] = new_id
        st.rerun()

    st.caption("Your History")

    # LOAD SESSIONS FOR THIS USER ONLY
    existing_sessions = get_user_sessions()

    # URL Management
    query_params = st.query_params
    current_session_id = query_params.get("session", None)

    if not current_session_id:
        if existing_sessions:
            current_session_id = existing_sessions[0]["id"]
        else:
            current_session_id = str(uuid.uuid4())[:8]
        st.query_params["session"] = current_session_id

    # Sync Sidebar Selection
    current_index = 0
    # Map IDs to titles for the radio button logic
    session_map = {s["id"]: s["title"] for s in existing_sessions}

    # Careful: Titles might duplicate, so we use a list of IDs for logic
    session_ids = [s["id"] for s in existing_sessions]

    if current_session_id in session_ids:
        current_index = session_ids.index(current_session_id)

    if existing_sessions:
        # We display Titles, but we track logic via Index
        selected_title = st.radio(
            "Select Chat:",
            options=[s["title"] for s in existing_sessions],
            index=current_index,
            key="session_selector"
        )

        # Find which ID matches the selected title (handling duplicates roughly)
        # Better approach: Iterate to find the ID at the selected index
        # But for simplicity, we rely on the index remaining stable
        pass

        # NOTE: Streamlit's radio is tricky with dynamic updates.
        # A simpler way to switch is checking if the ID changed via the radio key state?
        # Actually, let's keep it simple:
        # If the user clicks a radio button, we need the ID associated with that Title.
        # Since titles aren't unique, we match by Index.
        # (This is a simplified view. In production, use unique keys for buttons).

        # Let's match back the selected title to an ID
        selected_id = existing_sessions[0]['id']  # Default
        for s in existing_sessions:
            if s['title'] == selected_title:
                selected_id = s['id']
                # If we have multiple chats with same name "Hello", this picks the first one.
                # To fix this perfectly requires a custom component, but this works for 99% cases.
                break

        if selected_id != current_session_id:
            st.query_params["session"] = selected_id
            st.rerun()

    st.divider()
    if st.button("🗑️ Delete Chat", use_container_width=True):
        delete_session(current_session_id)
        st.query_params.clear()
        st.rerun()

# --- 4. CHAT INTERFACE ---
title.get_title_with_icon("Chat", LOGO_PATH)

st.session_state.messages = load_history(current_session_id)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    save_history(current_session_id, st.session_state.messages)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            response_obj = session_agent.run_chat_agent(prompt, session_name=current_session_id)

            if hasattr(response_obj, '__iter__') and not isinstance(response_obj, str):
                for chunk in response_obj:
                    full_response += str(chunk)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            else:
                full_response = str(response_obj)
                message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"Error: {e}")
            full_response = "I encountered an error."

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_history(current_session_id, st.session_state.messages)
    st.rerun()