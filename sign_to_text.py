import streamlit as st
import numpy as np
import cv2

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

    st.title("🤟 Sign to Text (Upload + Match)")

    st.write("Step 1: Upload reference ISL images (A, B, C...)")
    ref_files = st.file_uploader(
        "Upload gesture images", type=["jpg", "jpeg", "png"], accept_multiple_files=True
    )

    if not ref_files:
        st.warning("Upload reference images first")
        return

    # Load reference contours
    ref_contours = {}

    for file in ref_files:
        file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
            continue

        mask = get_mask(img)
        contour = get_contour(mask)

        if contour is not None:
            label = file.name.split(".")[0].upper()  # A.jpg → A
            ref_contours[label] = contour

    if not ref_contours:
        st.error("No valid hand shapes in reference images")
        return

    st.success(f"{len(ref_contours)} reference gestures loaded")

    # -------- CAPTURE --------
    img_file = st.camera_input("Capture Hand Sign")

    if img_file:

        data = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        captured = cv2.imdecode(data, cv2.IMREAD_COLOR)

        if captured is None:
            st.error("Invalid capture")
            return

        st.image(cv2.cvtColor(captured, cv2.COLOR_BGR2RGB),
                 caption="Captured Image", use_container_width=True)

        mask = get_mask(captured)
        contour = get_contour(mask)

        if contour is None:
            st.error("No hand detected")
            return

        best_letter = None
        best_score = float("inf")

        for label, ref_contour in ref_contours.items():
            score = shape_score(contour, ref_contour)

            if score < best_score:
                best_score = score
                best_letter = label

        if best_letter:
            st.success(f"Detected Letter: {best_letter}")
        else:
            st.error("No match found")
