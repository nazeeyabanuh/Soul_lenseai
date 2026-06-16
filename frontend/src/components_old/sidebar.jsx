function Sidebar({ setPage }) {
  return (
    <div className="sidebar">

      <h1>SoulLens AI</h1>

      <button onClick={() => setPage("home")}>
        Analysis
      </button>

      <button onClick={() => setPage("dashboard")}>
        Dashboard
      </button>

      <button onClick={() => setPage("relationship")}>
        Relationship
      </button>

      <button onClick={() => setPage("history")}>
        History
      </button>

    </div>
  );
}

export default Sidebar;