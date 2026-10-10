import { useEffect, useMemo } from 'react'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import ProgressBar from '../../components/ProgressBar.jsx'
import { getMyLessons } from '../../services/lessonService.js'

export default function MyLearning() {
  const [lessons, setLessons] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    getMyLessons().then(setLessons).catch((e) => setError(e.message))
  }, [])

  const grouped = useMemo(() => {
    const map = {}
    lessons.forEach((l) => {
      const key = l.subject_name || 'Other'
      ;(map[key] = map[key] || []).push(l)
    })
    return map
  }, [lessons])

  if (error) return <div className="alert">{error}</div>

  return (
    <div className="page">
      {Object.keys(grouped).length === 0 && <div className="loading">Loading...</div>}
      {Object.entries(grouped).map(([subject, rows]) => (
        <div className="panel" key={subject}>
          <h3>{subject}</h3>
          <div className="lesson-list">
            {rows.map((lesson) => (
              <div className="lesson-card" key={lesson.id}>
                <div className="lesson-main">
                  <div className="lesson-title-row">
                    <strong>{lesson.title}</strong>
                    <span className={`badge ${lesson.difficulty.toLowerCase()}`}>{lesson.difficulty}</span>
                    <span className={`chip ${lesson.status === 'Completed' ? 'done' : ''}`}>{lesson.status}</span>
                  </div>
                  <ProgressBar value={lesson.progress} />
                </div>
                <Link className="ghost-btn" to={`/lessons/${lesson.id}`}>
                  {lesson.status === 'Not Started' ? 'Start' : 'Open'}
                </Link>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
