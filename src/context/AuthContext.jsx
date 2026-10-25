import { useEffect, useState, useCallback, useRef } from 'react'
import { AuthContext } from './authContextDef.js'

function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^|;\\s*)' + name + '=([^;]*)'))
  return match ? decodeURIComponent(match[2]) : null
}

export function AuthProvider({ children, enabled = false }) {
  const [user, setUser] = useState(null)
  const [authenticated, setAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)
  const sessionVersion = useRef(0)

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
    const version = ++sessionVersion.current
    try {
      const res = await fetch('/api/auth/status/', { credentials: 'same-origin' })
      if (res.ok) {
        const data = await res.json()
        if (version !== sessionVersion.current) return
        setAuthenticated(Boolean(data.authenticated))
        setUser(data.user || null)
      } else {
        if (version !== sessionVersion.current) return
        setAuthenticated(false)
        setUser(null)
      }
    } catch {
      if (version !== sessionVersion.current) return
      setAuthenticated(false)
      setUser(null)
    } finally {
      if (version === sessionVersion.current) setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (enabled) { refreshStatus() }
    else { sessionVersion.current++; setAuthenticated(false); setUser(null); setLoading(enabled === null) }
  }, [enabled, refreshStatus])

  useEffect(() => {
    if (!enabled) return undefined
    const expired = () => { sessionVersion.current++; setAuthenticated(false); setUser(null); setLoading(false) }
    const refresh = () => { refreshStatus() }
    window.addEventListener('prepal:session-expired', expired)
    window.addEventListener('focus', refresh)
    window.addEventListener('pageshow', refresh)
    return () => {
      window.removeEventListener('prepal:session-expired', expired)
      window.removeEventListener('focus', refresh)
      window.removeEventListener('pageshow', refresh)
    }
  }, [enabled, refreshStatus])

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
    sessionVersion.current++
    setLoading(false)
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
    sessionVersion.current++
    setLoading(false)
    setAuthenticated(true)
    setUser(data.user)
    return data.user
  }

  const logout = async () => {
    const token = await fetchCsrfToken()
    const response = await fetch('/api/auth/logout/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': token,
        },
        credentials: 'same-origin',
      })
      if (!response.ok) throw new Error('Sign out failed. Please try again.')
      sessionVersion.current++
      setLoading(false)
      setAuthenticated(false)
      setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, authenticated, featuresEnabled: enabled === true, loading, login, register, logout, refreshStatus }}>
      {children}
    </AuthContext.Provider>
  )
}

export default AuthProvider
