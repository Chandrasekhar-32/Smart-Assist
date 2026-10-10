import { useAuth } from '../../context/AuthContext.jsx'

export default function TeacherProfile() {
  const { user } = useAuth()
  if (!user) return null
  return (
    <div className="page narrow">
      <div className="panel">
        <div className="profile-head">
          <div className="avatar big">{user.name[0]}</div>
          <div>
            <h2>{user.name}</h2>
            <span className="muted">{user.email} · Teacher</span>
          </div>
        </div>
        <div className="info-box">
          <span>Role</span>
          <strong>Teacher</strong>
        </div>
        <div className="info-box">
          <span>Access</span>
          <strong>Student performance, progress and ML recommendations</strong>
        </div>
        <p className="muted">
          Recommendations are generated automatically by the SmartAssist ML module from student
          performance data - teachers review them with their explanations.
        </p>
      </div>
    </div>
  )
}
