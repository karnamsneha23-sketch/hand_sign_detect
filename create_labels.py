import pickle

labels = {i: chr(65 + i) for i in range(26)}

with open("model/labels.pkl", "wb") as f:
    pickle.dump(labels, f)

print("labels.pkl created successfully ✔")