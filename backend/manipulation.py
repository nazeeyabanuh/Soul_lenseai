from .utils import get_ai_response # pyright: ignore[reportMissingImports]


def detect_manipulation(text):
    prompt = f"""

You are an expert psychologist.

Analyze this message:

{text}

Determine:

1. Is manipulation present?
2. Manipulation type
3. Risk level
4. Short explanation

Possible types:

* Emotional Blackmail
* Guilt Tripping
* Victim Signaling
* Gaslighting
* Love Bombing
* Blame Shifting
* Emotional Invalidation
* Silent Treatment
* Dependency Creation
* Obligation Pressure
* None

Return ONLY valid JSON:

{{
"manipulation": true,
"type": "Blame Shifting",
"risk": "Medium",
"reason": "The speaker shifts responsibility onto the other person."
}}
"""

    try:
        response = get_ai_response(prompt)

        import json
        result = json.loads(response)

        return result

    except Exception:
        return {
            "manipulation": False,
            "type": "Unknown",
            "risk": "Low",
            "reason": "Could not analyze."
        }

