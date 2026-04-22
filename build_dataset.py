import cv2
import mediapipe as mp
import os
import numpy as np
import pickle

DATASET_PATH =  r"C:\Users\kramu\OneDrive\Desktop\sign.project\backend\dataset"
OUTPUT_FILE = "features.pkl"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)

data = []
labels = []

def get_landmarks(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    if res.multi_hand_landmarks:
        hand = res.multi_hand_landmarks[0]

        return np.array(
            [[lm.x, lm.y, lm.z] for lm in hand.landmark]
        ).flatten()

    return None

for file in os.listdir(DATASET_PATH):
    path = os.path.join(DATASET_PATH, file)
    img = cv2.imread(path)

    if img is None:
        continue

    features = get_landmarks(img)

    if features is not None:
        data.append(features)
        labels.append(os.path.splitext(file)[0].upper())
        print("✔", file)
    else:
        print("❌ No hand detected:", file)

print("\nTotal:", len(data))

with open(OUTPUT_FILE, "wb") as f:
    pickle.dump((data, labels), f)

print("✔ Saved features.pkl")