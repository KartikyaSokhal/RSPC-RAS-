import { useEffect, useState, useCallback } from 'react'
import { AuthContext } from './authContextDef.js'

function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^|;\\s*)' + name + '=([^;]*)'))
  return match ? decodeURIComponent(match[2]) : null
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [authenticated, setAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  const fetchCsrfToken = useCallback(async () => {
    let token = getCookie('csrftoken')
    if (!token) {
      try {
        const res = await fetch('/api/config/', { credentials: 'same-origin' })
        const json = await res.json()
        token = json.csrf_token || getCookie('csrftoken')
      } catch {
        /* Ignore error */
      }
    }
    return token || ''
  }, [])

  const refreshStatus = useCallback(async () => {
    try {
      const res = await fetch('/api/auth/status/', { credentials: 'same-origin' })
      if (res.ok) {
        const data = await res.json()
        setAuthenticated(Boolean(data.authenticated))
        setUser(data.user || null)
      } else {
        setAuthenticated(false)
        setUser(null)
      }
    } catch {
      setAuthenticated(false)
      setUser(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    refreshStatus()
  }, [refreshStatus])

  const login = async ({ username, password }) => {
    const token = await fetchCsrfToken()
    const res = await fetch('/api/auth/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': token,
      },
      credentials: 'same-origin',
      body: JSON.stringify({ username, password }),
    })
    const data = await res.json()
    if (!res.ok) {
      throw new Error(data?.error?.message || data?.detail || 'Invalid username or password.')
    }
    setAuthenticated(true)
    setUser(data.user)
    return data.user
  }

  const register = async ({ username, password, email, name }) => {
    const token = await fetchCsrfToken()
    const res = await fetch('/api/auth/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': token,
      },
      credentials: 'same-origin',
      body: JSON.stringify({ username, password, email, name }),
    })
    const data = await res.json()
    if (!res.ok) {
      throw new Error(data?.error?.message || data?.detail || 'Registration failed.')
    }
    setAuthenticated(true)
    setUser(data.user)
    return data.user
  }

  const logout = async () => {
    const token = await fetchCsrfToken()
    try {
      await fetch('/api/auth/logout/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': token,
        },
        credentials: 'same-origin',
      })
    } finally {
      setAuthenticated(false)
      setUser(null)
    }
  }

  return (
    <AuthContext.Provider value={{ user, authenticated, loading, login, register, logout, refreshStatus }}>
      {children}
    </AuthContext.Provider>
  )
}

export default AuthProvider
