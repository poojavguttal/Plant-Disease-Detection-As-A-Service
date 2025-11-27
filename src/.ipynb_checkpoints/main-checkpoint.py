from fastapi import FastAPI, File, UploadFile
from fastapi.middlewear.cors import CORSMiddleware
from utils.predict import predict_image
from utils.advice import generate_advice
from pydantic import BaseModel 

app = FastAPI()

app.add_middlewear(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

class AdviceRequest(BaseModel):
    crop:str
    label:str
    confidence:float

@app.get("/")
def root():
    return {"message": "Plant Disease API is running!"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    result = await predict_image(file)
    return result

@app.post("/advice")
async def advice(request: AdviceRequest):
    result = await generate_advice(request)
    return result




    