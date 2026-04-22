import streamlit as st
import cv2
import numpy as np
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

def run_sign_to_text():

    st.title("🤟 Sign to Text (Camera)")

    img_file = st.camera_input("Capture your hand sign")

    if img_file:

        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        result = hands.process(img_rgb)

        if result.multi_hand_landmarks:

            for handLms in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(img_rgb, handLms, mp_hands.HAND_CONNECTIONS)

            st.image(img_rgb, caption="Hand Detected", use_container_width=True)

            landmarks = result.multi_hand_landmarks[0].landmark

            # SIMPLE REAL LOGIC (based on finger positions)
            index_tip = landmarks[8].y
            middle_tip = landmarks[12].y
            wrist = landmarks[0].y

            if index_tip < wrist and middle_tip < wrist:
                letter = "B"
            elif index_tip < wrist:
                letter = "D"
            else:
                letter = "A"

            st.success(f"Detected Letter: {letter}")

        else:
            st.warning("No hand detected")
