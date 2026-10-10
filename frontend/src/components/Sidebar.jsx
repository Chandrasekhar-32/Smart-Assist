import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

const STUDENT_ITEMS = [
  { to: '/dashboard', label: 'Dashboard', icon: '◧' },
  { to: '/subjects', label: 'Subjects', icon: '▤' },
  { to: '/my-learning', label: 'My Learning', icon: '▣' },
  { to: '/recommendations', label: 'Recommendations', icon: '✦' },
  { to: '/progress', label: 'Progress', icon: '◫' },
  { to: '/profile', label: 'Profile', icon: '◐' },
]

const TEACHER_ITEMS = [
  { to: '/teacher', label: 'Dashboard', icon: '◧' },
  { to: '/teacher/students', label: 'Students', icon: '▤' },
  { to: '/teacher/performance', label: 'Performance', icon: '▦' },
  { to: '/teacher/recommendations', label: 'Recommendations', icon: '✦' },
  { to: '/teacher/profile', label: 'Profile', icon: '◐' },
]

export default function Sidebar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const items = user?.role === 'TEACHER' ? TEACHER_ITEMS : STUDENT_ITEMS

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <aside className="sidebar">
      <div className="brand">
        <span className="brand-dot">S</span>
        <div>
          <strong>SmartAssist</strong>
          <small>Adaptive Learning</small>
        </div>
      </div>
      <nav className="nav">
        {items.map((item) => (
          <NavLink key={item.to} to={item.to} className={({ isActive }) => (isActive ? 'active' : '')}>
            <span className="nav-icon">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
        <button className="nav-link" onClick={handleLogout}>
          <span className="nav-icon">↩</span>
          Logout
        </button>
      </nav>
      <div className="sidebar-foot">
        <div className="avatar">{user?.name?.[0] || '?'}</div>
        <div>
          <strong>{user?.name}</strong>
          <small>{user?.role === 'TEACHER' ? 'Teacher' : 'Student'}</small>
        </div>
      </div>
    </aside>
  )
}
