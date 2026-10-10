import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import Card from '../../components/Card.jsx'
import ProgressBar from '../../components/ProgressBar.jsx'
import RecommendationCard from '../../components/RecommendationCard.jsx'
import { getDashboard } from '../../services/lessonService.js'

export default function StudentDashboard() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    getDashboard().then(setData).catch((e) => setError(e.message))
  }, [])

  if (error) return <div className="alert">{error}</div>
  if (!data) return <div className="loading">Loading dashboard...</div>

  return (
    <div className="page">
      <section className="welcome">
        <div>
          <h2>Welcome, {data.welcome_name} 👋</h2>
          <p>Your Learning Overview</p>
        </div>
        <Link className="ghost-btn" to="/progress">View full progress</Link>
      </section>

      <section className="stat-grid">
        <Card label="Lessons Completed" value={`${data.lessons_completed} / ${data.total_lessons}`} />
        <Card label="Average Score" value={`${Math.round(data.average_score)}%`} accent="blue" />
        <Card label="Progress" value={`${Math.round(data.progress)}%`} accent="green" />
        <Card label="Quiz Attempts" value={data.quiz_attempts} hint={data.improvement > 0 ? `Improvement +${data.improvement}%` : ''} accent="purple" />
      </section>

      <section className="grid-2">
        <div className="panel">
          <h3>Continue Learning</h3>
          {data.continue_learning && (
            <div className="continue-card">
              <div>
                <strong>{data.continue_learning.title}</strong>
                <span className="muted">{data.continue_learning.subject}</span>
              </div>
              <ProgressBar value={data.continue_learning.progress} label="Progress" />
              <Link className="primary-btn" to={`/lessons/${data.continue_learning.id}`}>Continue</Link>
            </div>
          )}
          <h3 className="mt">Recent Performance</h3>
          {data.recent_performance.length === 0 && <p className="muted">No quizzes yet.</p>}
          <ul className="perf-list">
            {data.recent_performance.map((item, i) => (
              <li key={i}>
                <span>{item.lesson}</span>
                <strong className={item.percentage >= 70 ? 'good' : item.percentage >= 50 ? 'ok' : 'bad'}>
                  {Math.round(item.percentage)}%
                </strong>
              </li>
            ))}
          </ul>
        </div>

        <div className="panel">
          <h3>Recommended For You</h3>
          <RecommendationCard rec={data.recommendation} compact />
          <h3 className="mt">Learning Progress</h3>
          <div className="progress-list">
            {data.subject_progress.map((s) => (
              <ProgressBar key={s.subject} value={s.progress} label={s.subject} />
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
