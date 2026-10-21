import { useEffect, useMemo, useRef, useState } from 'react'
import { Link, useLocation, useParams } from 'react-router-dom'
import useResource from '../hooks/useResource.js'
import useSyllabus from '../hooks/useSyllabus.js'
import SyllabusTree from '../components/study/SyllabusTree.jsx'
import TopicBreadcrumbs from '../components/study/TopicBreadcrumbs.jsx'
import ContentRenderer from '../components/study/ContentRenderer.jsx'
import TutorPanel from '../components/ai/TutorPanel.jsx'
import Skeleton from '../components/ui/Skeleton.jsx'
import StatusPanel from '../components/ui/StatusPanel.jsx'
import { LEARNER_FEATURES_UNAVAILABLE_MESSAGE } from '../learnerFeatures.js'

function filterSidebarTree(items, query) {
  if (!query) return items
  return items.flatMap(item => {
    const children = filterSidebarTree(item.children || [], query)
    const matches = item.title.toLowerCase().includes(query.toLowerCase())
    if (matches || children.length > 0) {
      return [{ ...item, children }]
    }
    return []
  })
}

function StudyWorkspace({ topic, roots }) {
  const [panel, setPanel] = useState('notes')
  const [selected, setSelected] = useState(null)
  const [sidebarFilter, setSidebarFilter] = useState('')
  const [chatOpen, setChatOpen] = useState(false)
  const launcher = useRef(null)
  const tutorPopup = useRef(null)
  const location = useLocation()


  useEffect(() => {
    if (!location.hash) return undefined
    const frame = requestAnimationFrame(() => {
      const anchor = document.getElementById(decodeURIComponent(location.hash.slice(1)))
      anchor?.focus({ preventScroll: true })
      anchor?.scrollIntoView({ block: 'center' })
    })
    return () => cancelAnimationFrame(frame)
  }, [location.hash, topic.slug])

  useEffect(() => {
    if (chatOpen) tutorPopup.current?.querySelector('button')?.focus({ preventScroll: true })
  }, [chatOpen])

  function closeTutor() {
    setChatOpen(false)
    launcher.current?.focus({ preventScroll: true })
  }

  function select(value) {
    setSelected(value)
    setChatOpen(true)
  }

  const filteredRoots = useMemo(() => {
    return filterSidebarTree(roots || [], sidebarFilter)
  }, [roots, sidebarFilter])

  const hasNotes = Boolean(topic.blocks && topic.blocks.length > 0)

  return (
    <>
      <div className="study-toolbar">
        <Link to="/syllabus" className="text-link">
          ← Full syllabus navigator
        </Link>
        <span className="toolbar-indicator">
          RPSC RAS STUDY WORKSPACE · {hasNotes ? 'ACTIVE LESSON' : 'SYLLABUS OUTLINE'}
        </span>
        <div className="toolbar-right-actions">
          {topic.has_quiz ? (
            <Link to={`/quiz/${topic.slug}`} className="text-link">
              Practice questions <span aria-hidden="true">↗</span>
            </Link>
          ) : (
            <span className="small text-muted">Untimed practice in prep</span>
          )}
        </div>
      </div>

      <div className="mobile-study-tabs" role="group" aria-label="Study panels">
        {[
          ['syllabus', 'Syllabus'],
          ['notes', hasNotes ? 'Reading' : 'Overview'],
        ].map(([key, label]) => (
          <button
            key={key}
            type="button"
            aria-pressed={panel === key}
            onClick={() => setPanel(key)}
          >
            {label}
          </button>
        ))}
      </div>

      <div className={`study-workspace show-${panel}`}>
        {/* LEFT PANEL: COMPLETE SYLLABUS DIRECTORY */}
        <aside className="study-sidebar" aria-label="Official syllabus outline">
          <div className="sidebar-header">
            <span className="eyebrow">Curriculum Navigator</span>
            <h2>Syllabus Tree</h2>
            <div className="sidebar-search-field">
              <input
                type="search"
                value={sidebarFilter}
                onChange={e => setSidebarFilter(e.target.value)}
                placeholder="Filter syllabus…"
                aria-label="Filter sidebar syllabus"
              />
            </div>
          </div>

          <div className="sidebar-tree-scroll">
            {filteredRoots?.length ? (
              <SyllabusTree topics={filteredRoots} originalTopics={roots} current={topic.slug} showControls />
            ) : (
              <p className="small">No matching syllabus sections.</p>
            )}
          </div>

          <div className="sidebar-footnote">
            <span aria-hidden="true">🏛️</span>
            <p>Official RPSC RAS syllabus hierarchy</p>
          </div>
        </aside>

        {/* CENTER PANEL: COMFORTABLE READING AREA */}
        <article className="study-reader">
          <TopicBreadcrumbs items={topic.breadcrumbs || [{ title: topic.title, slug: topic.slug }]} />

          <header className="reading-header">
            <span className="eyebrow">Official RPSC Syllabus Topic</span>
            <h1>{topic.title}</h1>
            <div className="reading-meta">
              <span>◷ Read at your pace</span>
              {hasNotes ? (
                <span className="status-badge notes-ready">● Verified study notes</span>
              ) : (
                <span className="status-badge coming-soon">○ Notes under editorial preparation</span>
              )}
            </div>

            <div className="topic-action-controls">
              <button
                type="button"
                className="topic-action-btn"
                disabled
                title="Bookmarks are unavailable in this release"
              >
                <span aria-hidden="true">☆</span> Bookmark Topic
              </button>

              <button
                type="button"
                className="topic-action-btn"
                disabled
                title="Completion tracking is unavailable in this release"
              >
                <span aria-hidden="true">○</span> Mark as Completed
              </button>
            </div>

            <p className="topic-action-feedback" role="status">{LEARNER_FEATURES_UNAVAILABLE_MESSAGE}</p>
          </header>


          {/* If published notes exist */}
          {hasNotes && (
            <>
              <ContentRenderer
                blocks={topic.blocks}
                revision={topic.revision}
                keywordLinks={topic.keyword_links || []}
                onSelection={select}
              />

              {topic.resources?.length > 0 && (
                <section className="lesson-resources">
                  <span className="eyebrow">Archival & Primary Sources</span>
                  <h2>Primary Documents & Field Guides</h2>
                  {topic.resources.map(resource => (
                    <Link className="resource-card" to={resource.url} key={resource.id}>
                      <span className="pdf-badge">PDF</span>
                      <div>
                        <h3>{resource.title}</h3>
                        <p>{resource.page_count} pages · Primary text & citation viewer</p>
                      </div>
                      <span aria-hidden="true">↗</span>
                    </Link>
                  ))}
                </section>
              )}

              {topic.related?.length > 0 && (
                <section className="related-lessons">
                  <h2>Related Topics</h2>
                  {topic.related.map(item => (
                    <Link to={`/topic/${item.slug}`} key={item.slug}>
                      <span className="label">
                        {item.kind === 'prerequisite' ? 'FOUNDATIONAL PREREQUISITE' : 'CONNECTED LESSON'}
                      </span>
                      <h3>{item.title} <span aria-hidden="true">→</span></h3>
                      <p>{item.reason}</p>
                    </Link>
                  ))}
                </section>
              )}

              <section className="practice-callout">
                <span className="practice-symbol" aria-hidden="true">✎</span>
                <div>
                  <h3>Check your understanding.</h3>
                  <p>Untimed practice challenge with immediate explanations and retries.</p>
                </div>
                <Link className="button primary" to={`/quiz/${topic.slug}`}>
                  Practice this lesson →
                </Link>
              </section>
            </>
          )}

          {/* If notes are NOT yet published ("Coming Soon") */}
          {!hasNotes && (
            <div className="coming-soon-panel">
              <div className="coming-soon-icon" aria-hidden="true">🏛️</div>
              <h2>Notes Under Editorial Preparation</h2>
              <p className="empty-note">No learning material has been published for this lesson yet.</p>
              <p className="coming-soon-lead">
                Verified study notes for <strong>{topic.title}</strong> are being compiled according to
                official RPSC examination benchmarks.
              </p>
              <p className="small text-muted">
                Every syllabus topic remains permanently discoverable within the curriculum outline.
                You can explore subtopics below or study available lessons in the library.
              </p>

              {topic.children?.length > 0 && (
                <section className="coming-soon-children">
                  <div className="section-heading">
                    <h3>Subtopics in this unit ({topic.children.length})</h3>
                  </div>
                  <div className="subtopic-links-list">
                    {topic.children.map((child, index) => (
                      <Link to={`/topic/${child.slug}`} key={child.slug} className="subtopic-link-row">
                        <span className="subtopic-index">{String(index + 1).padStart(2, '0')}.</span>
                        <span className="subtopic-title">{child.title}</span>
                        <span className="subtopic-tag">
                          {child.has_notes ? '● Notes ready' : '○ In prep'}
                        </span>
                        <span aria-hidden="true">↗</span>
                      </Link>
                    ))}
                  </div>
                </section>
              )}

              <div className="coming-soon-actions">
                <Link to="/syllabus" className="button">
                  ← Browse full syllabus directory
                </Link>
                <Link to="/topic/1-pre-historical-sites-of-rajasthan" className="button primary">
                  Study ready Rajasthan history notes →
                </Link>
              </div>
            </div>
          )}

          {topic.tags?.length > 0 && <nav className="article-tags" aria-label="Article tags">{topic.tags.map(tag => <Link className="button" key={tag.id} to={`/tags/${encodeURIComponent(tag.slug)}`}>{tag.name}</Link>)}</nav>}
          {topic.is_published && <p><Link className="text-link" to={`/practice/${topic.slug}`}>Practice this syllabus unit →</Link></p>}
          <p className="privacy-note">
            Reading and practice are available without a student account. Quiz results stay in this page.
          </p>

        </article>

      </div>

      {/* FLOATING AI TUTOR LAUNCHER BUTTON */}
      <button
        ref={launcher}
        type="button"
        className={`floating-tutor-launcher ${chatOpen ? 'active' : ''}`}
        onClick={() => chatOpen ? closeTutor() : setChatOpen(true)}
        onKeyDown={event => { if (event.key === 'Escape' && chatOpen) closeTutor() }}
        aria-controls={chatOpen ? 'study-tutor-popup' : undefined}
        aria-haspopup="dialog"
        aria-label={chatOpen ? 'Hide AI Tutor' : 'Ask AI Tutor'}
        aria-expanded={chatOpen}
      >
        <span className="spark-icon" aria-hidden="true">✨</span>
        <span className="launcher-text">{chatOpen ? 'Close AI Tutor' : 'Ask AI Tutor'}</span>
        {selected && !chatOpen && <span className="launcher-badge">Passage selected</span>}
      </button>

      {/* FLOATING AI TUTOR POPUP DIALOG */}
      {chatOpen && (
        <aside ref={tutorPopup} id="study-tutor-popup" className="floating-tutor-popup" role="dialog" aria-labelledby="tutor-heading" onKeyDown={event => { if (event.key === 'Escape') { event.preventDefault(); closeTutor() } }}>
          <TutorPanel
            topic={topic}
            selected={selected}
            clearSelection={() => setSelected(null)}
            onCitation={() => {}}
            onClose={closeTutor}
          />
        </aside>
      )}
    </>
  )
}

export default function TopicPage() {
  const { slug } = useParams()
  const { data, loading, error, retry } = useResource(`/topic/${encodeURIComponent(slug)}/`)
  const { data: roots } = useSyllabus()

  if (loading) return <div className="page"><Skeleton label="Opening syllabus topic…" /></div>
  if (error || !data) {
    return (
      <div className="page">
        <StatusPanel
          title={error?.response?.status === 404 ? 'This lesson is not available.' : 'The lesson could not load.'}
          retry={error?.response?.status !== 404 ? retry : undefined}
        >
          Check the syllabus navigator to explore available topics.
        </StatusPanel>
      </div>
    )
  }

  return <StudyWorkspace key={slug} topic={data} roots={roots} />
}
