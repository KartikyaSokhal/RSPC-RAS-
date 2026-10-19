import { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import useAuth from '../hooks/useAuth.js'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const from = location.state?.from?.pathname || '/dashboard'

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login({ username, password })
      navigate(from, { replace: true })
    } catch (err) {
      setError(err.message || 'Unable to sign in. Please check your credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page auth-page">
      <div className="auth-card">
        <div className="auth-header">
          <span className="brand-mark small" aria-hidden="true">p<span>·</span></span>
          <h1>Welcome back</h1>
          <p>Sign in to your Prepal student account to continue your RPSC preparation.</p>
        </div>

        {error && (
          <div className="auth-error-banner" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="login-username">Username</label>
            <input
              id="login-username"
              type="text"
              required
              autoComplete="username"
              value={username}
              onChange={e => setUsername(e.target.value)}
              placeholder="e.g. ras_aspirant"
            />
          </div>

          <div className="form-group">
            <label htmlFor="login-password">Password</label>
            <input
              id="login-password"
              type="password"
              required
              autoComplete="current-password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="Your password"
            />
          </div>

          <button type="submit" className="button primary full-width" disabled={loading}>
            {loading ? 'Signing in…' : 'Sign in to Dashboard →'}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Don’t have an account yet?{' '}
            <Link to="/signup" className="auth-switch-link">
              Create student account
            </Link>
          </p>
          <div style={{ marginTop: '16px' }}>
            <Link to="/syllabus" className="text-muted small">
              ← Continue browsing as guest
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
