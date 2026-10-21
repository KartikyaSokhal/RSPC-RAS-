import { useEffect, useRef } from 'react'
import useResource from '../../hooks/useResource.js'

export default function TopicPopup({ topic, onClose, onUnavailable }) {
  const { data, loading, error } = useResource(`/topic/${encodeURIComponent(topic.slug)}/context/`)
  const close = useRef(null)
  useEffect(() => { close.current?.focus({ preventScroll: true }) }, [])
  useEffect(() => { if (error?.response?.status === 404) onUnavailable?.() }, [error, onUnavailable])
  function keyboard(event) {
    if (event.key === 'Escape') { event.preventDefault(); onClose() }
    if (event.key === 'Tab') {
      const controls = [...event.currentTarget.querySelectorAll('button,a[href]')]
      const first = controls[0]; const last = controls.at(-1)
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus({ preventScroll: true }) }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus({ preventScroll: true }) }
    }
  }
  return <div className="topic-popup-backdrop" onClick={event => { if (event.target === event.currentTarget) onClose() }}>
    <section className="topic-popup" role="dialog" aria-modal="true" aria-labelledby="prepal-popup-title" aria-describedby="prepal-popup-description" onKeyDown={keyboard}>
      <button ref={close} className="button" type="button" onClick={onClose} aria-label="Close topic preview">Close ×</button>
      <h2 id="prepal-popup-title">{data?.title || topic.title}</h2>
      <p id="prepal-popup-description">{loading ? 'Opening topic preview…' : error ? 'This topic preview is unavailable. Close this window to continue reading.' : data?.description || 'No overview is available; open the published topic to read it.'}</p>
      {data && !error && <a className="button primary" href={`/topic/${encodeURIComponent(topic.slug)}`} target="_blank" rel="noopener noreferrer" aria-label="Open Full Topic (opens in a new tab)">Open Full Topic ↗</a>}
    </section>
  </div>
}
