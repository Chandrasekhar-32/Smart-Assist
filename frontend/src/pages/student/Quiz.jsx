import { useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import QuizQuestion from '../../components/QuizQuestion.jsx'
import { getQuiz, submitQuiz } from '../../services/quizService.js'

export default function Quiz() {
  const { quizId } = useParams()
  const navigate = useNavigate()
  const [quiz, setQuiz] = useState(null)
  const [answers, setAnswers] = useState({})
  const [index, setIndex] = useState(0)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [elapsed, setElapsed] = useState(0)
  const timer = useRef(null)

  useEffect(() => {
    getQuiz(quizId).then(setQuiz).catch((e) => setError(e.message))
    timer.current = setInterval(() => setElapsed((e) => e + 1), 1000)
    return () => clearInterval(timer.current)
  }, [quizId])

  if (error) return <div className="alert">{error}</div>
  if (!quiz) return <div className="loading">Loading quiz...</div>

  const questions = quiz.questions
  const question = questions[index]
  const answered = Object.keys(answers).length
  const minutes = String(Math.floor(elapsed / 60)).padStart(2, '0')
  const seconds = String(elapsed % 60).padStart(2, '0')

  const submit = async () => {
    setBusy(true)
    try {
      const payload = questions.map((q) => ({
        question_id: q.id,
        answer: answers[q.id] || '',
      }))
      const result = await submitQuiz(quizId, payload, elapsed)
      clearInterval(timer.current)
      navigate('/result', { state: result })
    } catch (e) {
      setError(e.message)
      setBusy(false)
    }
  }

  return (
    <div className="page narrow">
      <div className="quiz-topbar">
        <div>
          <span className="chip">{quiz.title}</span>
          <span className="muted">{answered} / {questions.length} answered</span>
        </div>
        <span className="timer">⏱ {minutes}:{seconds}</span>
      </div>

      <div className="quiz-dots">
        {questions.map((q, i) => (
          <button
            key={q.id}
            className={`dot ${i === index ? 'current' : ''} ${answers[q.id] ? 'filled' : ''}`}
            onClick={() => setIndex(i)}
            aria-label={`Question ${i + 1}`}
          />
        ))}
      </div>

      <div className="panel">
        <QuizQuestion
          index={index}
          total={questions.length}
          question={question}
          answer={answers[question.id] || ''}
          onAnswer={(key) => setAnswers({ ...answers, [question.id]: key })}
        />
      </div>

      <div className="lesson-actions">
        <button className="ghost-btn" disabled={index === 0} onClick={() => setIndex(index - 1)}>
          ← Previous
        </button>
        {index < questions.length - 1 ? (
          <button className="primary-btn" onClick={() => setIndex(index + 1)}>Next →</button>
        ) : (
          <button className="primary-btn" disabled={busy} onClick={submit}>
            {busy ? 'Submitting...' : 'Submit Quiz'}
          </button>
        )}
      </div>
      {answered > 0 && answered < questions.length && index === questions.length - 1 && (
        <p className="muted center">Unanswered questions will be marked as incorrect.</p>
      )}
    </div>
  )
}
