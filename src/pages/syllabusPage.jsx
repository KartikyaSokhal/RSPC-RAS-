import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import useSyllabus from '../hooks/useSyllabus.js'
import SyllabusTree from '../components/study/SyllabusTree.jsx'
import Skeleton from '../components/ui/Skeleton.jsx'
import StatusPanel from '../components/ui/StatusPanel.jsx'

function filterTree(items, query, filterStatus) {
  if (!query && filterStatus === 'all') return items

  return items.flatMap(item => {
    const children = filterTree(item.children || [], query, filterStatus)
    const matchesQuery = !query || item.title.toLowerCase().includes(query.toLowerCase())
    const matchesStatus =
      filterStatus === 'all' ||
      (filterStatus === 'ready' && (item.has_notes || children.some(c => c.has_notes))) ||
      (filterStatus === 'prep' && (!item.has_notes || children.some(c => !c.has_notes)))

    if (matchesQuery && matchesStatus) {
      return [{ ...item, children }]
    }
    if (children.length > 0) {
      return [{ ...item, children }]
    }
    return []
  })
}

function countTotalTopics(nodes) {
  let count = 0
  for (const n of nodes) {
    count += 1
    if (n.children?.length) {
      count += countTotalTopics(n.children)
    }
  }
  return count
}

function countReadyTopics(nodes) {
  let count = 0
  for (const n of nodes) {
    if (n.has_notes) count += 1
    if (n.children?.length) {
      count += countReadyTopics(n.children)
    }
  }
  return count
}

function hierarchyDepth(nodes) {
  return nodes.length ? 1 + Math.max(...nodes.map(node => hierarchyDepth(node.children || []))) : 0
}

export default function SyllabusPage() {
  const { data, loading, error, retry } = useSyllabus()
  const [query, setQuery] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')

  const allTopics = useMemo(() => data || [], [data])
  const totalCount = useMemo(() => countTotalTopics(allTopics), [allTopics])
  const readyCount = useMemo(() => countReadyTopics(allTopics), [allTopics])
  const depth = useMemo(() => hierarchyDepth(allTopics), [allTopics])
  const countsAvailable = !loading && !error && Array.isArray(data)
  const displayCount = value => countsAvailable ? value : loading ? 'Loading…' : 'Unavailable'

  const filteredTopics = useMemo(() => {
    return filterTree(allTopics, query.trim().toLowerCase(), filterStatus)
  }, [allTopics, query, filterStatus])

  return (
    <div className="page syllabus-page">
      <div className="page-intro">
        <span className="eyebrow">RPSC / RAS Examination Outline</span>
        <h1>The Complete Syllabus.<br /><em>A clear, structured path forward.</em></h1>
        <p>
          {countsAvailable
            ? `Explore ${totalCount} curriculum ${totalCount === 1 ? 'topic' : 'topics'} organized into ${allTopics.length} ${allTopics.length === 1 ? 'stream' : 'streams'}. `
            : 'Explore the curriculum hierarchy. Counts will appear when the outline is available. '}
          Topics with published learning material are marked accordingly; remaining syllabus entries display their
          exact position and subtopics while notes remain in editorial preparation.
        </p>
      </div>

      {/* PROMINENT TOPIC COUNTS COMPACT SUMMARY ABOVE SYLLABUS LIST */}
      <section className="syllabus-stats-summary above-syllabus" aria-label="Syllabus topic summary">
        <div className="summary-stat-pill">
          <span className="pill-dot blue" />
          <span className="pill-label">Total Syllabus Topics:</span>
          <strong>{displayCount(totalCount)}</strong>
        </div>
        <div className="summary-stat-pill">
          <span className="pill-dot amber" />
          <span className="pill-label">Main Curriculum Streams:</span>
          <strong>{displayCount(allTopics.length)}{countsAvailable && ' Streams'}</strong>
        </div>
        <div className="summary-stat-pill">
          <span className="pill-dot green" />
          <span className="pill-label">Topics with Published Notes:</span>
          <strong>{displayCount(readyCount)}{countsAvailable && ' Ready'}</strong>
        </div>
      </section>

      <div className="syllabus-layout">
        <aside className="collection-note">
          <span className="eyebrow">Curriculum Scope</span>
          <h2>Official Examination Structure</h2>
          <p>
            The RPSC RAS examination tests candidates across Rajasthan history, Indian history, and global/Indian geography.
          </p>

          <div className="syllabus-stats-box">
            <div className="stat-line">
              <span>Total topics:</span>
              <strong>{displayCount(totalCount)}</strong>
            </div>
            <div className="stat-line">
              <span>Core streams:</span>
              <strong>{displayCount(allTopics.length)}</strong>
            </div>
            <div className="stat-line">
              <span>Hierarchy levels:</span>
              <strong>{displayCount(depth)}</strong>
            </div>
          </div>

          <div className="note-divider" />

          <p className="small">Looking for a specific term inside published notes or primary PDFs?</p>
          <Link className="text-link" to="/search">
            Search the full library <span aria-hidden="true">→</span>
          </Link>
        </aside>

        <section className="syllabus-browser">
          <div className="browser-header-tools">
            <label className="search-field">
              <span aria-hidden="true">⌕</span>
              <input
                type="search"
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="Filter subjects, dynasties, eras and concepts…"
                aria-label="Filter syllabus"
              />
              {query && (
                <button
                  type="button"
                  className="clear-search-btn"
                  onClick={() => setQuery('')}
                  aria-label="Clear filter"
                >
                  ✕
                </button>
              )}
            </label>

            <div className="status-filter-group" role="group" aria-label="Filter topics by status">
              <button
                type="button"
                className={`filter-pill ${filterStatus === 'all' ? 'active' : ''}`}
                onClick={() => setFilterStatus('all')}
                disabled={!countsAvailable}
              >
                All ({displayCount(totalCount)})
              </button>
              <button
                type="button"
                className={`filter-pill ${filterStatus === 'ready' ? 'active' : ''}`}
                onClick={() => setFilterStatus('ready')}
                disabled={!countsAvailable}
              >
                ● Notes ready ({displayCount(readyCount)})
              </button>
              <button
                type="button"
                className={`filter-pill ${filterStatus === 'prep' ? 'active' : ''}`}
                onClick={() => setFilterStatus('prep')}
                disabled={!countsAvailable}
              >
                ○ In preparation ({displayCount(Math.max(0, totalCount - readyCount))})
              </button>
            </div>
          </div>

          {loading ? (
            <Skeleton label="Loading syllabus topics…" />
          ) : error ? (
            <StatusPanel title="Syllabus outline needs another moment." retry={retry}>
              We were unable to load the syllabus structure. Please try again.
            </StatusPanel>
          ) : filteredTopics.length ? (
            <SyllabusTree topics={filteredTopics} originalTopics={allTopics} showControls />
          ) : (
            <div className="syllabus-empty card">
              <p>No topics match “{query}”.</p>
              <button
                type="button"
                className="button small"
                onClick={() => { setQuery(''); setFilterStatus('all') }}
              >
                Clear Filters
              </button>
            </div>
          )}
        </section>
      </div>
    </div>
  )
}
