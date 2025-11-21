import streamlit as st


# Define the Pages.
home_page = st.Page("pages/1_Home.py", title="Home", icon="🏠")
summary_page = st.Page("pages/2_Summary.py", title="Summary", icon="📝")
flash_card_page = st.Page("pages/3_Flash_Card.py", title="Flash Card", icon="🏞️")
quiz_page = st.Page("pages/4_Quiz.py", title="Quiz", icon="🪶")
practice_exam_page = st.Page("pages/5_Practice_Exam.py", title="Practice Exam", icon="☕️")
about_page = st.Page("pages/6_About.py", title="About", icon="📜")

navigation = st.navigation([
    home_page,
    summary_page,
    flash_card_page,
    quiz_page,
    practice_exam_page,
    about_page,
])

navigation.run()