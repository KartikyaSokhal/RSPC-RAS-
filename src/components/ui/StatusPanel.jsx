import { Link } from 'react-router-dom'

export default function StatusPanel({ title = 'A quiet moment in the library.', children, retry, to = '/syllabus', linkLabel = 'Explore the syllabus' }) {
  return <section className="status-panel" role="status">
    <span className="status-symbol" aria-hidden="true">◌</span>
    <h2>{title}</h2><p>{children}</p>
    <div className="button-row">{retry && <button className="button primary" onClick={retry}>Try again</button>}<Link className="button" to={to}>{linkLabel} <span aria-hidden="true">→</span></Link></div>
  </section>
}
