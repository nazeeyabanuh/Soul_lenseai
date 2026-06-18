"""
Soul Lense AI - Pytest Test Suite
Tests all five API endpoints using FastAPI TestClient.
AI service calls are mocked to avoid real API usage during testing.
"""

import json
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ─────────────────────────────────────────
# Mock return values (realistic AI outputs)
# ─────────────────────────────────────────

MOCK_EMOTION_RESPONSE = json.dumps({
    "emotion": "joy",
    "sentiment": "positive",
    "style": "assertive",
    "emotional_need": "Desire for connection and validation.",
    "ai_analysis": "The message reflects a positive emotional state. The tone is warm and engaging.",
    "insight": "Continue expressing emotions openly to maintain healthy communication."
})

MOCK_MANIPULATION_RESPONSE = json.dumps({
    "manipulation_detected": False,
    "types": [],
    "risk_level": "Low",
    "confidence": 0.1,
    "reasoning": "No manipulative patterns detected.",
    "primary_influencer": "Unclear",
    "emotional_tone": "Positive",
    "toxicity_score": 0,
    "escalation_detected": False
})

MOCK_MANIPULATION_DETECTED = json.dumps({
    "manipulation_detected": True,
    "types": ["guilt-tripping"],
    "risk_level": "Medium",
    "confidence": 0.75,
    "reasoning": "Guilt-tripping language detected.",
    "primary_influencer": "Person A",
    "emotional_tone": "Negative",
    "toxicity_score": 4,
    "escalation_detected": False
})

MOCK_ANALYSIS_TEXT = "This conversation shows an imbalanced emotional dynamic. One party appears to dominate the exchange."
MOCK_SUMMARY_TEXT = "The conversation reflects emotional tension between the two parties."


# ─────────────────────────────────────────
# GET /
# ─────────────────────────────────────────

class TestRootEndpoint:

    def test_root_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_running_status(self):
        response = client.get("/")
        data = response.json()
        assert "status" in data
        assert "running" in data["status"].lower()


# ─────────────────────────────────────────
# POST /analyze
# ─────────────────────────────────────────

class TestAnalyzeEndpoint:

    @patch("main.get_ai_response", return_value=MOCK_EMOTION_RESPONSE)
    @patch("main.detect_manipulation_ai", return_value=MOCK_MANIPULATION_RESPONSE)
    def test_analyze_returns_200(self, mock_manip, mock_emotion):
        response = client.post("/analyze", json={"text": "I feel great today!"})
        assert response.status_code == 200

    @patch("main.get_ai_response", return_value=MOCK_EMOTION_RESPONSE)
    @patch("main.detect_manipulation_ai", return_value=MOCK_MANIPULATION_RESPONSE)
    def test_analyze_returns_all_required_fields(self, mock_manip, mock_emotion):
        response = client.post("/analyze", json={"text": "I feel great today!"})
        data = response.json()
        required_fields = [
            "emotion", "sentiment", "style", "emotional_need",
            "psychology", "neuroscience", "ai_analysis", "insight",
            "manipulation_detected", "manipulation_type",
            "risk_level", "manipulation_details"
        ]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

    @patch("main.get_ai_response", return_value=MOCK_EMOTION_RESPONSE)
    @patch("main.detect_manipulation_ai", return_value=MOCK_MANIPULATION_RESPONSE)
    def test_analyze_emotion_is_valid_value(self, mock_manip, mock_emotion):
        response = client.post("/analyze", json={"text": "I feel great today!"})
        data = response.json()
        valid_emotions = ["joy", "sadness", "anger", "fear", "neutral"]
        assert data["emotion"] in valid_emotions

    @patch("main.get_ai_response", return_value=MOCK_EMOTION_RESPONSE)
    @patch("main.detect_manipulation_ai", return_value=MOCK_MANIPULATION_RESPONSE)
    def test_analyze_sentiment_is_valid_value(self, mock_manip, mock_emotion):
        response = client.post("/analyze", json={"text": "I feel great today!"})
        data = response.json()
        assert data["sentiment"] in ["positive", "negative", "neutral"]

    @patch("main.get_ai_response", return_value=MOCK_EMOTION_RESPONSE)
    @patch("main.detect_manipulation_ai", return_value=MOCK_MANIPULATION_RESPONSE)
    def test_analyze_manipulation_details_has_confidence(self, mock_manip, mock_emotion):
        response = client.post("/analyze", json={"text": "I feel great today!"})
        data = response.json()
        assert "confidence" in data["manipulation_details"]
        assert "reasoning" in data["manipulation_details"]

    @patch("main.get_ai_response", side_effect=Exception("AI service down"))
    @patch("main.detect_manipulation_ai", return_value=MOCK_MANIPULATION_RESPONSE)
    def test_analyze_fallback_on_ai_failure(self, mock_manip, mock_emotion):
        """Fallback mechanism: should return neutral defaults when AI fails"""
        response = client.post("/analyze", json={"text": "test fallback"})
        assert response.status_code == 200
        data = response.json()
        assert data["emotion"] == "neutral"
        assert data["sentiment"] == "neutral"

    def test_analyze_rejects_empty_request_body(self):
        response = client.post("/analyze", json={})
        assert response.status_code == 422

    def test_analyze_rejects_missing_text_field(self):
        response = client.post("/analyze", json={"message": "wrong field"})
        assert response.status_code == 422


