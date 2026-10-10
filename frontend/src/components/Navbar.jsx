import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function Navbar({ title }) {
  const { user, logout } = useAuth()
  return (
    <header className="navbar">
      <h1>{title || 'SmartAssist'}</h1>
      <div className="navbar-actions">
        <Link to={user?.role === 'TEACHER' ? '/teacher/profile' : '/profile'} className="link-btn">
          Profile
        </Link>
        <button className="ghost-btn" onClick={logout}>
          Logout
        </button>
      </div>
    </header>
  )
}
