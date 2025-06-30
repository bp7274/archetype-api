from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Load model from Hugging Face Hub
from transformers import pipeline
app = FastAPI()
# Load your Hugging Face model
pipe = pipeline("text2text-generation", model="bp7274/archetype-model")
@app.post("/predict")
# Function to generate quote
def generate_quote(age, location, profession, personality):
    prompt = f"Age: {age}, Location: {location}, Profession: {profession}, Personality: {personality}"
    result = pipe(prompt, max_length=64, do_sample=True)
    return result[0]['generated_text']
