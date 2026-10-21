import { useEffect, useMemo, useRef } from 'react'
import { Link, Outlet, useLocation } from 'react-router-dom'
import useTheme from '../../hooks/useTheme.js'
import useResource from '../../hooks/useResource.js'
import { PlatformContext } from './platformContext.js'
import { SyllabusContext } from '../study/syllabusContext.js'
import { indexSyllabus } from '../study/syllabusUtils.js'

export default function AppShell() {
  const { theme, toggleTheme } = useTheme()
  const { data: config } = useResource('/config/')
  const syllabus = useResource('/topics/?tree=1')
  const totalTopics = useMemo(() => syllabus.data ? indexSyllabus(syllabus.data).size : null, [syllabus.data])
  const location = useLocation()
  const main = useRef(null)
  const previousRoute = useRef(location.pathname)

  // Scroll to top or anchor on navigation
  useEffect(() => {
    const navigated = previousRoute.current !== location.pathname
    previousRoute.current = location.pathname
    if (!navigated && !location.hash) return undefined
    const frame = requestAnimationFrame(() => {
      if (location.hash) {
        document.getElementById(decodeURIComponent(location.hash.slice(1)))?.scrollIntoView({ block: 'center' })
      } else if (!document.activeElement?.matches('input,textarea,select,button')) {
        window.scrollTo({ top: 0, behavior: 'instant' })
        main.current?.focus({ preventScroll: true })
      }
    })
    return () => cancelAnimationFrame(frame)
  }, [location.pathname, location.hash])

  return (
    <PlatformContext.Provider value={config || {}}>
      <SyllabusContext.Provider value={syllabus}>
      <a className="skip-link" href="#main-content">Skip to content</a>

      {config?.demo && (
        <div className="demo-banner">
          <span className="live-dot" />
          <span>RPSC / RAS Academic Edition · Synthetic demonstration content · Source-grounded AI assistant</span>
        </div>
      )}

      <header className="site-header">
        <div className="header-inner">
          {/* BRAND */}
          <Link to="/" className="brand" aria-label="Prepal home">
            <span className="brand-mark" aria-hidden="true">
              p<span>·</span>
            </span>
            <span className="brand-text-wrap">
              <span className="brand-name">prepal<span className="brand-dot">.</span></span>
              <span className="brand-badge">RPSC RAS</span>
            </span>
          </Link>

          <div className="header-controls">
            <Link className="button primary header-search-button" to="/search">Search <span aria-hidden="true">⌕</span></Link>
            {/* COMPACT SUN/MOON THEME TOGGLE */}
            <button
              type="button"
              className="theme-toggle-btn"
              onClick={toggleTheme}
              aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}
              title={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}
            >
              {theme === 'light' ? (
                /* Moon Icon for switching to dark */
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
                </svg>
              ) : (
                /* Sun Icon for switching to light */
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <circle cx="12" cy="12" r="5" />
                  <line x1="12" y1="1" x2="12" y2="3" />
                  <line x1="12" y1="21" x2="12" y2="23" />
                  <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
                  <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
                  <line x1="1" y1="12" x2="3" y2="12" />
                  <line x1="21" y1="12" x2="23" y2="12" />
                  <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
                  <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
                </svg>
              )}
            </button>

          </div>
        </div>
      </header>

      <main id="main-content" ref={main} tabIndex={-1} className="main-content">
        <Outlet />
      </main>

      <footer className="site-footer">
        <div>
          <Link className="brand footer-brand" to="/">
            prepal<span className="brand-dot">.</span>
          </Link>
          <p className="footer-tagline">Prepal Academic Syllabus · Rajasthan Administrative Services (RAS).</p>
        </div>
        <div className="footer-center" aria-label="Syllabus statistics" aria-busy={syllabus.loading}>
          {syllabus.loading ? <p>Loading syllabus statistics…</p> : syllabus.error ? <p>Syllabus statistics are temporarily unavailable.</p> : <p>{syllabus.data?.length} Subjects · {totalTopics} Curriculum Topics</p>}
          <div className="footer-social-space" aria-hidden="true" />
        </div>
        <nav aria-label="Footer">
          <Link to="/syllabus">Syllabus</Link>
          <Link to="/search">Search</Link>
          <Link to="/help">Help & Privacy</Link>
        </nav>
        <small>Designed for RPSC RAS candidates. Independent academic study resource; not affiliated with the government examination authority.</small>
      </footer>
      </SyllabusContext.Provider>
    </PlatformContext.Provider>
  )
}
