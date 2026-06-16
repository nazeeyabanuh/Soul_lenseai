import json
import google.generativeai as genai
import os

try:
    from genai import generative_ai  # type: ignore[import]
except ImportError:  # pragma: no cover - optional dependency
    generative_ai = None

try:
    from dotenv import load_dotenv  # type: ignore[import]
except ImportError:  # pragma: no cover - optional dependency
    def load_dotenv():
        return False

load_dotenv()

client = genai.configure(api_key=os.getenv("GEMINI_API_KEY")) if os.getenv("GEMINI_API_KEY") else None


MANIPULATION_RULES = {
    "Guilt Tripping": [
        "after everything i did for you", "you owe me", "i sacrificed everything for you", "you never appreciate me",
        "you should do this for me", "do this for me at least once", "you never do this for me", "you should be grateful",
        "i did so much for you", "after all i have done",
    ],
    "Emotional Blackmail": [
        "if you really loved me", "if you leave me i will die", "you will regret this", "do this or i will leave",
        "why whats wrong", "what's wrong with you", "if you stop talking to me i will disappear", "you'll lose me",
    ],
    "Gaslighting": ["you are overreacting", "that never happened", "you imagined it", "it is all in your head", "you always make things up", "you are too sensitive"],
    "Victim Signaling": ["nobody cares", "no one cares", "everyone ignores me", "i always suffer", "i am always alone", "nobody understands me"],
    "Love Bombing": ["i can't live without you", "you are my everything", "i will do anything for you", "you are perfect", "i need you forever", "you complete me"],
    "Emotional Withdrawal / Silent Treatment": ["silent treatment", "ignore me and see", "if you stop talking to me", "don't speak to me", "i'll disappear if you leave"],
    "Obligation Pressure": ["you owe me", "you must do this", "you need to do this", "you have to do this"],
    "Emotional Invalidation": ["you are overreacting", "you are too sensitive", "don't be dramatic", "stop being childish"],
    "Dependency Creation": ["i can't live without you", "you are my everything", "i need you forever", "you complete me"],
}


def _fallback_manipulation_analysis(text: str):
    lowered = text.lower()
    detected_types = []

    for name, phrases in MANIPULATION_RULES.items():
        if any(phrase in lowered for phrase in phrases):
            detected_types.append(name)

    unique_types = list(dict.fromkeys(detected_types))
    count = len(unique_types)
    toxicity_score = 0 if count == 0 else min(100, 40 + (count * 12) + (2 if any(word in lowered for word in ["always", "never", "must", "have to", "you owe me", "if you really loved me"]) else 0))
    risk = "High" if toxicity_score >= 80 or count >= 3 else "Medium" if toxicity_score >= 40 else "Low"
    emotional_tone = "Toxic" if toxicity_score >= 70 else "Negative" if toxicity_score >= 40 else "Healthy"
    escalation = any(word in lowered for word in ["always", "never", "if you really loved me", "you owe me", "i can't live without you", "silent treatment"])
    confidence = round(min(0.98, 0.35 + (count * 0.12) + (0.08 if escalation else 0.0)), 2)
    primary_influencer = "Unclear"

    if "person a:" in lowered and "person b:" in lowered:
        a_hits = sum(1 for phrase in ["you owe me", "if you really loved me", "never", "always", "ignore me", "nobody cares"] if phrase in lowered)
        b_hits = sum(1 for phrase in ["you owe me", "if you really loved me", "never", "always", "ignore me", "nobody cares"] if phrase in lowered)
        if a_hits > b_hits:
            primary_influencer = "Person A"
        elif b_hits > a_hits:
            primary_influencer = "Person B"
        else:
            primary_influencer = "Balanced"

    return {
        "manipulation_detected": bool(unique_types),
        "types": unique_types,
        "primary_influencer": primary_influencer,
        "emotional_tone": emotional_tone,
        "toxicity_score": toxicity_score,
        "risk_level": risk,
        "escalation_detected": escalation,
        "confidence": confidence,
        "reasoning": "Guilt, pressure, or dependency language is present." if unique_types else "No manipulation patterns were detected.",
    }

def get_ai_response(prompt: str):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key not found"

    try:

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        print("GEMINI ERROR:", e)

        return f"Gemini Error: {str(e)}"


def detect_manipulation_ai(text: str):
    fallback = _fallback_manipulation_analysis(text)

    if client is None or not os.getenv("GEMINI_API_KEY"):
        return json.dumps(fallback)

    try:
        prompt = f"""
You are a STRICT psychological manipulation classification engine.

INPUT:
{text}

CRITICAL RULES:
1. Do NOT use soft language.
2. manipulation_detected must be TRUE or FALSE.
3. If any manipulation pattern exists, classification MUST be TRUE.
4. Tone is irrelevant; patterns are everything.

DETECT THESE TYPES:
- Guilt Tripping
- Emotional Blackmail
- Gaslighting
- Victim Signaling
- Love Bombing
- Emotional Withdrawal / Silent Treatment
- Obligation Pressure
- Emotional Invalidation
- Dependency Creation

OUTPUT ONLY VALID JSON:
{{
  "manipulation_detected": true,
  "types": ["Guilt Tripping"],
  "primary_influencer": "Person A / Person B / Balanced / Unclear",
  "emotional_tone": "Healthy / Negative / Toxic / Neutral",
  "toxicity_score": 0,
  "risk_level": "Low / Medium / High",
  "escalation_detected": false,
  "confidence": 0.0,
  "reasoning": "ONE short sentence explaining the main pattern only"
}}
"""

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.content[0].text
        parsed = json.loads(content)

        if isinstance(parsed, dict):
            parsed.setdefault("types", [])
            parsed.setdefault("manipulation_detected", bool(parsed.get("types")))
            parsed.setdefault("primary_influencer", "Unclear")
            parsed.setdefault("emotional_tone", "Neutral")
            parsed.setdefault("toxicity_score", 0)
            parsed.setdefault("risk_level", "Low")
            parsed.setdefault("escalation_detected", False)
            parsed.setdefault("confidence", 0.0)
            parsed.setdefault("reasoning", "Manipulation pattern detected.")
            return json.dumps(parsed)
    except Exception:
        pass

    return json.dumps(fallback)
