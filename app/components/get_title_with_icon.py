import base64
import streamlit as st


def get_title_with_icon(text: str, icon_path: str, width: int = 40, offset_px: int = -5) -> None:
    """
    Display a Streamlit title with an inline icon (local image).

    Parameters:
        text (str): The title.
        icon_path (str): Path to the local icon .
        width (int): Width of the icon in pixels.
        offset_px (int): Vertical offset in pixels (negative moves up).
    """
    # Convert local image to base64.
    with open(icon_path, "rb") as file:
        icon_base64 = file.read()

    icon_url = base64.b64encode(icon_base64).decode()

    # Display inline title with HTML.
    st.markdown(
        f"""
        <h1>
            <img src="data:image/png;base64,{icon_url}" 
                width="{width}"
                style="vertical-align:middle; position:relative; top:{offset_px}px;"/>
            {text}
        </h1>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    pass
