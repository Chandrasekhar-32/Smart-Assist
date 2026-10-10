import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getLatestRecommendation, getRecommendations } from '../../services/recommendationService.js'
import { getProgress } from '../../services/lessonService.js'
import { formatLabel } from '../../services/format.js'

export default function Recommendation() {
  const [rec, setRec] = useState(null)
  const [history, setHistory] = useState([])
  const [progress, setProgress] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    getLatestRecommendation().then(setRec).catch((e) => setError(e.message))
    getRecommendations().then(setHistory).catch(() => {})
    getProgress().then(setProgress).catch(() => {})
  }, [])

  if (error) return <div className="alert">{error}</div>
  if (!rec) {
    return (
      <div className="page">
        <div className="panel empty-state">
          <h3>No recommendations yet</h3>
          <p>Complete a quiz and SmartAssist will analyze your performance.</p>
          <Link className="primary-btn" to="/subjects">Start Learning</Link>
        </div>
      </div>
    )
  }

  const confidence = Math.round((rec.confidence || 0) * 100)
  const previous = rec.previous_performance ?? progress?.average_score ?? 0

  return (
    <div className="page">
      <div className="panel rec-hero">
        <span className="rec-kicker">Personalized Recommendation</span>
        <div className="rec-hero-grid">
          <div>
            <h2>{formatLabel(rec.recommended_format)}</h2>
            <span className="chip big">{rec.difficulty} learning need</span>
          </div>
          <div className="confidence big">
            <strong>{confidence}%</strong>
            <small>model confidence</small>
          </div>
        </div>

        <div className="why-box">
          <h4>Why this recommendation?</h4>
          <p>{rec.reason}</p>
          <p className="muted">
            Therefore, SmartAssist recommends {formatLabel(rec.recommended_format).toLowerCase()} before
            attempting the quiz again.
          </p>
        </div>

        <div className="target-grid">
          <div>
            <span>Previous Performance</span>
            <strong>{Math.round(previous)}%</strong>
          </div>
          <div>
            <span>Target</span>
            <strong>70%+</strong>
          </div>
          {rec.lesson_title && (
            <div>
              <span>For lesson</span>
              <strong>{rec.lesson_title}</strong>
            </div>
          )}
        </div>

        <div className="result-actions">
          {rec.lesson_id && (
            <Link className="primary-btn" to={`/lessons/${rec.lesson_id}`}>Start Recommended Lesson</Link>
          )}
          <Link className="ghost-btn" to="/subjects">Browse Subjects</Link>
        </div>
      </div>

      <div className="panel">
        <h3>Recommendation History</h3>
        {history.length === 0 && <p className="muted">No previous recommendations.</p>}
        <ul className="perf-list">
          {history.map((item) => (
            <li key={item.id}>
              <div>
                <strong>{item.recommended_format_label}</strong>
                <span className="muted"> {item.lesson_title ? `· ${item.lesson_title}` : ''} · {item.difficulty}</span>
              </div>
              <span className="muted small">{item.created_at?.slice(0, 16).replace('T', ' ')}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
