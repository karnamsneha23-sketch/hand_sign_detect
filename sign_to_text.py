import streamlit as st
import cv2
import numpy as np

def classify_dummy():
    # simple demo mapping (you can improve later)
    return "A"

def sign_to_text():

    st.title("🤟 Sign to Text (Upload Image)")

    file = st.file_uploader("Upload hand sign image", type=["jpg", "png", "jpeg"])

    if file is not None:
        # read image
        file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)

        st.image(frame, channels="BGR")

        # dummy prediction (replace later with model)
        letter = classify_dummy()

        st.success(f"Detected Letter: {letter}")

        # speak using browser audio
        st.audio(
            f"https://translate.google.com/translate_tts?ie=UTF-8&q={letter}&tl=en&client=tw-ob"
        )
