import { useContext, useEffect, useState } from 'react'
import { PlatformContext } from '../components/layout/platformContext.js'
import { Link, useNavigate } from 'react-router-dom'
import { post, errorMessage } from '../api/client.js'
import useAuth from '../hooks/useAuth.js'
export default function ResetPasswordPage() {
  const config = useContext(PlatformContext)
  const { refreshStatus } = useAuth()
  const navigate = useNavigate()
  const [credentials] = useState(() => Object.fromEntries(new URLSearchParams(window.location.hash.slice(1))))
  useEffect(() => { if (window.location.hash) window.history.replaceState({}, '', window.location.pathname) }, [])
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const confirming = Boolean(credentials.uid && credentials.token)
  if (config.password_reset_enabled === false) return <div className="page auth-page"><section className="auth-card"><h1>Password recovery is unavailable</h1><p>This synthetic preview does not collect email addresses or send recovery messages. Ask the local operator for your assigned demo account.</p><Link to="/login">Back to sign in</Link></section></div>
  return <div className="page auth-page"><section className="auth-card"><h1>{confirming ? 'Choose a new password' : 'Reset your password'}</h1><p>Recovery is available for accounts with an email address and password.</p><form className="auth-form" onSubmit={async event => {
    event.preventDefault(); setBusy(true); setError(''); setMessage('')
    try {
      const result = await post(confirming ? '/auth/password-reset/confirm/' : '/auth/password-reset/', confirming ? {...credentials, password} : {email})
      setMessage(result.message); setPassword('')
      if (confirming) {
        await refreshStatus()
        navigate('/login', {replace: true, state: {passwordReset: true}})
      }
    } catch (err) { setError(errorMessage(err)) } finally { setBusy(false) }
  }}>{confirming ? <label>New password<input type="password" autoComplete="new-password" required minLength={8} maxLength={256} value={password} onChange={e => setPassword(e.target.value)} /></label> : <label>Email<input type="email" autoComplete="email" required value={email} onChange={e => setEmail(e.target.value)} /></label>}<button className="button primary" disabled={busy}>{busy ? 'Please wait…' : confirming ? 'Change password' : 'Send recovery email'}</button></form>{error && <p role="alert">{error}</p>}{message && <p role="status">{message}</p>}<Link to="/login">Back to sign in</Link></section></div>
}
