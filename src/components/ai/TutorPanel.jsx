import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import SafeMarkdown from '../content/SafeMarkdown.jsx'
import { post, errorMessage } from '../../api/client.js'

export default function TutorPanel({ topic, selected, clearSelection, onCitation, onClose }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [related, setRelated] = useState(false)
  const controller = useRef(null)
  const bottom = useRef(null)
  useEffect(() => () => controller.current?.abort(), [])
  async function send(preset) {
    const text = input.trim()
    if (busy || (!text && !preset)) return
    const request = new AbortController(); controller.current = request
    setBusy(true); setError('')
    const history = messages.slice(-6).map(m => ({ role: m.role, text: m.text.slice(0, 1000) }))
    while (history.reduce((n, m) => n + m.text.length, 0) > 4000) history.shift()
    try {
      const response = await post(`/topic/${topic.slug}/chat/`, { message: text, ...(preset ? { preset } : {}), history, allow_related: related, ...(selected ? { selected } : {}) }, request.signal)
      if (request.signal.aborted) return
      setMessages(previous => [...previous.slice(-18), { role: 'user', text: text || `${preset} ${selected ? 'this passage' : 'this lesson'}` }, { role: 'assistant', text: response.response, citations: response.citations || [], mocked: response.mocked }])
      setInput('')
      // Only scroll on this explicit send, not when reading earlier messages.
      requestAnimationFrame(() => bottom.current?.scrollIntoView({ block: 'nearest', behavior: 'instant' }))
    } catch (err) {
      if (!request.signal.aborted) setError(errorMessage(err, 'The tutor could not respond. You can keep reading and try again later.'))
    } finally { if (!request.signal.aborted) setBusy(false) }
  }
  return (
    <section className="tutor-panel ai-companion-panel" aria-labelledby="tutor-heading">
      <div className="tutor-heading">
        <span className="spark-icon" aria-hidden="true">✨</span>
        <div style={{ flex: 1 }}>
          <h2 id="tutor-heading">AI Study Assistant</h2>
          <p>Ask questions or clarify concepts</p>
        </div>
        <span className="tutor-dot" title="Active on this topic" aria-hidden="true" />
        {onClose && (
          <button
            type="button"
            className="tutor-close-btn"
            onClick={onClose}
            aria-label="Close AI Assistant"
            title="Close Assistant"
          >
            ✕
          </button>
        )}
      </div>

      <div className="scope-label">
        GROUNDED IN THIS LESSON {related ? '+ RELATED SOURCES' : ''}
      </div>

      <div className="chat-messages" aria-live="polite" aria-busy={busy}>
        {!messages.length && (
          <div className="tutor-welcome">
            <span className="welcome-spark" aria-hidden="true">💡</span>
            <h3>Ask doubts about this topic</h3>
            <p>
              Ask about archaeological evidence, dates, key concepts, or select any text passage in the notes to get instant clarification.
            </p>
            <p className="small">
              Answers are grounded in verified lesson sources. Always check citations.
            </p>
          </div>
        )}
        {messages.map((message, i) => (
          <div key={i} className={`chat-msg ${message.role === 'user' ? 'chat-msg-user' : 'chat-msg-bot'}`}>
            <span className="message-label">
              {message.role === 'user' ? 'YOU' : message.mocked ? 'PREPAL · MOCK RESPONSE' : 'PREPAL TUTOR'}
            </span>
            {message.role === 'assistant' ? (
              <SafeMarkdown>{message.text}</SafeMarkdown>
            ) : (
              <p>{message.text}</p>
            )}
            {message.citations?.length > 0 && (
              <div className="citation-list">
                <span className="label">RETURN TO THE SOURCE</span>
                {message.citations.map(c => (
                  <Link key={c.id} to={c.url} onClick={onCitation} className="citation-link">
                    <span aria-hidden="true">↗</span>{c.title}
                  </Link>
                ))}
              </div>
            )}
          </div>
        ))}
        {busy && (
          <p role="status" className="thinking">
            <span className="pulse-dot" />Reading the sources…
          </p>
        )}
        <div ref={bottom} />
      </div>

      {selected && (
        <div className="selected-passage">
          <div className="row">
            <strong>Selected passage</strong>
            <button className="icon-button" onClick={clearSelection} aria-label="Clear selected passage">
              ×
            </button>
          </div>
          <p>“{selected.text.slice(0, 180)}{selected.text.length > 180 ? '…' : ''}”</p>
        </div>
      )}

      <div className="tutor-actions">
        <button disabled={busy} onClick={() => send('explain')}>Explain simply</button>
        <button disabled={busy} onClick={() => send('summarize')}>Summarize</button>
        <button disabled={busy} onClick={() => send('examples')}>Give an example</button>
      </div>

      {topic.related?.length > 0 && (
        <label className="related-toggle">
          <input type="checkbox" checked={related} onChange={e => setRelated(e.target.checked)} />
          Include reviewed related lessons
        </label>
      )}

      {error && <p className="inline-error" role="alert">{error}</p>}

      <form className="chat-form" onSubmit={e => { e.preventDefault(); send() }}>
        <label className="sr-only" htmlFor="tutor-question">Ask the tutor</label>
        <textarea
          id="tutor-question"
          maxLength={2000}
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Ask a question about this topic (e.g. key findings, dates)..."
          rows={3}
          disabled={busy}
        />
        <div className="row">
          <span>Grounded in syllabus sources</span>
          <button className="send-button" type="submit" aria-label="Send question" disabled={busy || !input.trim()}>
            <span aria-hidden="true">↑</span>
          </button>
        </div>
      </form>
    </section>
  )
}
