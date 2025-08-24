from fastapi import FastAPI
from pydantic import BaseModel
from .utils import call_ollama

app = FastAPI()

class ChatRequest(BaseModel):
    language: str
    message: str

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/chat")
def chat(request: ChatRequest):
    prompt = f"Respond only in {request.language}: {request.message}"
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