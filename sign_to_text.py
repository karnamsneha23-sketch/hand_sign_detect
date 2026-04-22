import streamlit as st
import cv2
import numpy as np

# SAFE MEDIAPIPE IMPORT
try:
    import mediapipe as mp
    hands_module = mp.solutions.hands
    draw_module = mp.solutions.drawing_utils
    mp_available = True
except Exception:
    mp_available = False

def run_sign_to_text():

    st.title("🤟 ISL Sign Detection")

    if not mp_available:
        st.error("⚠️ MediaPipe not working in deployment")
        st.info("Showing demo detection instead")
    
    img_file = st.camera_input("Capture Hand Sign")

    if img_file:

        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        st.image(img_rgb, use_container_width=True)

        # ---------------- REAL IF MEDIAPIPE WORKS ----------------
        if mp_available:

            hands = hands_module.Hands(static_image_mode=True, max_num_hands=1)
            results = hands.process(img_rgb)

            if results.multi_hand_landmarks:
                lm = results.multi_hand_landmarks[0].landmark

                # -------- BASIC ISL LOGIC --------
                thumb = lm[4].y
                index = lm[8].y
                middle = lm[12].y
                ring = lm[16].y
                pinky = lm[20].y
                wrist = lm[0].y

                # 🟢 FEW REALISTIC ISL LETTER RULES
                if index < wrist and middle < wrist and ring < wrist and pinky < wrist:
                    letter = "B"   # open palm

                elif index < wrist and middle > wrist:
                    letter = "D"   # index finger up

                elif index > wrist and middle > wrist and ring > wrist:
                    letter = "A"   # fist

                else:
                    letter = "C"

                st.success(f"Detected Letter: {letter}")

            else:
                st.warning("No hand detected")

        # ---------------- FALLBACK (NO MEDIAPIPE) ----------------
        else:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            avg = np.mean(gray)

            if avg < 80:
                letter = "A"
            elif avg < 120:
                letter = "B"
            else:
                letter = "C"

            st.success(f"Demo Letter: {letter}")
