import streamlit as st
import os

def text_to_sign_page():
    st.title("Text to Sign")

    text = st.text_input("Enter text")

    if text:
        st.write("Output:")

        # create columns equal to number of letters
        cols = st.columns(len(text))

        for i, ch in enumerate(text.lower()):
            if ch == " ":
                continue

            file_name = f"{ch.upper()}.jpeg"

            with cols[i]:
                if os.path.exists(file_name):
                    st.image(file_name, width=120)
                else:
                    st.write(f"{ch} ❌")