# ─────────────────────────────────────────
# GET /history
# ─────────────────────────────────────────

class TestHistoryEndpoint:

    def test_history_returns_200(self):
        response = client.get("/history")
        assert response.status_code == 200

    def test_history_returns_list(self):
        response = client.get("/history")
        assert isinstance(response.json(), list)

    @patch("main.get_ai_response", return_value=MOCK_EMOTION_RESPONSE)
    @patch("main.detect_manipulation_ai", return_value=MOCK_MANIPULATION_RESPONSE)
    def test_history_record_has_required_fields(self, mock_manip, mock_emotion):
        """Seed one record then check history fields"""
        client.post("/analyze", json={"text": "Testing history record"})
        response = client.get("/history")
        records = response.json()
        if records:
            record = records[0]
            assert "id" in record
            assert "text" in record
            assert "emotion" in record
            assert "sentiment" in record
            assert "manipulation_type" in record

    def test_history_returns_max_20_records(self):
        response = client.get("/history")
        assert len(response.json()) <= 20


# ─────────────────────────────────────────
# GET /dashboard
# ─────────────────────────────────────────

class TestDashboardEndpoint:

    def test_dashboard_returns_200(self):
        response = client.get("/dashboard")
        assert response.status_code == 200

    def test_dashboard_returns_all_required_fields(self):
        response = client.get("/dashboard")
        data = response.json()
        required_fields = [
            "total_analyses", "emotion_breakdown",
            "manipulation_count", "most_common_emotion",
            "positive_messages", "negative_messages"
        ]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

    def test_dashboard_total_analyses_is_integer(self):
        response = client.get("/dashboard")
        data = response.json()
        assert isinstance(data["total_analyses"], int)
        assert data["total_analyses"] >= 0

    def test_dashboard_emotion_breakdown_is_dict(self):
        response = client.get("/dashboard")
        data = response.json()
        assert isinstance(data["emotion_breakdown"], dict)

    def test_dashboard_counts_are_non_negative(self):
        response = client.get("/dashboard")
        data = response.json()
        assert data["manipulation_count"] >= 0
        assert data["positive_messages"] >= 0
        assert data["negative_messages"] >= 0


# ─────────────────────────────────────────
# POST /relationship
# ─────────────────────────────────────────

