import os
import streamlit as st
from components.get_title_with_icon import get_title_with_icon


LOGO_PATH = os.path.join(os.getcwd(), "assets/icon.png")

st.set_page_config(
    page_title="KaggleN",
    page_icon=LOGO_PATH
)

# Title Section.
get_title_with_icon("KaggleN", LOGO_PATH)
st.badge("Partner of your Kaggle journey.", icon=":material/star:", color="violet")