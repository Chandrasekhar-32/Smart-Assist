import { api } from './api.js'

export const getSubjects = () => api.get('/subjects')
export const getSubjectLessons = (id) => api.get(`/subjects/${id}/lessons`)
export const getLesson = (id) => api.get(`/lessons/${id}`)
export const getLessonResources = (id) => api.get(`/lessons/${id}/resources`)
export const markViewed = (id) => api.post(`/lessons/${id}/view`, {})
export const getMyLessons = () => api.get('/student/lessons')
export const getDashboard = () => api.get('/student/dashboard')
export const getProgress = () => api.get('/student/progress')
export const getProfile = () => api.get('/student/profile')
export const updateProfile = (payload) => api.put('/student/profile', payload)
