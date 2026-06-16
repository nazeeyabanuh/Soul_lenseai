import { useState } from "react";
import "./App.css";
import Home from "./pages_old/home";
import Dashboard from "./pages_old/Dashboard";
import History from "./pages_old/History";
import Relationship from "./pages_old/Relationship";

function App() {
  const [page, setPage] = useState("analysis");

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <p className="eyebrow">Soul Lense AI</p>
          <h1 className="logo">MindView</h1>
          <p className="subtle">Track emotional insights and relationship patterns in one place.</p>
        </div>

        <nav className="nav-stack">
          <button className={page === "analysis" ? "nav-btn active" : "nav-btn"} onClick={() => setPage("analysis")}>Analysis</button>
          <button className={page === "dashboard" ? "nav-btn active" : "nav-btn"} onClick={() => setPage("dashboard")}>Dashboard</button>
          <button className={page === "history" ? "nav-btn active" : "nav-btn"} onClick={() => setPage("history")}>History</button>
          <button className={page === "relationship" ? "nav-btn active" : "nav-btn"} onClick={() => setPage("relationship")}>Relationship</button>
        </nav>
      </aside>

      <main className="main-panel">
        {page === "analysis" && <Home />}
        {page === "dashboard" && <Dashboard />}
        {page === "history" && <History />}
        {page === "relationship" && <Relationship />}
      </main>
    </div>
  );
}

export default App;