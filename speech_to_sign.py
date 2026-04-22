import streamlit as st
import speech_recognition as sr
import os
import tempfile

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Speech to ISL", layout="centered")
r = sr.Recognizer()

# ---------------- SPEECH (FILE BASED) ----------------
def process_audio(uploaded_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        with sr.AudioFile(temp_path) as source:
            audio = r.record(source)

        text = r.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        st.error("⚠️ No internet / API issue")
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

    # ✅ ONLY AUDIO UPLOAD
    uploaded_file = st.file_uploader("Upload your speech (.wav)", type=["wav"])

    if uploaded_file:
        st.info("🔄 Processing audio...")
        text = process_audio(uploaded_file)

        if text:
            st.success("✅ You said: " + text)
            show_isl(text)
        else:
            st.error("❌ Could not understand audio")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app()
