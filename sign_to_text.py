import streamlit as st
import numpy as np
import cv2
import os

# --------- HAND MASK ---------
def get_mask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 30, 60])
    upper = np.array([20, 150, 255])

    mask = cv2.inRange(hsv, lower, upper)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    return mask


# --------- GET CONTOUR ---------
def get_contour(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        return max(contours, key=cv2.contourArea)
    return None


# --------- SHAPE MATCH ---------
def shape_score(c1, c2):
    return cv2.matchShapes(c1, c2, 1, 0.0)


# --------- MAIN ---------
def run_sign_to_text():

    st.title("🤟 Sign to Text (Camera ISL)")

    img_file = st.camera_input("Capture Hand Sign")

    if img_file:

        data = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        captured = cv2.imdecode(data, cv2.IMREAD_COLOR)

        if captured is None:
            st.error("Invalid image")
            return

        st.image(cv2.cvtColor(captured, cv2.COLOR_BGR2RGB),
                 caption="Captured Image", use_container_width=True)

        # Extract hand
        mask = get_mask(captured)
        contour = get_contour(mask)

        if contour is None:
            st.error("No hand detected")
            return

        folder = "images"

        best_letter = None
        best_score = float("inf")

        # Compare with all ISL images
        for file in os.listdir(folder):

            path = os.path.join(folder, file)
            ref = cv2.imread(path)

            if ref is None:
                continue

            ref_mask = get_mask(ref)
            ref_contour = get_contour(ref_mask)

            if ref_contour is None:
                continue

            score = shape_score(contour, ref_contour)

            if score < best_score:
                best_score = score
                best_letter = file.split(".")[0]

        # -------- SHOW RESULT LIKE TEXT→SIGN --------
        if best_letter:

            st.success(f"Detected Letter: {best_letter}")

            cols = st.columns(1)

            file_path = os.path.join("images", f"{best_letter}.jpeg")

            with cols[0]:
                if os.path.exists(file_path):
                    st.image(file_path, width=150, caption=best_letter)
                else:
                    st.write(f"{best_letter} ❌")

        else:
            st.error("No match found")
