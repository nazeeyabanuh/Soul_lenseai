function ResultCard({ title, value }) {
  return (
    <div className="result-card">
      <h3>{title}</h3>
      <h2>{value}</h2>
    </div>
  );
}

export default ResultCard;