import os
# import base64
import streamlit as st
from components.get_title_with_icon import get_title_with_icon


# App Initialization.
# Get the absolute folder path of the current file.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
st.write(BASE_DIR)
LOGO_PATH = os.path.abspath(os.path.join(BASE_DIR, "../assets/icon.png"))
st.write(LOGO_PATH)
# another_icon = os.path.join(BASE_DIR, "../../assets/icon.png")


st.set_page_config(
    page_title="NoteTea",
    page_icon=LOGO_PATH
)

# # Define pages and set their sidebar labels explicitly refer to your app file but label it "Home"
# home_page = st.Page("pages/1_Home.py", title="Home", icon=LOGO_PATH)
# #
# nav = st.navigation([home_page])   # place navigation in sidebar by default
# s = nav.run()


# Title Section.
get_title_with_icon("NoteTea", LOGO_PATH)
st.badge("Turn Notes Into Memory.", icon=":material/star:", color="violet")
