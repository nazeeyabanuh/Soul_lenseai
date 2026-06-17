import { useEffect, useState } from "react";
function Dashboard() {
  const [stats, setStats] = useState(null);
  useEffect(() => {
    async function loadDashboard() {
      const response = await fetch(
        "https://soul-lenseai.onrender.com/dashboard"
      );
      const data = await response.json();
      setStats(data);
    }
    loadDashboard();
  }, []);
  if (!stats) {
    return <h2>Loading Dashboard...</h2>;
  }
  return (
    <div>
      <h1>Dashboard</h1>
      <h2>
        Total Analyses:
        {stats.total_analyses}
      </h2>
      <h2>
        Top Emotion:
        {stats.most_common_emotion}
      </h2>
      <h2>
        Positive:
        {stats.positive_messages}
      </h2>
      <h2>
        Negative:
        {stats.negative_messages}
      </h2>
    </div>
  );
}
export default Dashboard;
