export default function ProgressBar({ value = 0, label, showValue = true }) {
  const v = Math.max(0, Math.min(100, Number(value) || 0))
  return (
    <div className="progress-wrap">
      {(label || showValue) && (
        <div className="progress-head">
          {label && <span>{label}</span>}
          {showValue && <span className="progress-value">{Math.round(v)}%</span>}
        </div>
      )}
      <div className="progress-track">
        <div className={`progress-fill ${v >= 70 ? 'high' : v >= 40 ? 'mid' : 'low'}`}
             style={{ width: `${v}%` }} />
      </div>
    </div>
  )
}
