import { useState } from "react";

function Relationship() {

  const [personA, setPersonA] = useState("");
  const [personB, setPersonB] = useState("");
  const [conversation, setConversation] = useState("");

  const [result, setResult] = useState(null);

  async function analyzeRelationship() {

    const response = await fetch(
      "http://127.0.0.1:8000/relationship",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          person_a: personA,
          person_b: personB
        })
      }
    );

    const data = await response.json();

    setResult(data);
  }

  async function analyzeFullConversation() {
    const response = await fetch("http://127.0.0.1:8000/conversation-analysis", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ conversation }),
    });

    const data = await response.json();
    setResult(data);
  }

  return (
    <div>

      <h1>Relationship Analysis</h1>

      <textarea
        placeholder="Person A"
        value={personA}
        onChange={(e) =>
          setPersonA(e.target.value)
        }
      />

      <br /><br />

      <textarea
        placeholder="Person B"
        value={personB}
        onChange={(e) =>
          setPersonB(e.target.value)
        }
      />

      <br /><br />

      <button onClick={analyzeRelationship}>Analyze Relationship</button>

      <br /><br />

      <h2>Full Conversation Context</h2>
      <textarea
        placeholder="Paste a full chat exchange here, for example: Person A: ...\nPerson B: ..."
        value={conversation}
        onChange={(e) => setConversation(e.target.value)}
      />

      <button onClick={analyzeFullConversation}>Analyze Full Conversation</button>

      {result && (
        <div style={{marginTop:"20px"}} className="result-card">
          <h2>Relationship Result</h2>
          {result.analysis && <p>{result.analysis}</p>}
          {result.conversation_summary && <p><strong>Summary:</strong> {result.conversation_summary}</p>}
          <p><strong>Manipulation detected:</strong> {result.manipulation_detected ? "Yes" : "No"}</p>
          <p><strong>Types:</strong> {Array.isArray(result.types) && result.types.length ? result.types.join(", ") : "None"}</p>
          <p><strong>Primary influencer:</strong> {result.primary_influencer || "Unclear"}</p>
          <p><strong>Emotional tone:</strong> {result.emotional_tone || "Neutral"}</p>
          <p><strong>Toxicity score:</strong> {result.toxicity_score ?? 0}/100</p>
          <p><strong>Confidence:</strong> {result.confidence ?? "N/A"}</p>
          <p><strong>Risk level:</strong> {result.risk_level || "Low"}</p>
          <p><strong>Escalation detected:</strong> {result.escalation_detected ? "Yes" : "No"}</p>
          <p><strong>Reasoning:</strong> {result.reasoning || "No additional reasoning was provided."}</p>
          {result.key_patterns && Array.isArray(result.key_patterns) && (
            <ul>
              {result.key_patterns.map((item, idx) => <li key={idx}>{item}</li>)}
            </ul>
          )}
          {result.person_a && <p><strong>Person A detection:</strong> {result.person_a.manipulation_detected ? `${result.person_a.type || "Manipulation"} (${result.person_a.reason || "Detected"})` : "No clear manipulation pattern detected."}</p>}
          {result.person_b && <p><strong>Person B detection:</strong> {result.person_b.manipulation_detected ? `${result.person_b.type || "Manipulation"} (${result.person_b.reason || "Detected"})` : "No clear manipulation pattern detected."}</p>}
          {result.psychology && <p><strong>Psychology:</strong> {result.psychology}</p>}
          {result.neuroscience && <p><strong>Neuroscience:</strong> {result.neuroscience}</p>}
          {result.emotional_need && <p><strong>Emotional need:</strong> {result.emotional_need}</p>}
        </div>
      )}

    </div>
  );
}

export default Relationship;