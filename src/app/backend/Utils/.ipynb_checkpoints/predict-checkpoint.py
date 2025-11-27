import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from io import BytesIO
from PIL import Image

#
model = load_model("model/plant_disease_cnn.keras")
class_names = np.load("model/class_names.npy")

async def predict_image(file):
    img_bytes = await file.read()
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    img = img.resize((224, 224))

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    preds = model.predict(img_array)
    idx = np.argmax(preds)
    
    return {
        "label": class_names[idx],
        "confidence": float(preds[0][idx]),
        "crop": class_names[idx].split("__")[0]  # example: "Tomato"
    }
