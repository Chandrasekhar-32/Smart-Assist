import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import ProgressBar from '../../components/ProgressBar.jsx'
import { getLesson, markViewed } from '../../services/lessonService.js'
import { formatLabel } from '../../services/format.js'

const ORDER = ['TEXT', 'SIMPLIFIED_TEXT', 'VISUAL', 'AUDIO', 'SHORT_LESSON']
const SHORT_LABELS = {
  TEXT: 'Normal Text', SIMPLIFIED_TEXT: 'Simplified', VISUAL: 'Visual',
  AUDIO: 'Audio', SHORT_LESSON: 'Short Lesson',
}

export default function Lesson() {
  const { lessonId } = useParams()
  const navigate = useNavigate()
  const [lesson, setLesson] = useState(null)
  const [active, setActive] = useState('TEXT')
  const [error, setError] = useState('')
  const [speaking, setSpeaking] = useState(false)

  useEffect(() => {
    setError('')
    getLesson(lessonId)
      .then((data) => {
        setLesson(data)
        const rec = data.recommended_resource
        setActive(rec && ORDER.includes(rec.recommended_format) ? rec.recommended_format : 'TEXT')
        markViewed(lessonId).catch(() => {})
      })
      .catch((e) => setError(e.message))
  }, [lessonId])

  const resource = useMemo(
    () => lesson?.resources?.find((r) => r.type === active) || lesson?.resources?.[0],
    [lesson, active],
  )
  const rec = lesson?.recommended_resource

  const speak = () => {
    if (!('speechSynthesis' in window) || !resource) return
    if (speaking) {
      window.speechSynthesis.cancel()
      setSpeaking(false)
      return
    }
    const utter = new SpeechSynthesisUtterance(resource.content || '')
    utter.onend = () => setSpeaking(false)
    setSpeaking(true)
    window.speechSynthesis.speak(utter)
  }

  if (error) return <div className="alert">{error}</div>
  if (!lesson) return <div className="loading">Loading lesson...</div>

  return (
    <div className="page">
      <div className="page-head">
        <div>
          <h2>{lesson.title}</h2>
          <span className="muted">{lesson.subject_name} · {lesson.difficulty}</span>
        </div>
        <span className={`badge ${lesson.difficulty.toLowerCase()}`}>{lesson.difficulty}</span>
      </div>

      <ProgressBar value={lesson.progress} label="Lesson progress" />

      {rec && (
        <div className="rec-banner">
          <div>
            <strong>Recommended for you: {rec.recommended_format_label}</strong>
            <p><strong>Reason:</strong> {rec.reason}</p>
          </div>
          <span className="confidence-chip">{Math.round((rec.confidence || 0) * 100)}%</span>
        </div>
      )}

      <div className="format-picker">
        <span className="format-label">Choose Learning Format</span>
        <div className="format-buttons">
          {ORDER.map((type) => (
            <button
              key={type}
              className={`format-btn ${active === type ? 'active' : ''} ${rec?.recommended_format === type ? 'recommended' : ''}`}
              onClick={() => setActive(type)}
            >
              {SHORT_LABELS[type]}
              {rec?.recommended_format === type && <em>★ Recommended</em>}
            </button>
          ))}
        </div>
      </div>

      <div className="panel lesson-content">
        <div className="lesson-content-head">
          <h3>{resource?.title || 'Lesson Content'}</h3>
          {active === 'AUDIO' && (
            <button className="ghost-btn" onClick={speak}>
              {speaking ? '◼ Stop' : '▶ Play audio'}
            </button>
          )}
        </div>
        <div className={active === 'VISUAL' ? 'content-visual' : 'content-text'}>
          {resource?.content}
        </div>
      </div>

      <div className="lesson-actions">
        <Link className="ghost-btn" to={`/subjects/${lesson.subject_id}`}>← Previous</Link>
        {lesson.quiz_id ? (
          <button className="primary-btn" onClick={() => navigate(`/quiz/${lesson.quiz_id}`)}>
            Take Quiz →
          </button>
        ) : (
          <span className="muted">Quiz coming soon</span>
        )}
      </div>
    </div>
  )
}
