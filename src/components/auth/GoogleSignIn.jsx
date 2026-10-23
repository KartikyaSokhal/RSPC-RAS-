import { useContext, useState } from 'react'
import { PlatformContext } from '../layout/platformContext.js'
import { post, errorMessage } from '../../api/client.js'
export default function GoogleSignIn() {
  const config = useContext(PlatformContext)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  return <div className="google-signin"><button className="button full-width" type="button" disabled={!config.google_signin_enabled || busy} onClick={async () => {
    setBusy(true); setError('')
    try { const data = await post('/auth/google/start/', {}); window.location.assign(data.url) }
    catch (err) { setError(errorMessage(err)); setBusy(false) }
  }}>Continue with Google</button>{!config.google_signin_enabled && <p className="form-hint">Google sign-in needs configuration. Email sign-in is available.</p>}{error && <p role="alert">{error}</p>}</div>
}
