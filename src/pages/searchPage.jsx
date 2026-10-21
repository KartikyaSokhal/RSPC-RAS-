import { Link, useSearchParams } from 'react-router-dom'
import useResource from '../hooks/useResource.js'
import Skeleton from '../components/ui/Skeleton.jsx'
import StatusPanel from '../components/ui/StatusPanel.jsx'

export default function SearchPage() {
  const [params, setParams] = useSearchParams()
  const query = params.get('q') || ''
  const page = Math.max(1, Number(params.get('page')) || 1)
  const { data, loading, error, retry } = useResource(query ? `/search/?q=${encodeURIComponent(query)}&page=${page}` : null)

  function submit(event) {
    event.preventDefault()
    const q = new FormData(event.currentTarget).get('q').trim()
    if (q) setParams({ q, page: '1' })
  }

  function applySuggestion(sugg) {
    setParams({ q: sugg, page: '1' })
  }

  return (
    <div className="page search-page">
      <div className="page-intro">
        <span className="eyebrow">Discoverable Knowledge Library</span>
        <h1>Find any concept<br /><em>in the RPSC syllabus.</em></h1>
        <p>Search syllabus topics, published study notes, and reviewed source PDFs.</p>
      </div>

      <form className="large-search" onSubmit={submit} role="search">
        <span aria-hidden="true" className="search-icon">⌕</span>
        <input
          key={query}
          name="q"
          type="search"
          defaultValue={query}
          maxLength={200}
          aria-label="Search syllabus topics and published notes"
          placeholder="Try 'Palaeolithic', 'Kalibangan', 'Guhila', 'Monsoon'..."
          required
        />
        <button className="button primary" type="submit">Search →</button>
      </form>

      {query && !loading && data && (
        <div className="results-label">
          {data.total} {data.total === 1 ? 'match' : 'matches'} for <strong>“{query}”</strong>
        </div>
      )}

      {data?.suggestion && data.suggestion.toLowerCase() !== query.toLowerCase() && (
        <div className="search-suggestion-banner" role="status">
          <span className="suggestion-label">Did you mean:</span>{' '}
          <button
            type="button"
            className="suggestion-btn"
            onClick={() => applySuggestion(data.suggestion)}
          >
            {data.suggestion}
          </button>
          ?
        </div>
      )}

      {!query ? (
        <div className="search-suggestions">
          <span className="label">SUGGESTED STARTING POINTS</span>
          <div className="search-tags">
            {['Palaeolithic', 'Kalibangan', 'Aravalli Range', 'Monsoon', 'Prajamandal', 'Forts'].map(term => (
              <button
                type="button"
                key={term}
                className="search-tag-btn"
                onClick={() => applySuggestion(term)}
              >
                {term}
              </button>
            ))}
          </div>
          <div style={{ marginTop: '20px' }}>
            <Link to="/syllabus" className="text-link">Explore the Complete Syllabus →</Link>
          </div>
        </div>
      ) : loading ? (
        <Skeleton label="Searching syllabus topics and published notes…" />
      ) : error ? (
        <StatusPanel title="Search needs another moment." retry={retry}>
          Your query is still here. Please try again.
        </StatusPanel>
      ) : data?.results.length ? (
        <>
          <div className="search-results">
            {data.results.map(result => (
              <Link className="search-result" to={result.url} key={result.source_id}>
                <div className="result-header">
                  <span className={`result-type ${result.kind}`}>
                    {result.kind === 'pdf' ? 'PDF / PAGE' : result.has_notes ? 'VERIFIED NOTES' : 'SYLLABUS TOPIC'}
                  </span>
                  {!result.has_notes && result.kind === 'topic' && (
                    <span className="badge-in-prep">In editorial preparation</span>
                  )}
                </div>
                <div>
                  <div className="result-path">{result.path.join(' › ')}</div>
                  <h2>{result.title}</h2>
                  <p>{result.snippet}</p>
                </div>
                <span className="result-arrow" aria-hidden="true">↗</span>
              </Link>
            ))}
          </div>
          <nav className="pagination" aria-label="Search pages">
            <button
              className="button"
              disabled={page <= 1}
              onClick={() => setParams({ q: query, page: String(page - 1) })}
            >
              ← Previous
            </button>
            <span>Page {page} of {Math.max(1, Math.ceil(data.total / 20))}</span>
            <button
              className="button"
              disabled={!data.has_more}
              onClick={() => setParams({ q: query, page: String(page + 1) })}
            >
              Next →
            </button>
          </nav>
        </>
      ) : (
        <StatusPanel title="No match found">
          No syllabus topics or study notes matched <strong>“{query}”</strong>.
          <p style={{ marginTop: '12px' }}>
            Try checking spelling, searching for a broader term, or browsing by stream in the syllabus.
          </p>
          <div style={{ marginTop: '16px' }}>
            <Link to="/syllabus" className="button primary">
              Browse the Syllabus Tree →
            </Link>
          </div>
        </StatusPanel>
      )}
    </div>
  )
}
