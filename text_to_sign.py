import streamlit as st
import os

def text_to_sign_page():
    st.title("Text to Sign")

    text = st.text_input("Enter text")

    if text:
        for ch in text.lower():
            file_name = f"{ch.upper()}.jpeg"

            if os.path.exists(file_name):
                st.image(file_name, width=100)
            else:
                st.write(f"{ch} ❌ not found")
