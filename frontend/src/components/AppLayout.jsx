import { Outlet, useLocation } from 'react-router-dom'
import Sidebar from './Sidebar.jsx'

const TITLES = [
  [/^\/dashboard/, 'Student Dashboard'],
  [/^\/subjects/, 'Subjects'],
  [/^\/my-learning/, 'My Learning'],
  [/^\/lessons/, 'Lesson'],
  [/^\/quiz/, 'Quiz'],
  [/^\/result/, 'Quiz Result'],
  [/^\/recommendations/, 'Personalized Recommendation'],
  [/^\/progress/, 'Learning Progress'],
  [/^\/profile/, 'My Profile'],
  [/^\/teacher\/students/, 'Students'],
  [/^\/teacher/, 'Teacher Dashboard'],
]

export default function AppLayout() {
  const location = useLocation()
  const title = TITLES.find(([re]) => re.test(location.pathname))?.[1] || 'SmartAssist'
  return (
    <div className="layout">
      <Sidebar />
      <main className="content">
        <div className="content-head">
          <h1>{title}</h1>
        </div>
        <Outlet />
      </main>
    </div>
  )
}
