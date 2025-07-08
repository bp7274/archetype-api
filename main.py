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
   result = generator(
    prompt,
    max_new_tokens=60,
    do_sample=True,
    temperature=0.8,  # controls creativity
    top_p=0.9         # nucleus sampling
)[0]['generated_text']

    
    return {"quote": result}


