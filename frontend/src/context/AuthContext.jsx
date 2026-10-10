import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import * as authService from '../services/authService.js'
import { getUser } from '../services/api.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUserState] = useState(getUser())

  useEffect(() => {
    setUserState(getUser())
  }, [])

  const value = useMemo(
    () => ({
      user,
      login: async (email, password) => {
        const u = await authService.login(email, password)
        setUserState(u)
        return u
      },
      register: async (payload) => {
        const u = await authService.register(payload)
        setUserState(u)
        return u
      },
      logout: () => {
        authService.logout()
        setUserState(null)
      },
    }),
    [user],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  return useContext(AuthContext)
}
