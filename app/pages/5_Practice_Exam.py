import streamlit as st
import os
from components.get_title_with_icon import get_title_with_icon


# App Initialization.
# Get the absolute folder path of the current file.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../assets/icon.png"))

st.logo(LOGO_PATH, size="large")


st.set_page_config(
    page_title="Practice Exam",
    page_icon=LOGO_PATH
)

st.title("🧐 Practice Exam")
st.write("🎉 Welcome to NoteTea.")
