import streamlit as st
import os
from components.get_title_with_icon import get_title_with_icon


# App Initialization.
# Get the absolute folder path of the current file.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../assets/icon.png"))

st.logo(LOGO_PATH, size="large")

st.title("🤔 Quiz")
st.write("🎉 Welcome to NoteTea.")
