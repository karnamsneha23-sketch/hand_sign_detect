import streamlit as st
import os

IMAGES_PATH = "images"

def get_image(char):
    # check all possible extensions
    for ext in [".jpg", ".png", ".jpeg"]:
        path = os.path.join(IMAGES_PATH, char.upper() + ext)
        if os.path.exists(path):
            return path
    return None

def text_to_sign_page():
    st.title("📝 Text → Sign")

    text = st.text_input("Enter text")

    # DEBUG
    st.write("Typed:", text)

    if st.button("Convert"):
        if text.strip() == "":
            st.warning("Enter text first!")
            return

        st.success("Converting...")

        cols = st.columns(len(text))

        for i, char in enumerate(text):
            if char.isalpha():
                img_path = get_image(char)

                if img_path:
                    cols[i].image(img_path, caption=char)
                else:
                    cols[i].error(f"{char} ❌ not found")