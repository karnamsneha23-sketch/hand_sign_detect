import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
import time
from collections import deque
from gtts import gTTS
import os
from playsound import playsound
import uuid

# ---------------- INIT ----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# ---------------- SESSION ----------------
if "sentence" not in st.session_state:
    st.session_state.sentence = ""

if "last_speech" not in st.session_state:
    st.session_state.last_speech = ""

if "buffer" not in st.session_state:
    st.session_state.buffer = deque(maxlen=7)

# ---------------- SAFE SPEECH (NEW FIX) ----------------
def speak(text):
    try:
        if not text:
            return

        file = f"speech_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text=text, lang="en")
        tts.save(file)

        playsound(file)
        os.remove(file)

    except:
        pass

# ---------------- FINGERS ----------------
def get_fingers(hand):
    tips = [8, 12, 16, 20]
    fingers = []

    if hand.landmark[4].x < hand.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    for tip in tips:
        if hand.landmark[tip].y < hand.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

# ---------------- CLASSIFIER ----------------
def classify(hand):

    thumb, index, middle, ring, pinky = get_fingers(hand)
    total = thumb + index + middle + ring + pinky

    # ---- BASIC ----
    if total == 0:
        return "A"  # also E, S fallback

    if thumb == 0 and index == 1 and middle == 1 and ring == 1 and pinky == 1:
        return "B"

    if index == 1 and middle == 1 and ring == 0:
        return "C"

    if index == 1 and total == 1:
        return "D"

    if thumb == 1 and index == 1 and middle == 0:
        return "F"

    if index == 1 and middle == 0 and ring == 0:
        return "G"

    if index == 1 and middle == 1:
        return "H"

    if pinky == 1 and total == 1:
        return "I"

    if thumb == 1 and index == 1:
        return "L"

    if index == 1 and middle == 1 and ring == 1:
        return "W"

    if thumb == 1 and pinky == 1:
        return "Y"

    # ---- EXTRA APPROX LETTERS ----
    if index == 1 and middle == 0 and ring == 0 and pinky == 0:
        return "J"   # motion-based approx

    if index == 1 and middle == 1 and ring == 0:
        return "K"

    if index == 0 and middle == 0 and ring == 0:
        return "M"

    if index == 0 and middle == 0:
        return "N"

    if thumb == 0 and index == 0 and middle == 0:
        return "O"

    if index == 1 and middle == 1 and ring == 1:
        return "P"

    if thumb == 1 and index == 1 and middle == 1:
        return "Q"

    if index == 1 and middle == 1:
        return "R"

    if thumb == 0 and index == 0:
        return "T"

    if index == 1 and middle == 1 and ring == 0:
        return "U"

    if index == 1 and middle == 1:
        return "V"

    if index == 1:
        return "X"

    if thumb == 1 and pinky == 1:
        return "Y"

    if index == 1:
        return "Z"

    return None


# ---------------- STABILITY ----------------
def stable(letter):
    st.session_state.buffer.append(letter)
    if len(st.session_state.buffer) < 5:
        return letter
    return max(set(st.session_state.buffer), key=st.session_state.buffer.count)

# ---------------- APP ----------------
def sign_to_text():

    st.title("🤟 sign to text")

    run = st.checkbox("Start Camera")

    frame_box = st.image([])
    output = st.empty()

    cap = cv2.VideoCapture(0)

    last_letter = None
    last_time = time.time()

    st.sidebar.header("Controls")

    if st.sidebar.button("🔄 Reset"):
        st.session_state.sentence = ""
        st.session_state.last_speech = ""

    if st.sidebar.button("🔊 Speak Now"):
        text = st.session_state.sentence.strip()
        if text:
            speak(text)
            st.session_state.last_speech = text

    # ---------------- LOOP ----------------
    while run:

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = hands.process(rgb)

        letter = None

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            raw = classify(hand)

            if raw:
                letter = stable(raw)

                if letter != last_letter or time.time() - last_time > 1.0:
                    st.session_state.sentence += letter
                    last_letter = letter
                    last_time = time.time()

        # SPACE LOGIC
        if letter is None:
            if time.time() - last_time > 2.0:
                if not st.session_state.sentence.endswith(" "):
                    st.session_state.sentence += " "
                    last_time = time.time()

        # ---------------- FIXED SPEECH ----------------
        text = st.session_state.sentence.strip()

        if len(text) > 2:
            if st.session_state.sentence.endswith(" ") and text != st.session_state.last_speech:
                st.session_state.last_speech = text
                speak(text)

        frame_box.image(frame, channels="BGR")
        output.markdown(f"## 📝 Sentence: {st.session_state.sentence}")

    cap.release()

# ---------------- RUN ----------------
if __name__ == "__main__":
    sign_to_text()