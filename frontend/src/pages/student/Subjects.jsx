import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import ProgressBar from '../../components/ProgressBar.jsx'
import { getSubjectLessons, getSubjects } from '../../services/lessonService.js'

const DIFFICULTY = { EASY: 'easy', MEDIUM: 'medium', HARD: 'hard' }

export default function Subjects() {
  const { subjectId } = useParams()
  const [subjects, setSubjects] = useState([])
  const [lessons, setLessons] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (subjectId) {
      getSubjectLessons(subjectId).then(setLessons).catch((e) => setError(e.message))
    } else {
      getSubjects().then(setSubjects).catch((e) => setError(e.message))
    }
  }, [subjectId])

  if (error) return <div className="alert">{error}</div>

  if (subjectId && lessons) {
    return (
      <div className="page">
        <Link className="back-link" to="/subjects">← All subjects</Link>
        <div className="page-head">
          <h2>{lessons[0]?.subject_name || 'Subject'}</h2>
          <span className="chip">{lessons.length} lessons</span>
        </div>
        <div className="lesson-list">
          {lessons.map((lesson) => (
            <div className="lesson-card" key={lesson.id}>
              <div className="lesson-main">
                <div className="lesson-title-row">
                  <strong>{lesson.title}</strong>
                  <span className={`badge ${DIFFICULTY[lesson.difficulty]}`}>{lesson.difficulty}</span>
                </div>
                <p className="muted">{lesson.description}</p>
                <ProgressBar value={lesson.progress} label={lesson.status === 'Completed' ? 'Completed' : lesson.status === 'In Progress' ? 'Progress' : 'Not started'} />
              </div>
              <Link className="primary-btn" to={`/lessons/${lesson.id}`}>
                {lesson.status === 'Completed' ? 'Review' : lesson.status === 'In Progress' ? 'Continue' : 'Start'}
              </Link>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="page">
      <div className="page-head">
        <h2>Choose a Subject</h2>
        <span className="muted">3 subjects · 15 lessons</span>
      </div>
      <div className="subject-grid">
        {subjects.map((subject) => (
          <Link className="subject-card" to={`/subjects/${subject.id}`} key={subject.id}>
            <div className="subject-icon">{subject.name[0]}</div>
            <h3>{subject.name}</h3>
            <p className="muted">{subject.description}</p>
            <div className="subject-meta">
              <span className="chip">{subject.lesson_count} lessons</span>
              <span className="chip">{Math.round(subject.progress)}% done</span>
            </div>
            <ProgressBar value={subject.progress} />
          </Link>
        ))}
      </div>
    </div>
  )
}
