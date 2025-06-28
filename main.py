from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Load model from Hugging Face Hub
classifier = pipeline("text-classification", model="bp7274/archetype-model")

app = FastAPI()

class InputText(BaseModel):
    text: str

@app.post("/predict")
async def predict(input: InputText):
    result = classifier(input.text)
    return {"result": result}
