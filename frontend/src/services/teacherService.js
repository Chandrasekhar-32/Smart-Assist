import { api } from './api.js'

export const getTeacherDashboard = () => api.get('/teacher/dashboard')
export const getStudents = () => api.get('/teacher/students')
export const getStudentDetails = (id) => api.get(`/teacher/students/${id}`)
export const getStudentPerformance = (id) => api.get(`/teacher/students/${id}/performance`)
export const getTeacherRecommendations = () => api.get('/teacher/recommendations')
export const getTeacherAttempts = () => api.get('/teacher/attempts')
