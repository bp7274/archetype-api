
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests


HF_TOKEN = "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"
MODEL_NAME = "bp7274/soulprint-model"
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}
class UserInput(BaseModel):
    age: int
    location: str
    profession: str
    personality: str
app = FastAPI()
# Optional: for Render's GET ping
@app.get("/")
def root():
    return {"message": "Service is running"}
# Optional: for frontend (e.g., Unity, browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/")
async def generate_quote(data: UserInput):
    try:
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


