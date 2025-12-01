import base64
import os
import streamlit as st
from config import LOGO_PATH


def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()

    return base64.b64encode(data).decode()


def render_welcome_screen():
    img_base64 = get_base64_image(LOGO_PATH)

    if img_base64:
        img_src = f"data:image/png;base64,{img_base64}"
        img_tag = f'<img src="{img_src}" width="80" style="margin-bottom: 20px;">'
    else:
        img_tag = '<div style="font-size: 80px; margin-bottom: 20px;">🤖</div>'

    # Render HTML.
    st.markdown("""
        <style>
            .welcome-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                margin-top: 50px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="welcome-container">
            {img_tag}
            <h1>Welcome to KaggleN</h1>
            <p style="color: gray; font-size: 1.1em;">
                Your AI Partner for Data Science Competitions.<br>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Suggestions.
    st.divider()
    st.caption("Try asking about:")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📊 **Analyze**\n\nAnalyze the Titanic dataset for me.")
    with col2:
        st.info("🔍 **Search**\n\nWhat are the latest Kaggle competitions?")
    with col3:
        st.info("🐍 **Code**\n\nWrite a Pandas script to clean missing values.")
