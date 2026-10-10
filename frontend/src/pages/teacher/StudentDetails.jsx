import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import Card from '../../components/Card.jsx'
import ProgressBar from '../../components/ProgressBar.jsx'
import { getStudentDetails } from '../../services/teacherService.js'
import { formatLabel } from '../../services/format.js'

export default function StudentDetails() {
  const { studentId } = useParams()
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    getStudentDetails(studentId).then(setData).catch((e) => setError(e.message))
  }, [studentId])

  if (error) return <div className="alert">{error}</div>
  if (!data) return <div className="loading">Loading student...</div>

  const rec = data.current_recommendation

  return (
    <div className="page">
      <Link className="back-link" to="/teacher/students">← All students</Link>

      <div className="panel student-head">
        <div className="avatar big">{data.name[0]}</div>
        <div>
          <h2>{data.name}</h2>
          <span className="muted">{data.email}{data.age ? ` · ${data.age} years` : ''} · prefers {data.preferred_format}</span>
        </div>
      </div>

      <section className="stat-grid">
        <Card label="Overall Score" value={`${Math.round(data.overall_score)}%`} accent="blue" />
        <Card label="Progress" value={`${Math.round(data.progress)}%`} accent="green" />
        <Card label="Attempts" value={data.attempts} accent="purple" />
        <Card label="Average Time" value={`${data.avg_time_minutes} min`} />
      </section>

      <section className="grid-2">
        <div className="panel">
          <h3>Recent Performance</h3>
          <table className="table">
            <thead>
              <tr><th>Lesson</th><th>Score</th><th>Attempts</th></tr>
            </thead>
            <tbody>
              {data.recent_performance.map((item, i) => (
                <tr key={i}>
                  <td>{item.lesson}</td>
                  <td>
                    <strong className={item.percentage >= 70 ? 'good' : item.percentage >= 50 ? 'ok' : 'bad'}>
                      {Math.round(item.percentage)}%
                    </strong>
                  </td>
                  <td>{item.attempts}</td>
                </tr>
              ))}
              {data.recent_performance.length === 0 && (
                <tr><td colSpan={3} className="muted">No attempts yet.</td></tr>
              )}
            </tbody>
          </table>
          <h3 className="mt">Progress</h3>
          <ProgressBar value={data.progress} label="Overall learning progress" />
        </div>

        <div className="panel">
          <h3>Current Recommendation</h3>
          {rec ? (
            <div className="rec-card static">
              <div className="rec-top">
                <div>
                  <span className="rec-kicker">Suggested format</span>
                  <h3>{rec.recommended_format_label}</h3>
                </div>
                <div className="confidence">
                  <strong>{Math.round(rec.confidence * 100)}%</strong>
                  <small>confidence</small>
                </div>
              </div>
              <p className="rec-reason">
                <strong>Why:</strong> {rec.reason}
              </p>
              <div className="rec-meta">
                <span>Learning need: <strong>{rec.difficulty}</strong></span>
                {rec.lesson_title && <span>Lesson: <strong>{rec.lesson_title}</strong></span>}
              </div>
            </div>
          ) : (
            <p className="muted">No recommendation generated yet.</p>
          )}

          <h3 className="mt">Recommendation History</h3>
          <ul className="perf-list">
            {data.history.map((item) => (
              <li key={item.id}>
                <div>
                  <strong>{item.recommended_format_label}</strong>
                  <span className="muted"> · {item.lesson_title || 'General'}</span>
                  <div className="muted small">{item.reason}</div>
                </div>
                <span className="chip">{item.difficulty}</span>
              </li>
            ))}
            {data.history.length === 0 && <li className="muted">No history.</li>}
          </ul>
        </div>
      </section>
    </div>
  )
}
