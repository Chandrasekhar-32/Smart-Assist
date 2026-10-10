export default function Card({ label, value, hint, accent }) {
  return (
    <div className={`card stat-card ${accent ? `accent-${accent}` : ''}`}>
      <span className="stat-label">{label}</span>
      <strong className="stat-value">{value}</strong>
      {hint && <small className="stat-hint">{hint}</small>}
    </div>
  )
}
