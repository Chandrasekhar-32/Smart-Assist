import { api, setUser } from './api.js'

export async function login(email, password) {
  const data = await api.post('/auth/login', { email, password })
  localStorage.setItem('smartassist_token', data.access_token)
  setUser(data.user)
  return data.user
}

export async function register(payload) {
  const data = await api.post('/auth/register', payload)
  localStorage.setItem('smartassist_token', data.access_token)
  setUser(data.user)
  return data.user
}

export function logout() {
  localStorage.removeItem('smartassist_token')
  localStorage.removeItem('smartassist_user')
}
