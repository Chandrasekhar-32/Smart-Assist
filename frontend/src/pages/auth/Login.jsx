import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext.jsx'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    setError('')
    setBusy(true)
    try {
      const user = await login(form.email, form.password)
      navigate(user.role === 'TEACHER' ? '/teacher' : '/dashboard')
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-brand">
          <span className="brand-dot big">S</span>
          <h1>SmartAssist</h1>
          <p>AI-driven adaptive learning platform</p>
        </div>
        <form onSubmit={submit}>
          {error && <div className="alert">{error}</div>}
          <label>
            Email
            <input
              type="email"
              required
              placeholder="you@example.com"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
          </label>
          <label>
            Password
            <input
              type="password"
              required
              placeholder="••••••••"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />
          </label>
          <button className="primary-btn block" disabled={busy}>
            {busy ? 'Signing in...' : 'Login'}
          </button>
        </form>
        <p className="auth-switch">
          New student? <Link to="/register">Create an account</Link>
        </p>
        <div className="demo-box">
          <strong>Demo accounts</strong>
          <span>Student: student@smartassist.edu / student123</span>
          <span>Teacher: teacher@smartassist.edu / teacher123</span>
        </div>
      </div>
    </div>
  )
}
