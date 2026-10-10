import { useEffect, useState } from 'react'
import { getProfile, updateProfile } from '../../services/lessonService.js'
import { useAuth } from '../../context/AuthContext.jsx'

const FORMATS = ['TEXT', 'SIMPLIFIED_TEXT', 'VISUAL', 'AUDIO', 'SHORT_LESSON']
const FORMAT_LABELS = {
  TEXT: 'Text', SIMPLIFIED_TEXT: 'Simplified Text', VISUAL: 'Visual',
  AUDIO: 'Audio', SHORT_LESSON: 'Short Lessons',
}

export default function Profile() {
  const { user } = useAuth()
  const [form, setForm] = useState(null)
  const [saved, setSaved] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    getProfile().then(setForm).catch((e) => setError(e.message))
  }, [])

  if (error) return <div className="alert">{error}</div>
  if (!form) return <div className="loading">Loading profile...</div>

  const set = (key) => (e) => {
    setForm({ ...form, [key]: e.target.value })
    setSaved(false)
  }

  const save = async (e) => {
    e.preventDefault()
    try {
      const updated = await updateProfile({
        name: form.name,
        age: form.age ? Number(form.age) : null,
        preferred_format: form.preferred_format,
        learning_requirement: form.learning_requirement,
      })
      setForm({ ...form, ...updated })
      setSaved(true)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="page narrow">
      <div className="panel">
        <div className="profile-head">
          <div className="avatar big">{form.name?.[0]}</div>
          <div>
            <h2>{form.name}</h2>
            <span className="muted">{form.email} · {user?.role === 'TEACHER' ? 'Teacher' : 'Student'}</span>
          </div>
        </div>

        <form onSubmit={save} className="profile-form">
          {saved && <div className="alert success">Profile updated.</div>}
          <div className="grid-2">
            <label>
              Full name
              <input value={form.name} onChange={set('name')} />
            </label>
            <label>
              Email
              <input value={form.email} disabled />
            </label>
            <label>
              Age
              <input type="number" min={5} max={99} value={form.age || ''} onChange={set('age')} />
            </label>
            <label>
              Preferred learning format
              <select value={form.preferred_format} onChange={set('preferred_format')}>
                {FORMATS.map((f) => <option key={f} value={f}>{FORMAT_LABELS[f]}</option>)}
              </select>
            </label>
          </div>
          <div className="info-box">
            <span>Learning requirement (set by the ML module)</span>
            <strong>{form.learning_requirement || 'Not assessed yet'}</strong>
          </div>
          <button className="primary-btn">Save changes</button>
        </form>
      </div>
    </div>
  )
}
