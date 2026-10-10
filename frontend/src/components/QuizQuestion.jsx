const OPTIONS = ['A', 'B', 'C', 'D']

export default function QuizQuestion({ index, total, question, answer, onAnswer }) {
  if (!question) return null
  return (
    <div className="quiz-question">
      <div className="quiz-question-head">
        <span className="chip">Question {index + 1} of {total}</span>
      </div>
      <h3>{question.question}</h3>
      <div className="options">
        {OPTIONS.map((key) => {
          const text = question[`option_${key.toLowerCase()}`]
          return (
            <label key={key} className={`option ${answer === key ? 'selected' : ''}`}>
              <input
                type="radio"
                name={`q-${question.id}`}
                checked={answer === key}
                onChange={() => onAnswer(key)}
              />
              <span className="option-key">{key}</span>
              <span>{text}</span>
            </label>
          )
        })}
      </div>
    </div>
  )
}
