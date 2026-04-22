import streamlit as st
import numpy as np
import cv2

# ---------------- DUMMY MODEL ----------------
def classify_dummy():
    return "A"

# ---------------- MAIN ----------------
def sign_to_text():

    st.title("🤟 Sign to Text (Upload Image)")

    file = st.file_uploader("Upload hand sign image", type=["jpg", "png", "jpeg"])

    if file is not None:
        try:
            # ✅ SAFE IMAGE READ (NO CRASH)
            file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
            frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            if frame is None:
                st.error("❌ Invalid image file")
                return

            # convert BGR → RGB (for correct display)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            st.image(frame, caption="Uploaded Image", use_column_width=True)

            # dummy prediction
            letter = classify_dummy()

            st.success(f"Detected Letter: {letter}")

            # 🔊 voice output
            st.audio(
                f"https://translate.google.com/translate_tts?ie=UTF-8&q={letter}&tl=en&client=tw-ob"
            )

        except Exception as e:
            st.error(f"❌ Error: {e}")

# ---------------- RUN ----------------
if __name__ == "__main__":
    sign_to_text()
