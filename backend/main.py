from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.ai_service import detect_manipulation_ai, get_ai_response
from database import SessionLocal, engine
from models import Base, Analysis
import json

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

def psychology_insight(emotion):
    insights = {
        "sadness": "May indicate loneliness and unmet emotional needs.",
        "anger": "May indicate frustration or violated boundaries.",
        "fear": "May indicate uncertainty or perceived threat.",
        "joy": "May indicate satisfaction and positive engagement."
    }
    return insights.get(emotion, "Requires deeper analysis.")

def neuroscience_explanation(emotion):
    explanations = {
        "sadness": "Often associated with increased activity in brain regions involved in emotional reflection.",
        "fear": "Often linked to threat detection systems and heightened vigilance.",
        "anger": "Can involve heightened arousal and rapid threat evaluation.",
        "joy": "Often associated with reward and motivation systems."
    }
    return explanations.get(emotion, "Neuroscience explanation unavailable.")

@app.get("/")
def root():
    return {"status": "SoulLense AI backend is running"}

@app.post("/analyze")
def analyze(input: TextInput):
    prompt = "You are an expert emotion analyst. Analyze this message: " + input.text + "\nReturn ONLY valid JSON:\n{\"emotion\": \"joy/sadness/anger/fear/neutral\", \"sentiment\": \"positive/negative/neutral\", \"style\": \"assertive/passive/aggressive\", \"emotional_need\": \"one short sentence\", \"ai_analysis\": \"two sentence analysis\", \"insight\": \"one actionable insight\"}"
    try:
        ai_response = get_ai_response(prompt)
        print("RAW AI RESPONSE:", ai_response)
        cleaned_response = ai_response.strip()
        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response.split("```")[1]
            if cleaned_response.startswith("json"):
                cleaned_response = cleaned_response[4:]
        emotion_data = json.loads(cleaned_response.strip())
    except Exception as e:
        print("EMOTION PARSE ERROR:", str(e))

    manipulation_raw = detect_manipulation_ai(input.text)
    manipulation = json.loads(manipulation_raw)
    emotion = emotion_data.get("emotion", "neutral")

    result = {
        "emotion": emotion,
        "sentiment": emotion_data.get("sentiment", ""),
        "style": emotion_data.get("style", ""),
        "emotional_need": emotion_data.get("emotional_need", ""),
        "psychology": psychology_insight(emotion),
        "neuroscience": neuroscience_explanation(emotion),
        "ai_analysis": emotion_data.get("ai_analysis", ""),
        "insight": emotion_data.get("insight", ""),
        "manipulation_detected": manipulation.get("manipulation_detected", False),
        "manipulation_type": ", ".join(manipulation.get("types", [])),
        "risk_level": manipulation.get("risk_level", "Low"),
        "manipulation_details": {"confidence": manipulation.get("confidence", 0), "reasoning": manipulation.get("reasoning", "")}
    }

    db = SessionLocal()
    try:
        record = Analysis(text=input.text, emotion=result["emotion"], sentiment=result["sentiment"], manipulation_type=result["manipulation_type"])
        db.add(record)
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

    return result

@app.get("/history")
def get_history():
    db = SessionLocal()
    try:
        records = db.query(Analysis).order_by(Analysis.id.desc()).limit(20).all()
        return [{"id": r.id, "text": r.text, "emotion": r.emotion, "sentiment": r.sentiment, "manipulation_type": r.manipulation_type} for r in records]
    finally:
        db.close()

@app.get("/dashboard")
def get_dashboard():
    db = SessionLocal()
    try:
        records = db.query(Analysis).all()
        total = len(records)
        emotions = {}
        manipulation_count = 0
        for r in records:
            emotions[r.emotion] = emotions.get(r.emotion, 0) + 1
            if r.manipulation_type and r.manipulation_type != "None":
                manipulation_count += 1
        return {"total_analyses": total, "emotion_breakdown": emotions, "manipulation_count": manipulation_count}
    finally:
        db.close()
