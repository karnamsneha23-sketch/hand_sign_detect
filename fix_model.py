from tensorflow.keras.models import load_model

# load old model safely
model = load_model("model/sign_model.keras", compile=False)

# re-save in new compatible format
model.save("model/fixed_model.keras")

print("Model fixed and saved successfully!")