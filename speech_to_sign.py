import streamlit as st
import speech_recognition as sr
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Speech to ISL", layout="centered")
r = sr.Recognizer()

# ---------------- SPEECH ----------------
def listen_speech():
    with sr.Microphone() as source:
        st.info("🎤 SPEAK NOW (don’t click anything)")
        r.adjust_for_ambient_noise(source, duration=0.3)
        audio = r.listen(source, timeout=None, phrase_time_limit=5)

    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        st.error("⚠️ Speech recognition service unavailable. Check internet connection.")
        return None
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None

# ---------------- ISL ----------------
def show_isl(text):
    text = text.upper()
    st.subheader("🤟 ISL OUTPUT")

    cols = st.columns(min(len(text), 6))
    i = 0

    for ch in text:
        if ch == " ":
            continue

        found = False
        for ext in [".jpeg", ".jpg", ".png"]:
            path = os.path.join("images", f"{ch}{ext}")
            if os.path.exists(path):
                with cols[i % 6]:
                    st.image(path, width=100, caption=ch)
                found = True
                break

        if not found:
            with cols[i % 6]:
                st.markdown(ch)

        i += 1

# ---------------- APP ----------------
def app():
    st.title("🎤➡️🤟 Speech to ISL")

    if "text" not in st.session_state:
        st.session_state.text = ""

    if st.button("🎙️ START SPEECH"):
        text = listen_speech()
        if text:
            st.session_state.text = text
            st.success("✅ You said: " + text)
        else:
            st.error("❌ Could not understand speech")

    # Manual fallback for deployment
    manual_text = st.text_input("Or type text here:")
    if manual_text:
        st.session_state.text = manual_text

    if st.session_state.text:
        show_isl(st.session_state.text)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app()
