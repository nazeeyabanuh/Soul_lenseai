import { useState } from "react";
import "../App.css";

function Home() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function analyzeEmotion() {
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error("Unable to analyze text right now.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong.");
      setResult(null);
    }
  }

  return (
    <div>

      <h1 className="page-title">
        Emotion Analysis
      </h1>

      <textarea
        placeholder="Type your thoughts..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <br />
      <br />

      <button onClick={analyzeEmotion}>
        Analyze Emotion
      </button>

      {error && <p className="error-text">{error}</p>}

      {result && (
        <div className="result-card">

          <h2>
            Emotion: {result.emotion}
          </h2>

          <p>
            Sentiment: {result.sentiment}
          </p>

          <p>
            Style: {result.style}
          </p>

          <p>
            Need: {result.emotional_need}
          </p>

          <p>
            Psychology: {result.psychology}
          </p>

          <p>
            Neuroscience: {result.neuroscience}
          </p>

          <p>
            Manipulation detected: {result.manipulation_detected ? "Yes" : "No"}
          </p>

          <p>
            Manipulation types: {result.manipulation_type || "None"}
          </p>

          <p>
            Risk level: {result.risk_level || "Low"}
          </p>

          <p>
            Manipulation confidence: {result.manipulation_details?.confidence ?? "0"}
          </p>

          <p>
            Manipulation reasoning: {result.manipulation_details?.reasoning || "No specific manipulation cues were detected."}
          </p>

          <p>
            AI analysis: {result.ai_analysis}
          </p>

          <p>
            Insight: {result.insight}
          </p>

        </div>
      )}

    </div>
  );
}

export default Home;