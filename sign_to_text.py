import streamlit as st
import numpy as np
import cv2

def run_sign_to_text():

    file = st.file_uploader("Upload hand sign image", type=["jpg", "png", "jpeg"])

    if file:
        try:
            # read image safely
            data = np.asarray(bytearray(file.read()), dtype=np.uint8)
            img = cv2.imdecode(data, cv2.IMREAD_COLOR)

            if img is None:
                st.error("❌ Invalid image file")
                return

            # convert BGR → RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            st.image(img, caption="Uploaded Image", use_container_width=True)

            # dummy prediction (replace later with ML model)
            predicted_letter = "A"

            st.success(f"Detected Letter: {predicted_letter}")

        except Exception as e:
            st.error(f"Error: {e}")
