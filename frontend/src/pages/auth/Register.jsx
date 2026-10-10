import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext.jsx'

const FORMATS = ['TEXT', 'SIMPLIFIED_TEXT', 'VISUAL', 'AUDIO', 'SHORT_LESSON']
const FORMAT_LABELS = {
  TEXT: 'Text', SIMPLIFIED_TEXT: 'Simplified Text', VISUAL: 'Visual',
  AUDIO: 'Audio', SHORT_LESSON: 'Short Lessons',
}

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({
    name: '', email: '', password: '', role: 'STUDENT',
    age: '', preferred_format: 'TEXT',
  })
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const set = (key) => (e) => setForm({ ...form, [key]: e.target.value })

  const submit = async (e) => {
    e.preventDefault()
    setError('')
    setBusy(true)
    try {
      const payload = { ...form, age: form.age ? Number(form.age) : null }
      const user = await register(payload)
      navigate(user.role === 'TEACHER' ? '/teacher' : '/dashboard')
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card wide">
        <div className="auth-brand">
          <span className="brand-dot big">S</span>
          <h1>Create your account</h1>
          <p>Join SmartAssist and get personalized learning recommendations</p>
        </div>
        <form onSubmit={submit}>
          {error && <div className="alert">{error}</div>}
          <div className="grid-2">
            <label>
              Full name
              <input required value={form.name} onChange={set('name')} placeholder="Your name" />
            </label>
            <label>
              Email
              <input type="email" required value={form.email} onChange={set('email')} placeholder="you@example.com" />
            </label>
            <label>
              Password
              <input type="password" required minLength={6} value={form.password} onChange={set('password')} placeholder="At least 6 characters" />
            </label>
            <label>
              I am a
              <select value={form.role} onChange={set('role')}>
                <option value="STUDENT">Student</option>
                <option value="TEACHER">Teacher</option>
              </select>
            </label>
            {form.role === 'STUDENT' && (
              <>
                <label>
                  Age (optional)
                  <input type="number" min={5} max={99} value={form.age} onChange={set('age')} placeholder="20" />
                </label>
                <label>
                  Preferred learning format
                  <select value={form.preferred_format} onChange={set('preferred_format')}>
                    {FORMATS.map((f) => (
                      <option key={f} value={f}>{FORMAT_LABELS[f]}</option>
                    ))}
                  </select>
                </label>
              </>
            )}
          </div>
          <button className="primary-btn block" disabled={busy}>
            {busy ? 'Creating account...' : 'Register'}
          </button>
        </form>
        <p className="auth-switch">
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  )
}
