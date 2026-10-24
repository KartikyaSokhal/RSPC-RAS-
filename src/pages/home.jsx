import { useMemo } from 'react'
import useSyllabus from '../hooks/useSyllabus.js'
import { indexSyllabus } from '../components/study/syllabusUtils.js'
import SyllabusTree from '../components/study/SyllabusTree.jsx'
import Skeleton from '../components/ui/Skeleton.jsx'
import StatusPanel from '../components/ui/StatusPanel.jsx'
import RajasthanMap from '../components/ui/RajasthanMap.jsx'

export default function Home() {
  const { data, loading, error, retry } = useSyllabus()
  const topics = useMemo(() => data || [], [data])
  const totalCount = useMemo(() => indexSyllabus(topics).size, [topics])
  const countsReady = !loading && !error && data !== null

  function jumpToSubject(id) {
    const root = document.getElementById(`home-subject-${id}`)
    root?.scrollIntoView({ block: 'start' })
    root?.querySelector('summary,a')?.focus({ preventScroll: true })
  }

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
            Explore the RPSC/RAS syllabus, published study notes and reviewed practice. Ask the AI assistant for help understanding available lesson sources, and check its citations.
          </p>
          <div className="hero-cta-group">
            <a href="#syllabus-explorer" className="button primary hero-primary-btn">
              Explore Syllabus ↓
            </a>
          </div>
        </div>

        <div className="hero-visual-col" aria-hidden="true">
          <RajasthanMap className="home-rajasthan-graphic" />
        </div>
      </section>

      <section className="syllabus-stats-summary" aria-label="Curriculum Overview Statistics" aria-busy={loading}>
        <div className="summary-stat-pill"><span className="pill-dot blue" aria-hidden="true" /><span className="pill-label">Total Curriculum Topics:</span><strong>{countsReady ? totalCount : '—'}</strong></div>
        <div className="summary-stat-pill"><span className="pill-dot amber" aria-hidden="true" /><span className="pill-label">Core Subjects:</span><strong>{countsReady ? topics.length : '—'}</strong></div>
      </section>
      <section className="syllabus-explorer-section" id="syllabus-explorer" aria-label="Syllabus Directory Explorer">
        {loading ? <Skeleton label="Loading syllabus topics…" /> : error ? (
          <StatusPanel title="Syllabus directory is temporarily unreachable" retry={retry}>Unable to load the RPSC examination hierarchy. Please refresh or try again in a moment.</StatusPanel>
        ) : topics.length ? <>
          <nav className="subject-navigation" aria-label="Jump to a subject">
            {topics.map((root, i) => <button className="button subject-nav-button" key={root.id} type="button" onClick={() => jumpToSubject(root.id)} aria-controls={`home-subject-${root.id}`}>{i + 1}. {root.title}</button>)}
          </nav>
          <SyllabusTree topics={topics} showControls rootAnchorPrefix="home-subject" />
        </> : <p className="notice">The syllabus outline is not available yet.</p>}
      </section>
    </div>
  )
}
