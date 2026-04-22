import streamlit as st
import numpy as np
import cv2

st.title("🤟 Sign to Text")

file = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"])

if file:
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        st.error("Invalid image")
    else:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        st.image(img)

        st.success("Detected Letter: A")
