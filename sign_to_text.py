import streamlit as st
import numpy as np
import cv2
import os

# ----------- HAND SEGMENTATION (REMOVE BACKGROUND) -----------
def extract_hand(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # skin color range (works decently)
    lower = np.array([0, 30, 60])
    upper = np.array([20, 150, 255])

    mask = cv2.inRange(hsv, lower, upper)

    # clean noise
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    return mask


# ----------- GET HAND SHAPE CONTOUR -----------
def get_contour(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        return max(contours, key=cv2.contourArea)
    return None


# ----------- MATCH SHAPES -----------
def match_shape(captured_contour, ref_img):
    ref_mask = extract_hand(ref_img)
    ref_contour = get_contour(ref_mask)

    if ref_contour is None:
        return float("inf")

    # shape similarity
    score = cv2.matchShapes(captured_contour, ref_contour, 1, 0.0)
    return score


# ----------- MAIN FUNCTION -----------
def run_sign_to_text():

    st.title("🤟 ISL Gesture Detection (Shape Matching)")

    img_file = st.camera_input("Capture Hand Sign")

    if img_file:

        data = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)

        if img is None:
            st.error("Invalid image")
            return

        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB),
                 caption="Captured Image", use_container_width=True)

        # extract hand from captured image
        mask = extract_hand(img)
        contour = get_contour(mask)

        if contour is None:
            st.error("No hand detected")
            return

        best_letter = None
        best_score = float("inf")

        folder = "images"

        for file in os.listdir(folder):
            path = os.path.join(folder, file)

            ref = cv2.imread(path)
            if ref is None:
                continue

            score = match_shape(contour, ref)

            if score < best_score:
                best_score = score
                best_letter = file.split(".")[0]

        if best_letter:
            st.success(f"Detected Letter: {best_letter}")
        else:
            st.error("No match found")
