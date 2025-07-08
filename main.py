
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gradio_client import Client
import uvicorn

# Define the request body format
class UserInput(BaseModel):
    age: str
    location: str
    profession: str
    personality: str

# Initialize FastAPI app
app = FastAPI()

# Load the Hugging Face Space
client = Client("bp7274/archetype-model")

@app.post("/")
async def generate_quote(data: UserInput):
    try:
        # Send prediction request to Hugging Face Space
        result = client.predict(
            data.age,
            data.location,
            data.profession,
            data.personality
        )
        return {"quote": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional: for local dev testing
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



