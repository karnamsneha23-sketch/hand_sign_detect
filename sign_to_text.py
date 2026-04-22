import streamlit as st
import cv2
import numpy as np
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)

def run_sign_to_text():

    st.title("🤟 Live Sign Detection (Web Camera)")

    st.write("Click below to enable camera and capture hand sign")

    image = st.camera_input("📷 Capture Hand Sign")

    if image:

        # Convert image
        file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Detect hand
        result = hands.process(img_rgb)

        if result.multi_hand_landmarks:

            st.image(img_rgb, caption="Hand Detected", use_container_width=True)

            landmarks = result.multi_hand_landmarks[0].landmark

            # SIMPLE FEATURE (finger position logic)
            index_finger_tip = landmarks[8].y
            thumb_tip = landmarks[4].y

            # Simple rule-based classification
            if index_finger_tip < thumb_tip:
                letter = "A"
            else:
                letter = "B"

            st.success(f"Detected Letter: {letter}")

        else:
            st.warning("No hand detected. Try again.")
