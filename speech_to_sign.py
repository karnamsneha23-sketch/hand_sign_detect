import streamlit as st
import speech_recognition as sr
import tempfile

def run_speech_to_sign():

    st.title("🎤 Speech to Sign")

    r = sr.Recognizer()

    uploaded_file = st.file_uploader("Upload WAV audio", type=["wav"])

    if uploaded_file:
        try:
            # save temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(uploaded_file.read())
                path = tmp.name

            # speech recognition
            with sr.AudioFile(path) as source:
                audio = r.record(source)

            text = r.recognize_google(audio)
            st.success(f"You said: {text}")

            # dummy sign output
            st.subheader("🤟 Sign Output")
            st.write("Sign representation: " + text.upper())

        except Exception as e:
            st.error(f"Error: {e}")
