import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the .env file
api_key = os.getenv("DEEPSEEK_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Define the request model
class ChatRequest(BaseModel):
    message: str

# Define the chat endpoint
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # DeepSeek API endpoint
        url = "https://api.deepseek.com/v1"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Prepare the payload
        payload = {
            "model": "deepseek-chat",  # Specify the model
            "messages": [{"role": "user", "content": request.message}]
        }
        
        # Make the API request
        response = requests.post(f"{url}/chat/completions", json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the response
        data = response.json()
        reply = data["choices"][0]["message"]["content"].strip()

        return {"reply": reply}
    except requests.exceptions.RequestException as e:
        return {"reply": f"Request Error: {str(e)}"}
    except KeyError:
        return {"reply": "Error: Unexpected response format from DeepSeek API."}
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}

# Run the app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)