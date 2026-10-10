import { Link } from 'react-router-dom'
import { formatLabel } from '../services/format.js'

export default function RecommendationCard({ rec, compact = false }) {
  if (!rec) {
    return (
      <div className="rec-card empty">
        <h3>Personalized Recommendation</h3>
        <p>Take a quiz and SmartAssist will analyze your performance to recommend the best learning format.</p>
        <Link className="primary-btn" to="/subjects">Start Learning</Link>
      </div>
    )
  }
  const confidence = Math.round((rec.confidence || 0) * 100)
  return (
    <div className={`rec-card ${compact ? 'compact' : ''}`}>
      <div className="rec-top">
        <div>
          <span className="rec-kicker">Recommended for you</span>
          <h3>{rec.recommended_format_label || formatLabel(rec.recommended_format)}</h3>
        </div>
        <div className="confidence">
          <strong>{confidence}%</strong>
          <small>confidence</small>
        </div>
      </div>
      <p className="rec-reason">
        <strong>Why this recommendation?</strong>
        {rec.reason}
      </p>
      {!compact && (
        <div className="rec-meta">
          <span>Learning need: <strong>{rec.difficulty}</strong></span>
          {rec.lesson_title && <span>Lesson: <strong>{rec.lesson_title}</strong></span>}
        </div>
      )}
      <div className="rec-actions">
        <Link className="primary-btn" to="/recommendations">View Recommendation</Link>
        {rec.lesson_id && (
          <Link className="ghost-btn" to={`/lessons/${rec.lesson_id}`}>Start Recommended Lesson</Link>
        )}
      </div>
    </div>
  )
}
