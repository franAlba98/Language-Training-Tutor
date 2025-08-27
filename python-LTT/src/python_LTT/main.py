from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import call_ollama

app = FastAPI()
last_message = {}  # Temporary in-memory store for last prompt

class ChatRequest(BaseModel):
    language: str
    message: str

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/chat")
def chat(request: ChatRequest, user_id: str = "default"):
    prompt = f"Respond only in {request.language}: {request.message}"
    last_message[user_id] = prompt
    response = call_ollama(prompt)
    return {"response": response}

class CorrectRequest(BaseModel):
    text: str
    language: str = "Spanish"

@app.post("/correct")
def correct(request: CorrectRequest):
    prompt = f"Detect grammar mistakes in this {request.language} text and suggest corrections: {request.text}"
    response = call_ollama(prompt)
    return {"corrections": response}

class VocabRequest(BaseModel):
    word: str
    language: str = "Spanish"

@app.post("/vocab")
def vocab(request: VocabRequest):
    prompt = f"Provide synonyms and related words for '{request.word}' in {request.language}"
    response = call_ollama(prompt)
    return {"suggestions": response}

class LevelRequest(BaseModel):
    conversation: str

@app.post("/level")
def level(request: LevelRequest):
    prompt = f"Classify the user's language level as beginner, intermediate, or advanced based on this conversation: {request.conversation}"
    response = call_ollama(prompt)
    return {"level": response}

@app.post("/regenerate")
def regenerate(user_id: str = "default"):
    if user_id not in last_message:
        raise HTTPException(status_code=404, detail="No previous message")
    response = call_ollama(last_message[user_id])
    return {"response": response}


class FeedbackRequest(BaseModel):
    conversation_id: str
    rating: int

@app.post("/feedback")
def feedback(request: FeedbackRequest):
    with open("feedback.log", "a") as f:
        f.write(f"{request.conversation_id},{request.rating}\n")
    return {"status": "recorded"}

class RefineRequest(BaseModel):
    original_response: str
    tweak_prompt: str

@app.post("/refine")
def refine(request: RefineRequest):
    prompt = f"Refine this response based on: {request.tweak_prompt}. Original: {request.original_response}"
    response = call_ollama(prompt)
    return {"refined": response}