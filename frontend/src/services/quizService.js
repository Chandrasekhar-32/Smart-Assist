import { api } from './api.js'

export const getQuiz = (id) => api.get(`/quizzes/${id}`)
export const submitQuiz = (id, answers, timeTaken) =>
  api.post(`/quizzes/${id}/submit`, { answers, time_taken: timeTaken })
export const getAttempts = () => api.get('/attempts')
