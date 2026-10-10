import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import { Link } from 'react-router-dom'

export default function QuizResult() {
  const { state } = useLocation()
  const navigate = useNavigate()
  if (!state) return <Navigate to="/dashboard" replace />

  const minutes = Math.floor(state.time_taken / 60)
  const seconds = state.time_taken % 60
  const rec = state.recommendation

  return (
    <div className="page narrow">
      <div className="panel result-panel">
        <div className="result-check">✓</div>
        <h2>Quiz Completed</h2>

        <div className="score-ring">
          <strong>{state.percentage}%</strong>
          <span>{state.score} / {state.total}</span>
        </div>

        <div className="result-meta">
          <div><span>Time Taken</span><strong>{minutes}m {seconds}s</strong></div>
          <div><span>Attempts</span><strong>{state.attempt_number}</strong></div>
          <div><span>Performance</span>
            <strong className={state.percentage >= 70 ? 'good' : state.percentage >= 50 ? 'ok' : 'bad'}>
              {state.performance}
            </strong>
          </div>
        </div>

        {state.improved && (
          <div className="alert success">
            🎉 Improvement detected: {Math.round(state.previous_percentage)}% → {Math.round(state.percentage)}%
          </div>
        )}
        {!state.improved && state.previous_percentage != null && (
          <div className="alert">
            Previous attempt: {Math.round(state.previous_percentage)}% · Target: 70%+
          </div>
        )}
        {state.previous_percentage == null && (
          <div className="alert">First attempt recorded. Target: 70%+</div>
        )}

        {rec && (
          <div className="rec-banner inline">
            <div>
              <strong>SmartAssist recommends: {rec.recommended_format_label}</strong>
              <p>{rec.reason}</p>
            </div>
          </div>
        )}

        <div className="result-actions">
          <Link className="primary-btn" to="/recommendations">View Recommendation</Link>
          <button className="ghost-btn" onClick={() => navigate(`/lessons/${state.lesson_id}`)}>
            Continue Learning
          </button>
        </div>
      </div>
    </div>
  )
}
