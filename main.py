from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Load your model from Hugging Face
generator = pipeline("text2text-generation", model="bp7274/archetype-model")

app = FastAPI()

# Define expected input structure
class InputData(BaseModel):
    age: str
    location: str
    profession: str
    personality: str

@app.post("/generate")
def generate_quote(data: InputData):
    # Build prompt string from input
    prompt = f"Age: {data.age}, Location: {data.location}, Profession: {data.profession}, Personality: {data.personality}"
    
    # Generate quote
    result = generator(prompt, max_length=100, do_sample=True)[0]['generated_text']
    
    return {"quote": result}


