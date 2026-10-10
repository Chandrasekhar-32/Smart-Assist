import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getStudents } from '../../services/teacherService.js'

export default function StudentList() {
  const [students, setStudents] = useState([])
  const [error, setError] = useState('')
  const [query, setQuery] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    getStudents().then(setStudents).catch((e) => setError(e.message))
  }, [])

  if (error) return <div className="alert">{error}</div>

  const filtered = students.filter((s) => s.name.toLowerCase().includes(query.toLowerCase()))

  return (
    <div className="page">
      <div className="panel">
        <div className="panel-head">
          <h3>All Students ({filtered.length})</h3>
          <input className="search" placeholder="Search student..." value={query}
                 onChange={(e) => setQuery(e.target.value)} />
        </div>
        <table className="table">
          <thead>
            <tr><th>Student</th><th>Email</th><th>Avg Score</th><th>Progress</th><th>Attempts</th><th>Status</th></tr>
          </thead>
          <tbody>
            {filtered.map((s) => (
              <tr key={s.id} className="clickable" onClick={() => navigate(`/teacher/students/${s.id}`)}>
                <td><strong>{s.name}</strong></td>
                <td className="muted">{s.email}</td>
                <td>{Math.round(s.avg_score)}%</td>
                <td>{Math.round(s.progress)}%</td>
                <td>{s.attempts}</td>
                <td>
                  <span className={`status ${s.status === 'Good' ? 'good' : s.status === 'Average' ? 'ok' : 'bad'}`}>
                    {s.status}
                  </span>
                </td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr><td colSpan={6} className="muted">No students found.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
