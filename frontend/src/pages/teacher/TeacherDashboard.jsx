import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import Card from '../../components/Card.jsx'
import { getTeacherDashboard, getTeacherRecommendations } from '../../services/teacherService.js'

export default function TeacherDashboard() {
  const [data, setData] = useState(null)
  const [recs, setRecs] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    getTeacherDashboard().then(setData).catch((e) => setError(e.message))
    getTeacherRecommendations().then(setRecs).catch(() => {})
  }, [])

  if (error) return <div className="alert">{error}</div>
  if (!data) return <div className="loading">Loading dashboard...</div>

  return (
    <div className="page">
      <section className="stat-grid">
        <Card label="Total Students" value={data.total_students} />
        <Card label="Average Score" value={`${Math.round(data.average_score)}%`} accent="blue" />
        <Card label="Students Needing Support" value={data.needing_support} accent="red" />
        <Card label="Recommendations Generated" value={data.recommendations_generated} accent="purple" />
      </section>

      <section className="grid-2">
        <div className="panel">
          <div className="panel-head">
            <h3>Student Performance</h3>
            <Link className="ghost-btn small" to="/teacher/students">View all</Link>
          </div>
          <table className="table">
            <thead>
              <tr><th>Student</th><th>Avg Score</th><th>Progress</th><th>Status</th></tr>
            </thead>
            <tbody>
              {data.students.map((s) => (
                <tr key={s.id} className="clickable" onClick={() => (window.location.href = `/teacher/students/${s.id}`)}>
                  <td><strong>{s.name}</strong></td>
                  <td>{Math.round(s.avg_score)}%</td>
                  <td>{Math.round(s.progress)}%</td>
                  <td>
                    <span className={`status ${s.status === 'Good' ? 'good' : s.status === 'Average' ? 'ok' : 'bad'}`}>
                      {s.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="panel">
          <div className="panel-head">
            <h3>Latest Recommendations</h3>
            <Link className="ghost-btn small" to="/teacher/recommendations">View all</Link>
          </div>
          <ul className="perf-list">
            {recs.slice(0, 6).map((r) => (
              <li key={r.id}>
                <div>
                  <strong>{r.student_name || 'Student'}</strong>
                  <span className="muted"> → {r.recommended_format_label}</span>
                  <div className="muted small">{r.lesson_title || ''}</div>
                </div>
                <span className="chip">{Math.round(r.confidence * 100)}%</span>
              </li>
            ))}
            {recs.length === 0 && <li className="muted">No recommendations yet.</li>}
          </ul>
        </div>
      </section>
    </div>
  )
}
