import streamlit as st
from components import title
from modules.history import HistoryManager
from config import LOGO_PATH


def render_sidebar():
    with st.sidebar:
        title.get_title_with_icon("KaggleN", LOGO_PATH)
        st.badge("Partner of your Kaggle journey.", icon=":material/star:", color="violet")

        st.divider()

        selected_agent = st.selectbox(
            "Select Agent",
            ["Search", "Kaggle", "Notion"],
            index=0
        )

        st.divider()

        if st.button("Clear Chat History", type="primary", use_container_width=True):
            HistoryManager.clear()
            st.rerun()

    return selected_agent