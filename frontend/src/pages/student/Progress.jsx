import { useEffect, useState } from 'react'
import Card from '../../components/Card.jsx'
import ProgressBar from '../../components/ProgressBar.jsx'
import { getProgress } from '../../services/lessonService.js'

export default function Progress() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    getProgress().then(setData).catch((e) => setError(e.message))
  }, [])

  if (error) return <div className="alert">{error}</div>
  if (!data) return <div className="loading">Loading progress...</div>

  return (
    <div className="page">
      <section className="stat-grid five">
        <Card label="Overall Progress" value={`${Math.round(data.overall_progress)}%`} accent="green" />
        <Card label="Average Score" value={`${Math.round(data.average_score)}%`} accent="blue" />
        <Card label="Lessons Completed" value={`${data.lessons_completed} / ${data.total_lessons}`} />
        <Card label="Quiz Attempts" value={data.quiz_attempts} accent="purple" />
        <Card label="Learning Improvement"
              value={`${data.improvement > 0 ? '+' : ''}${data.improvement}%`}
              accent={data.improvement > 0 ? 'green' : 'red'} />
      </section>

      <section className="grid-2">
        <div className="panel">
          <h3>Subject-wise Progress</h3>
          <div className="progress-list big">
            {data.subject_progress.map((s) => (
              <ProgressBar key={s.subject} value={s.progress} label={s.subject} />
            ))}
          </div>
        </div>
        <div className="panel">
          <h3>Recent Quiz Performance</h3>
          <table className="table">
            <thead>
              <tr><th>Quiz</th><th>Score</th></tr>
            </thead>
            <tbody>
              {data.recent_quizzes.map((q, i) => (
                <tr key={i}>
                  <td>{q.quiz}</td>
                  <td>
                    <strong className={q.percentage >= 70 ? 'good' : q.percentage >= 50 ? 'ok' : 'bad'}>
                      {Math.round(q.percentage)}%
                    </strong>
                  </td>
                </tr>
              ))}
              {data.recent_quizzes.length === 0 && (
                <tr><td colSpan={2} className="muted">No quizzes yet.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}
