import streamlit as st

st.set_page_config(page_title="ISL Translator", layout="centered")

# ---------------- HEADER ----------------
st.title("🤟 Hand Talk Bridge")
st.subheader("Two-way ISL Translator System")

# ---------------- MENU ----------------
menu = st.sidebar.radio(
    "Select Option",
    ["Text to Sign", "Sign to Text", "Speech to Sign"]
)

# ---------------- TEXT TO SIGN ----------------
if menu == "Text to Sign":
    try:
        import text_to_sign
        text_to_sign.text_to_sign_page()   # MUST match function name
    except Exception as e:
        st.error("Text to Sign module error")
        st.error(e)

# ---------------- SIGN TO TEXT ----------------
elif menu == "Sign to Text":
    try:
        import sign_to_text
        sign_to_text.run_sign_to_text()    # FIXED FUNCTION NAME
    except Exception as e:
        st.error("Sign to Text module error")
        st.error(e)

# ---------------- SPEECH TO SIGN ----------------
elif menu == "Speech to Sign":
    try:
        import speech_to_sign
        speech_to_sign.run_speech_to_sign()  # FIXED FUNCTION NAME
    except Exception as e:
        st.error("Speech to Sign module error")
        st.error(e)
