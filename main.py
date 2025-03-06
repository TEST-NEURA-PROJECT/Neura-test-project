from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request model
class ChatRequest(BaseModel):
    message: str

# Define the chat endpoint
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response = openai.completions.create(
            model="gpt-3.5-turbo",  # or whichever model you're using
            prompt=request.message,
            max_tokens=150
        )
        # Extract and return the reply from OpenAI
        reply = response.choices[0].text.strip()
        return {"reply": reply}
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}