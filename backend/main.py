from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.ai_service import detect_manipulation_ai
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

class TextInput(BaseModel):
    text: str

@app.get('/')
def root():
    return {'status': 'SoulLense AI backend is running'}

@app.post('/analyze')
def analyze(input: TextInput):
    result = detect_manipulation_ai(input.text)
    return json.loads(result)

