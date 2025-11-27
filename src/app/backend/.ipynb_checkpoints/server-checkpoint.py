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
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model & class names
model = load_model("/app/models/plant_disease_cnn.keras")
class_names = np.load("/app/models/class_names.npy").tolist()

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

    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)

    return { "advice": response.text }
