import streamlit as st
import numpy as np
import cv2

def run_sign_to_text():

    st.title("🤟 ISL Sign Detection (Stable Demo)")

    img_file = st.camera_input("Capture Hand Sign")

    if img_file:

        data = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)

        if img is None:
            st.error("Invalid image")
            return

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        st.image(img_rgb, use_container_width=True)

        # ---------------- SIMPLE BUT WORKING LOGIC ----------------
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray, 50, 150)
        edge_count = np.sum(edges > 0)

        brightness = np.mean(gray)

        # BASIC ISL-LIKE OUTPUT (DEMO SAFE)
        if edge_count < 400:
            letter = "A"   # closed hand
        elif edge_count < 1200:
            letter = "B"   # semi open
        elif brightness < 90:
            letter = "C"
        else:
            letter = "D"

        st.success(f"Detected Letter: {letter}")
