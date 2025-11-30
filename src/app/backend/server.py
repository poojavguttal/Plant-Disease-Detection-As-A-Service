import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from io import BytesIO
import google.generativeai as genai

# Load .env file
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # Configure Gemini
# genai.configure(api_key=GEMINI_API_KEY)
import os
from dotenv import load_dotenv

# load_dotenv()  # Load .env locally

# load_dotenv(dotenv_path="src/app/backend/.env")


# print("KEY:", os.getenv("GOOGLE_API_KEY"))


# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyC0sIXnx8wyeyQafaVRDtDVQRAf0Iv7nPI")
my_api_key = "AIzaSyC0sIXnx8wyeyQafaVRDtDVQRAf0Iv7nPI"
genai.configure(api_key=my_api_key)




app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



model = load_model("models/plant_disease_cnn.keras")
class_names = np.load("models/class_names.npy")

# models = genai.list_models()
# for model in models:
#     # Some SDKs use 'supported_generation_methods', some 'supported_methods'
#     supported = getattr(model, "supported_generation_methods", getattr(model, "supported_methods", []))
#     if "generateContent" in supported:
#         print(f"Name: {model.name}, Description: {getattr(model, 'description', 'No description')}")


def preprocess(image_bytes):
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    img_bytes = await file.read()
    input_tensor = preprocess(img_bytes)

    preds = model.predict(input_tensor)[0]
    idx = int(np.argmax(preds))
    label = class_names[idx]
    confidence = float(preds[idx])

    return {
        "label": label,
        "confidence": confidence
    }

@app.post("/advice")
async def advice(data: dict):
    label = data["label"]
    confidence = data["confidence"]
    lang = data.get("lang", "English")

    prompt = f"""
    You are an agricultural advisor. Only give advice based on trusted sources (.edu, .gov, FAO).
    Answer in {lang}.
    Disease: {label}
    Confidence: {confidence}
    """

    response = genai.GenerativeModel("models/gemini-flash-latest").generate_content(prompt)

    return { "advice": response.text }
