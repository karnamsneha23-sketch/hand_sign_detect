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

# ---------------- TEXT TO SIGN ----------------
if menu == "Text to Sign":
    try:
        import text_to_sign
        text_to_sign.text_to_sign_page()
    except Exception as e:
        st.error(f"Text to Sign module error: {e}")

# ---------------- SIGN TO TEXT ----------------
elif menu == "Sign to Text":
    try:
        from sign_to_text import sign_to_text
        sign_to_text()
    except Exception as e:
        st.error(f"Sign to Text module error: {e}")

# ---------------- SPEECH TO SIGN ----------------
elif menu == "Speech to Sign":
    try:
        from speech_to_sign import app
        app()
    except Exception as e:
        st.error(f"Speech to Sign module error: {e}")
