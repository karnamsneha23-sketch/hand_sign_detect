# utils.py
import streamlit as st
import threading
from gtts import gTTS
import os
import pickle
import tensorflow as tf

def speak_async(text):
    """Speak text asynchronously"""
    def speak():
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save("temp_audio.mp3")
            os.system("start temp_audio.mp3" if os.name == 'nt' else "afplay temp_audio.mp3")
        except:
            pass
    
    thread = threading.Thread(target=speak, daemon=True)
    thread.start()

def init_session_state():
    """Initialize session state variables"""
    if 'run_cam' not in st.session_state:
        st.session_state.run_cam = False
    if 'sentence' not in st.session_state:
        st.session_state.sentence = ""
    if 'word_buffer' not in st.session_state:
        st.session_state.word_buffer = []
    if 'current_predictions' not in st.session_state:
        st.session_state.current_predictions = []
    if 'last_letter' not in st.session_state:
        st.session_state.last_letter = ""
    if 'last_time' not in st.session_state:
        st.session_state.last_time = 0
    if 'no_hand_time' not in st.session_state:
        st.session_state.no_hand_time = 0

@st.cache_resource
def load_model_and_labels():
    """Load trained model and labels"""
    try:
        model = tf.keras.models.load_model('model/sign_model.h5')
        with open('model/labels.pkl', 'rb') as f:
            labels = pickle.load(f)
        return model, labels
    except:
        st.error("Model files not found!")
        return None, None