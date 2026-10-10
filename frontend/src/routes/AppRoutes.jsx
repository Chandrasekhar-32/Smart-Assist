import { Navigate, Route, Routes } from 'react-router-dom'
import AppLayout from '../components/AppLayout.jsx'
import { useAuth } from '../context/AuthContext.jsx'

import Login from '../pages/auth/Login.jsx'
import Register from '../pages/auth/Register.jsx'

import StudentDashboard from '../pages/student/StudentDashboard.jsx'
import Subjects from '../pages/student/Subjects.jsx'
import MyLearning from '../pages/student/MyLearning.jsx'
import Lesson from '../pages/student/Lesson.jsx'
import Quiz from '../pages/student/Quiz.jsx'
import QuizResult from '../pages/student/QuizResult.jsx'
import Recommendation from '../pages/student/Recommendation.jsx'
import Progress from '../pages/student/Progress.jsx'
import Profile from '../pages/student/Profile.jsx'

import TeacherDashboard from '../pages/teacher/TeacherDashboard.jsx'
import StudentList from '../pages/teacher/StudentList.jsx'
import StudentDetails from '../pages/teacher/StudentDetails.jsx'
import TeacherPerformance from '../pages/teacher/TeacherPerformance.jsx'
import TeacherRecommendations from '../pages/teacher/TeacherRecommendations.jsx'
import TeacherProfile from '../pages/teacher/TeacherProfile.jsx'

function Protected({ role, children }) {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  if (role && user.role !== role) {
    return <Navigate to={user.role === 'TEACHER' ? '/teacher' : '/dashboard'} replace />
  }
  return children
}

function Home() {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  return <Navigate to={user.role === 'TEACHER' ? '/teacher' : '/dashboard'} replace />
}

function Guest({ children }) {
  const { user } = useAuth()
  if (user) return <Navigate to={user.role === 'TEACHER' ? '/teacher' : '/dashboard'} replace />
  return children
}

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Guest><Login /></Guest>} />
      <Route path="/register" element={<Guest><Register /></Guest>} />

      <Route element={<Protected role="STUDENT"><AppLayout /></Protected>}>
        <Route path="/dashboard" element={<StudentDashboard />} />
        <Route path="/subjects" element={<Subjects />} />
        <Route path="/subjects/:subjectId" element={<Subjects />} />
        <Route path="/my-learning" element={<MyLearning />} />
        <Route path="/lessons/:lessonId" element={<Lesson />} />
        <Route path="/quiz/:quizId" element={<Quiz />} />
        <Route path="/result" element={<QuizResult />} />
        <Route path="/recommendations" element={<Recommendation />} />
        <Route path="/progress" element={<Progress />} />
        <Route path="/profile" element={<Profile />} />
      </Route>

      <Route element={<Protected role="TEACHER"><AppLayout /></Protected>}>
        <Route path="/teacher" element={<TeacherDashboard />} />
        <Route path="/teacher/students" element={<StudentList />} />
        <Route path="/teacher/students/:studentId" element={<StudentDetails />} />
        <Route path="/teacher/performance" element={<TeacherPerformance />} />
        <Route path="/teacher/recommendations" element={<TeacherRecommendations />} />
        <Route path="/teacher/profile" element={<TeacherProfile />} />
      </Route>

      <Route path="*" element={<Home />} />
    </Routes>
  )
}
