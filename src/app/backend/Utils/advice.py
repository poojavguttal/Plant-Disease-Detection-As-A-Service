import os
import google.generativeai as genai

# Load API key from environment
# genai.configure(api_key=os.getenv(""))

import google.generativeai as genai

import os
from dotenv import load_dotenv

# load_dotenv()  # Load .env locally

# load_dotenv(dotenv_path="src/app/backend/.env")
my_api_key = "AIzaSyC0sIXnx8wyeyQafaVRDtDVQRAf0Iv7nPI"
genai.configure(api_key=my_api_key)




async def generate_advice(payload):
    model = genai.GenerativeModel("models/gemini-flash-latest")
    system_prompt = f"""
    You are an agricultural extension advisor.
    Only use trusted sources: .edu, .gov, FAO.org, IPM guidelines.
    """

    user_prompt = f"""
    Crop: {payload.crop}
    Disease: {payload.label}
    Confidence: {payload.confidence}

    Provide farmer-friendly steps:
    - do_now
    - treatment_classes
    - prevention
    - citations (only trusted)
    - disclaimer
    """

    response = model.generate_content(
        [
            {"role": "system", "parts": system_prompt},
            {"role": "user", "parts": user_prompt},
        ]
    )

    return {"advice": response.text}
