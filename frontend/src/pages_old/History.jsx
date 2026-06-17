import { useEffect, useState } from "react";
function History() {
  const [history, setHistory] = useState([]);
  useEffect(() => {
    fetch("https://soul-lenseai.onrender.com/history")
      .then(res => res.json())
      .then(data => setHistory(data));
  }, []);
  return (
    <div>
      <h1>History</h1>
      {history.map(item => (
        <div
          key={item.id}
          className="card"
        >
          <p>{item.text}</p>
          <h3>{item.emotion}</h3>
        </div>
      ))}
    </div>
  );
}
export default History;
