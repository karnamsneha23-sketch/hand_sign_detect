import streamlit as st

st.set_page_config(page_title="ISL Translator", layout="centered")

# Main heading
st.title("🤟 Hand Talk Bridge")

# Subheading
st.subheader("Two-way ISL Translator System")

# Sidebar menu
menu = st.sidebar.radio(
    "Select Option",
    ["Text to Sign", "Sign to Text", "Speech to Sign"]
)

# ---------------- SAFE IMPORTS (FIXED) ----------------
if menu == "Text to Sign":
    try:
        from text_to_sign import text_to_sign_page
        text_to_sign_page()
    except Exception as e:
        st.error(f"Text to Sign module error: {e}")

elif menu == "Sign to Text":
    try:
        from sign_to_text import sign_to_text  # FIXED NAME
        sign_to_text()
    except Exception as e:
        st.error(f"Sign to Text module error: {e}")

elif menu == "Speech to Sign":
    try:
        from speech_to_sign import app
        app()
    except Exception as e:
        st.error(f"Speech to Sign module error: {e}")
