
import { api, setUser } from './api.js'

export async function login(email, password) {
  const data = await api.post('/api/auth/login', { email, password })

  if (!data || !data.access_token) {
    throw new Error('Login failed: the server did not return an access token.')
  }

  localStorage.setItem('smartassist_token', data.access_token)

  if (data.user) {
    setUser(data.user)
    return data.user
  }

  throw new Error('Login response has no user information. Check the backend login response.')
}

export async function register(payload) {
  const data = await api.post('/api/auth/register', payload)

  if (!data || !data.access_token) {
    throw new Error('Registration failed: the server did not return an access token.')
  }

  localStorage.setItem('smartassist_token', data.access_token)

  if (data.user) {
    setUser(data.user)
    return data.user
  }

  throw new Error('Registration response has no user information. Check the backend registration response.')
}

export function logout() {
  localStorage.removeItem('smartassist_token')
  localStorage.removeItem('smartassist_user')
}
