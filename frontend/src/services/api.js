
const BASE = (import.meta.env.VITE_API_URL || 'https://smart-assist-rbxl.onrender.com').replace(/\/$/, '')

function token() {
  return localStorage.getItem('smartassist_token')
}

export function setUser(user) {
  if (user) localStorage.setItem('smartassist_user', JSON.stringify(user))
  else localStorage.removeItem('smartassist_user')
}

export function getUser() {
  try {
    return JSON.parse(localStorage.getItem('smartassist_user'))
  } catch {
    return null
  }
}

async function request(path, { method = 'GET', body, auth = true } = {}) {
  const headers = { 'Content-Type': 'application/json' }

  if (auth && token()) {
    headers.Authorization = `Bearer ${token()}`
  }

  const url = `${BASE}${path.startsWith('/') ? path : `/${path}`}`

  const res = await fetch(url, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })

  let data = null

  try {
    data = await res.json()
  } catch {
    data = null
  }

  if (!res.ok) {
    const message = Array.isArray(data?.detail)
      ? data.detail.map((d) => d.msg).join(', ')
      : data?.detail || `Request failed (${res.status})`

    const err = new Error(message)
    err.status = res.status
    throw err
  }

  return data
}

export const api = {
  get: (path) => request(path),
  post: (path, body) => request(path, { method: 'POST', body }),
  put: (path, body) => request(path, { method: 'PUT', body }),
}
