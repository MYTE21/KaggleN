import streamlit as st

# --- Data ---
# A simple list of dictionaries to hold our flashcard content
FLASHCARDS = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is 2 + 2?", "answer": "4"},
    {"question": "What element has the atomic number 1?", "answer": "Hydrogen"},
    {"question": "Who wrote 'Romeo and Juliet'?", "answer": "William Shakespeare"},
    {"question": "What is the powerhouse of the cell?", "answer": "Mitochondria"},
]

# --- App Initialization ---

# Set the page title and a simple layout
st.set_page_config(page_title="Simple Flashcards", layout="centered")

st.title("Simple Streamlit Flashcards 📇")
st.write("A basic app to demonstrate flashcard logic in Streamlit.")

# Initialize session state variables if they don't exist
# 'card_index' tracks which card we are on
if 'card_index' not in st.session_state:
    st.session_state.card_index = 0

# 'flipped' tracks whether the current card is showing the answer
if 'flipped' not in st.session_state:
    st.session_state.flipped = False

# --- Helper Functions ---

def go_to_next_card():
    """Increments the card index, wrapping around to the beginning if at the end."""
    current_index = st.session_state.card_index
    # Use modulo operator to wrap around
    st.session_state.card_index = (current_index + 1) % len(FLASHCARDS)
    # Reset the flipped state for the new card
    st.session_state.flipped = False

def flip_card():
    """Toggles the 'flipped' state."""
    st.session_state.flipped = not st.session_state.flipped

# --- App Layout ---

# Get the current card from our list based on the index
current_card = FLASHCARDS[st.session_state.card_index]

# Display the card number
st.write(f"---")
st.write(f"**Card {st.session_state.card_index + 1} of {len(FLASHCARDS)}**")
st.write(f"---")


# Card Display Logic
# We use a container to create a visual "card"
with st.container(border=True):
    # Apply custom CSS for min-height to keep the card size consistent
    st.markdown(
        """
        <style>
        [data-testid="stVerticalBlockBorderWrapper"] > [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
            min-height: 150px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.flipped:
        # --- Back of Card (Answer) ---
        st.subheader(current_card["answer"])
    else:
        # --- Front of Card (Question) ---
        st.subheader(current_card["question"])


# --- Buttons ---

# Create two columns for the buttons
col1, col2 = st.columns(2)

with col1:
    # The "Flip" button calls the flip_card function
    st.button("Flip Card", on_click=flip_card, use_container_width=True, type="primary")

with col2:
    # The "Next" button calls the go_to_next_card function
    st.button("Next Card →", on_click=go_to_next_card, use_container_width=True)