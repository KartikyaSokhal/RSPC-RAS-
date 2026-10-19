import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import useResource from '../hooks/useResource.js'
import SyllabusTree from '../components/study/SyllabusTree.jsx'
import Skeleton from '../components/ui/Skeleton.jsx'
import StatusPanel from '../components/ui/StatusPanel.jsx'
import RajasthanMap from '../components/ui/RajasthanMap.jsx'

function filterTopics(items, query, filterStatus) {
  if (!query && filterStatus === 'all') return items

  return items.flatMap(item => {
    const children = filterTopics(item.children || [], query, filterStatus)
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

export default function Home() {
  const { data, loading, error, retry } = useResource('/topics/?tree=1')
  const [searchQuery, setSearchQuery] = useState('')
  const [activeStream, setActiveStream] = useState('all')
  const [filterStatus, setFilterStatus] = useState('all')

  const allTopics = useMemo(() => data || [], [data])
  const totalCount = useMemo(() => countTotalTopics(allTopics), [allTopics])
  const readyCount = useMemo(() => countReadyTopics(allTopics), [allTopics])

  const streamFilteredTopics = useMemo(() => {
    if (activeStream === 'all') return allTopics
    return allTopics.filter(t => String(t.id) === String(activeStream) || t.slug === activeStream)
  }, [allTopics, activeStream])

  const visibleTopics = useMemo(() => {
    return filterTopics(streamFilteredTopics, searchQuery, filterStatus)
  }, [streamFilteredTopics, searchQuery, filterStatus])

  return (
    <div className="page home-page">
      {/* HERO SECTION: LEFT COPY & CTAS | RIGHT RAJASTHAN MAP */}
      <section className="home-hero-grid" aria-labelledby="hero-title">
        <div className="hero-content-col">
          <span className="eyebrow">RPSC / RAS Examination Platform</span>
          <h1 id="hero-title" className="hero-title">
            Master the Rajasthan<br />
            <em>Administrative Services</em> Syllabus.
          </h1>
          <p className="hero-description">
            Study with clarity and perspective. Explore all 152 curriculum topics across Rajasthan history, Indian geography, and state administration with verified source notes and reviewed practice.
          </p>
          <div className="hero-cta-group">
            <a href="#syllabus-explorer" className="button primary hero-primary-btn">
              Explore Syllabus ↓
            </a>
            <Link to="/search" className="button hero-secondary-btn">
              Search Topics ⌕
            </Link>
          </div>
        </div>

        <div className="hero-visual-col" aria-hidden="true">
          <RajasthanMap className="home-rajasthan-graphic" />
        </div>
      </section>

      {/* COMPACT SUMMARY METRICS SECTION ABOVE SYLLABUS LIST */}
      <section className="syllabus-stats-summary" aria-label="Curriculum Overview Statistics">
        <div className="summary-stat-pill">
          <span className="pill-dot blue" />
          <span className="pill-label">Total Curriculum Topics:</span>
          <strong>{totalCount || 152}</strong>
        </div>
        <div className="summary-stat-pill">
          <span className="pill-dot amber" />
          <span className="pill-label">Core Streams:</span>
          <strong>{allTopics.length || 5} Subjects</strong>
        </div>
        <div className="summary-stat-pill">
          <span className="pill-dot green" />
          <span className="pill-label">Verified Notes Ready:</span>
          <strong>{readyCount || 10} Topics</strong>
        </div>
      </section>

      {/* SYLLABUS DIRECTORY EXPLORER */}
      <section className="syllabus-explorer-section" id="syllabus-explorer" aria-label="Syllabus Directory Explorer">
        <div className="explorer-filters-card">
          <div className="search-field full-width">
            <span aria-hidden="true">⌕</span>
            <input
              type="search"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="Filter topics (e.g., 'Guhila', 'Kalibangan', 'Palaeolithic', 'Monsoon')..."
              aria-label="Filter syllabus topics"
            />
            {searchQuery && (
              <button
                type="button"
                className="clear-search-btn"
                onClick={() => setSearchQuery('')}
                aria-label="Clear filter"
              >
                ✕
              </button>
            )}
          </div>

          <div className="filter-controls-row">
            {allTopics.length > 1 && (
              <div className="stream-tabs" role="tablist" aria-label="Syllabus curriculum streams">
                <button
                  type="button"
                  role="tab"
                  aria-selected={activeStream === 'all'}
                  className={`stream-tab ${activeStream === 'all' ? 'active' : ''}`}
                  onClick={() => setActiveStream('all')}
                >
                  All Streams ({totalCount || 152})
                </button>
                {allTopics.map(root => (
                  <button
                    type="button"
                    key={root.id}
                    role="tab"
                    aria-selected={activeStream === String(root.id)}
                    className={`stream-tab ${activeStream === String(root.id) ? 'active' : ''}`}
                    onClick={() => setActiveStream(String(root.id))}
                    title={root.title}
                  >
                    {root.title.length > 32 ? root.title.slice(0, 30) + '…' : root.title}
                  </button>
                ))}
              </div>
            )}

            <div className="status-toggle-group" role="group" aria-label="Filter by lesson preparation status">
              <button
                type="button"
                className={`status-toggle-btn ${filterStatus === 'all' ? 'active' : ''}`}
                onClick={() => setFilterStatus('all')}
              >
                All
              </button>
              <button
                type="button"
                className={`status-toggle-btn ${filterStatus === 'ready' ? 'active' : ''}`}
                onClick={() => setFilterStatus('ready')}
              >
                <span className="dot green" /> Notes ready
              </button>
              <button
                type="button"
                className={`status-toggle-btn ${filterStatus === 'prep' ? 'active' : ''}`}
                onClick={() => setFilterStatus('prep')}
              >
                <span className="dot gray" /> In preparation
              </button>
            </div>
          </div>
        </div>

        {/* TOPICS TREE LIST */}
        <div className="syllabus-tree-container">
          {loading ? (
            <Skeleton label="Loading verified syllabus topics…" />
          ) : error ? (
            <StatusPanel title="Syllabus directory is temporarily unreachable" retry={retry}>
              Unable to load the RPSC examination hierarchy. Please refresh or try again in a moment.
            </StatusPanel>
          ) : visibleTopics.length > 0 ? (
            <SyllabusTree topics={visibleTopics} activeTopicId={null} defaultExpandedDepth={1} />
          ) : (
            <div className="no-filter-results card">
              <p>No syllabus topics matched “{searchQuery}”.</p>
              <button
                type="button"
                className="button small"
                onClick={() => { setSearchQuery(''); setActiveStream('all'); setFilterStatus('all') }}
              >
                Reset Filters
              </button>
            </div>
          )}
        </div>
      </section>
    </div>
  )
}
