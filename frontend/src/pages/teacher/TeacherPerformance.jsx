import { useEffect, useState } from 'react'
import { getTeacherAttempts } from '../../services/teacherService.js'

export default function TeacherPerformance() {
  const [rows, setRows] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    getTeacherAttempts().then(setRows).catch((e) => setError(e.message))
  }, [])

  if (error) return <div className="alert">{error}</div>

  const avg = rows.length ? Math.round(rows.reduce((s, r) => s + r.percentage, 0) / rows.length) : 0

  return (
    <div className="page">
      <div className="panel">
        <div className="panel-head">
          <h3>Quiz Attempts Across All Students ({rows.length})</h3>
          <span className="chip">Average {avg}%</span>
        </div>
        <table className="table">
          <thead>
            <tr><th>Student</th><th>Lesson</th><th>Score</th><th>Attempt</th><th>Time</th><th>Date</th></tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.id}>
                <td><strong>{r.student}</strong></td>
                <td>{r.lesson}</td>
                <td>
                  <strong className={r.percentage >= 70 ? 'good' : r.percentage >= 50 ? 'ok' : 'bad'}>
                    {Math.round(r.percentage)}%
                  </strong>
                </td>
                <td>#{r.attempt_number}</td>
                <td>{Math.floor(r.time_taken / 60)}m {r.time_taken % 60}s</td>
                <td className="muted">{r.created_at?.slice(0, 16).replace('T', ' ')}</td>
              </tr>
            ))}
            {rows.length === 0 && <tr><td colSpan={6} className="muted">No attempts yet.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  )
}
