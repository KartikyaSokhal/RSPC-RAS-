import { useContext, useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { PlatformContext } from '../components/layout/platformContext.js'
import { returnLocation } from '../components/auth/returnLocation.js'
import GoogleSignIn from '../components/auth/GoogleSignIn.jsx'
import useAuth from '../hooks/useAuth.js'

export default function SignupPage() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const config = useContext(PlatformContext)
  const [name, setName] = useState('')
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    if (password.length < 8) {
      setError('Password must be at least 8 characters long.')
      return
    }
    setLoading(true)
    try {
      await register({ username, password, email, name })
      navigate(returnLocation(location.state?.from), { replace: true })
    } catch (err) {
      setError(err.message || 'Registration failed. Please check your information.')
    } finally {
      setLoading(false)
    }
  }

  if (config.registration_enabled === false) return <div className="page auth-page"><div className="auth-card"><h1>Student registration is not available</h1><p>This synthetic demonstration does not collect real student data. Use an assigned demo account to sign in. Public registration requires approved persistent storage and recovery safeguards.</p><Link className="button primary" to="/login" state={{ from: location.state?.from }}>Sign In</Link> <Link to="/">Return to homepage</Link></div></div>

  return (
    <div className="page auth-page">
      <div className="auth-card">
        <div className="auth-header">
          <span className="brand-mark small" aria-hidden="true">p<span>·</span></span>
          <h1>Create student account</h1>
          <p>Join Prepal to track your syllabus completion, save bookmarks, and view your quiz practice history.</p>
        </div>

        {error && (
          <div className="auth-error-banner" role="alert">
            {error}
          </div>
        )}

        <GoogleSignIn />
        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="signup-name">Full name</label>
            <input
              id="signup-name"
              type="text"
              autoComplete="name"
              value={name}
              onChange={e => setName(e.target.value)}
              placeholder="e.g. Priyanshi Sharma"
            />
          </div>

          <div className="form-group">
            <label htmlFor="signup-username">Username *</label>
            <input
              id="signup-username"
              type="text"
              required
              autoComplete="username"
              value={username}
              onChange={e => setUsername(e.target.value)}
              placeholder="e.g. priyanshi_ras"
            />
            <small className="form-hint">At least 3 characters. Letters, numbers, and underscores.</small>
          </div>

          <div className="form-group">
            <label htmlFor="signup-email">Email *</label>
            <input
              id="signup-email"
              required
              type="email"
              autoComplete="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="student@example.com"
            />
          </div>

          <div className="form-group">
            <label htmlFor="signup-password">Password *</label>
            <input
              id="signup-password"
              type="password"
              required
              minLength={8}
              autoComplete="new-password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="Minimum 8 characters"
            />
          </div>

          <button type="submit" className="button primary full-width" disabled={loading}>
            {loading ? 'Creating account…' : 'Create Account & Start Learning →'}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Already have an account?{' '}
            <Link to="/login" state={{ from: location.state?.from }} className="auth-switch-link">
              Sign in
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
