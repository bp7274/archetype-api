
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
import uvicorn

# Replace with your actual Hugging Face token
HF_TOKEN = "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"
MODEL_NAME = "bp7274/soulprint-model"

# Set headers for the Inference API
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# Define input format
class UserInput(BaseModel):
    age: str
    location: str
    profession: str
    personality: str

app = FastAPI()

@app.post("/")
async def generate_quote(data: UserInput):
    try:
        # Create input string (you may need to adapt based on how your model expects it)
        prompt = f"{data.age}, {data.location}, {data.profession}, {data.personality}"

        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
            headers=headers,
            json={"inputs": prompt}
        )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        output = response.json()
        if isinstance(output, list):
            return {"quote": output[0]["generated_text"]}
        else:
            return {"quote": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional: local dev
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


