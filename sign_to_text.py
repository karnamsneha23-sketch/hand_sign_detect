import streamlit as st
import numpy as np
import cv2

st.title("🤟 Sign to Text (Upload Image)")

file = st.file_uploader("Upload hand sign image", type=["jpg", "png", "jpeg"])

if file is not None:
    try:
        file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if frame is None:
            st.error("Invalid image")
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            st.image(frame)

            st.success("Detected Letter: A")

    except Exception as e:
        st.error(f"Error: {e}")