class TestRelationshipEndpoint:

    @patch("main.get_ai_response", return_value=MOCK_ANALYSIS_TEXT)
    @patch("main.detect_manipulation_ai", return_value=MOCK_MANIPULATION_RESPONSE)
    def test_relationship_returns_200(self, mock_manip, mock_ai):
        response = client.post("/relationship", json={
            "person_a": "I really need you to help me.",
            "person_b": "Sure, I can help."
        })
        assert response.status_code == 200

    @patch("main.get_ai_response", return_value=MOCK_ANALYSIS_TEXT)
    @patch("main.detect_manipulation_ai", return_value=MOCK_MANIPULATION_RESPONSE)
    def test_relationship_returns_all_required_fields(self, mock_manip, mock_ai):
        response = client.post("/relationship", json={
            "person_a": "You never listen to me.",
            "person_b": "I am always here for you."
        })
        data = response.json()
        required_fields = [
            "analysis", "manipulation_detected", "types",
            "primary_influencer", "emotional_tone", "toxicity_score",
            "confidence", "risk_level", "escalation_detected",
            "reasoning", "person_a", "person_b"
        ]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

    @patch("main.get_ai_response", return_value=MOCK_ANALYSIS_TEXT)
    @patch("main.detect_manipulation_ai", return_value=MOCK_MANIPULATION_RESPONSE)
    def test_relationship_person_a_and_b_have_sub_fields(self, mock_manip, mock_ai):
        response = client.post("/relationship", json={
            "person_a": "You always make me feel bad.",
            "person_b": "I didn't mean to."
        })
        data = response.json()
        assert "manipulation_detected" in data["person_a"]
        assert "type" in data["person_a"]
        assert "reason" in data["person_a"]
        assert "manipulation_detected" in data["person_b"]

    def test_relationship_rejects_missing_person_b(self):
        response = client.post("/relationship", json={"person_a": "Hello"})
        assert response.status_code == 422

    def test_relationship_rejects_empty_body(self):
        response = client.post("/relationship", json={})
        assert response.status_code == 422


# ─────────────────────────────────────────
# POST /conversation-analysis
# ─────────────────────────────────────────

class TestConversationAnalysisEndpoint:

    @patch("main.get_ai_response", return_value=MOCK_SUMMARY_TEXT)
    @patch("main.detect_manipulation_ai", return_value=MOCK_MANIPULATION_RESPONSE)
    def test_conversation_returns_200(self, mock_manip, mock_ai):
        response = client.post("/conversation-analysis", json={
            "conversation": "Person A: Are you okay? Person B: I'm fine."
        })
        assert response.status_code == 200

    @patch("main.get_ai_response", return_value=MOCK_SUMMARY_TEXT)
    @patch("main.detect_manipulation_ai", return_value=MOCK_MANIPULATION_RESPONSE)
    def test_conversation_returns_all_required_fields(self, mock_manip, mock_ai):
        response = client.post("/conversation-analysis", json={
            "conversation": "Person A: I need help. Person B: Always."
        })
        data = response.json()
        required_fields = [
            "conversation_summary", "manipulation_detected", "types",
            "primary_influencer", "emotional_tone", "toxicity_score",
            "confidence", "risk_level", "escalation_detected", "reasoning"
        ]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

    @patch("main.get_ai_response", return_value=MOCK_SUMMARY_TEXT)
    @patch("main.detect_manipulation_ai", return_value=MOCK_MANIPULATION_DETECTED)
    def test_conversation_detects_manipulation_when_present(self, mock_manip, mock_ai):
        response = client.post("/conversation-analysis", json={
            "conversation": "You never care about me. Everything is your fault."
        })
        data = response.json()
        assert data["manipulation_detected"] is True
        assert data["risk_level"] in ["Low", "Medium", "High"]

    @patch("main.get_ai_response", side_effect=Exception("AI unavailable"))
    @patch("main.detect_manipulation_ai", return_value=MOCK_MANIPULATION_RESPONSE)
    def test_conversation_fallback_on_ai_failure(self, mock_manip, mock_ai):
        """Fallback: should still return 200 with default summary"""
        response = client.post("/conversation-analysis", json={
            "conversation": "Test fallback behaviour."
        })
        assert response.status_code == 200
        data = response.json()
        assert "conversation_summary" in data

    def test_conversation_rejects_empty_body(self):
        response = client.post("/conversation-analysis", json={})
        assert response.status_code == 422