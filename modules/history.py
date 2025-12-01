import json
import os
import streamlit as st
from config import HISTORY_PATH


class HistoryManager:
    """
    Handles loading and saving chat history.
    """
    @staticmethod
    def load():
        if os.path.exists(HISTORY_PATH):
            try:
                with open(HISTORY_PATH, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    @staticmethod
    def save(messages):
        with open(HISTORY_PATH, "w") as f:
            json.dump(messages, f, indent=4)

    @staticmethod
    def clear():
        HistoryManager.save([])
        st.session_state.messages = []


if __name__ == "__main__":
    HistoryManager.load()