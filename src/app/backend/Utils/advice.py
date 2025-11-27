import os
import google.generativeai as genai

# Load API key from environment
genai.configure(api_key=os.getenv(""))

model = genai.GenerativeModel("gemini-1.5-flash")

async def generate_advice(payload):
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
