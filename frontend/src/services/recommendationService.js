import { api } from './api.js'

export const getRecommendations = () => api.get('/recommendations')
export const getLatestRecommendation = () => api.get('/recommendations/latest')
export const generateRecommendation = (lessonId) =>
  api.post('/recommendations/generate', lessonId ? { lesson_id: lessonId } : {})
export const predict = (features) => api.post('/predict', features)
