import { useEffect, useState } from 'react'
import { get } from '../api/client.js'

export default function useResource(path) {
  const [attempt, setAttempt] = useState(0)
  const [state, setState] = useState({ key: null, data: null, error: null })
  const key = `${path}:${attempt}`
  useEffect(() => {
    if (!path) return undefined
    let active = true
    const controller = new AbortController()
    get(path, controller.signal).then(data => {
      if (active) setState({ key, data, error: null })
    }).catch(error => {
      if (active && error.code !== 'ERR_CANCELED') setState({ key, data: null, error })
    })
    return () => { active = false; controller.abort() }
  }, [path, key])
  return { data: state.key === key ? state.data : null, error: state.key === key ? state.error : null,
    loading: Boolean(path) && state.key !== key, retry: () => setAttempt(n => n + 1) }
}
