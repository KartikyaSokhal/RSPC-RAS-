import { useEffect, useRef, useState } from 'react'
import { Link, NavLink, Outlet, useLocation } from 'react-router-dom'
import useTheme from '../../hooks/useTheme.js'
import useResource from '../../hooks/useResource.js'
import useAuth from '../../hooks/useAuth.js'
import { PlatformContext } from './platformContext.js'

export default function AppShell() {
  const { theme, toggleTheme } = useTheme()
  const { data: config } = useResource('/config/')
  const { user, authenticated, logout } = useAuth()
  const location = useLocation()
  const main = useRef(null)
  const previousRoute = useRef(location.pathname)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

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
      <a className="skip-link" href="#main-content">Skip to content</a>

      {config?.demo && (
        <div className="demo-banner">
          <span className="live-dot" />
          <span>RPSC / RAS Academic Edition · Verified Syllabus Hierarchy (152 Topics) · AI Tutor Grounded in Sources</span>
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

          {/* DESKTOP NAVIGATION */}
          <nav className="desktop-nav" aria-label="Main navigation">
            <NavLink to="/syllabus" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
              Syllabus
            </NavLink>
            <NavLink to="/search" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
              Search
            </NavLink>
            <NavLink to="/about" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
              About
            </NavLink>
          </nav>

          {/* HEADER CONTROLS & AUTH */}
          <div className="header-controls">
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

            {/* AUTH ACTIONS */}
            {authenticated ? (
              <div className="user-menu-group">
                <NavLink to="/dashboard" className="nav-profile-pill" title="My Learning Dashboard">
                  <span className="user-avatar-initial" aria-hidden="true">
                    {(user?.name || user?.username || 'S')[0].toUpperCase()}
                  </span>
                  <span className="user-name-text">Dashboard</span>
                </NavLink>
                <button
                  type="button"
                  onClick={logout}
                  className="nav-logout-btn"
                  title="Sign out of student account"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="auth-nav-group">
                <Link to="/login" className="nav-login-link">
                  Sign in
                </Link>
                <Link to="/signup" className="button primary small nav-signup-btn">
                  Sign up
                </Link>
              </div>
            )}

            {/* MOBILE HAMBURGER BUTTON */}
            <button
              type="button"
              className="mobile-menu-toggle"
              aria-label={mobileMenuOpen ? 'Close navigation menu' : 'Open navigation menu'}
              aria-expanded={mobileMenuOpen}
              onClick={() => setMobileMenuOpen(prev => !prev)}
            >
              <span className={`hamburger-bar ${mobileMenuOpen ? 'open' : ''}`} />
            </button>
          </div>
        </div>

        {/* MOBILE MENU DRAWER */}
        {mobileMenuOpen && (
          <nav className="mobile-nav-drawer" aria-label="Mobile navigation">
            <NavLink to="/syllabus" className="mobile-nav-link" onClick={() => setMobileMenuOpen(false)}>
              Syllabus
            </NavLink>
            <NavLink to="/search" className="mobile-nav-link" onClick={() => setMobileMenuOpen(false)}>
              Search
            </NavLink>
            <NavLink to="/about" className="mobile-nav-link" onClick={() => setMobileMenuOpen(false)}>
              About & Scope
            </NavLink>
            {authenticated ? (
              <>
                <NavLink to="/dashboard" className="mobile-nav-link" onClick={() => setMobileMenuOpen(false)}>
                  My Dashboard
                </NavLink>
                <button
                  type="button"
                  onClick={() => { logout(); setMobileMenuOpen(false) }}
                  className="mobile-nav-link logout"
                >
                  Sign Out
                </button>
              </>
            ) : (
              <div className="mobile-auth-actions">
                <Link to="/login" className="button full-width" onClick={() => setMobileMenuOpen(false)}>
                  Sign In
                </Link>
                <Link to="/signup" className="button primary full-width" onClick={() => setMobileMenuOpen(false)}>
                  Sign Up
                </Link>
              </div>
            )}
          </nav>
        )}
      </header>

      <main id="main-content" ref={main} tabIndex={-1} className="main-content">
        <Outlet />
      </main>

      <footer className="site-footer">
        <div>
          <Link className="brand footer-brand" to="/">
            prepal<span className="brand-dot">.</span>
          </Link>
          <p className="footer-tagline">Academic syllabus study library for Rajasthan Administrative Services (RAS).</p>
        </div>
        <p className="footer-center">152 Curriculum Topics · Source-Grounded Notes · AI Study Companion</p>
        <nav aria-label="Footer">
          <Link to="/syllabus">Syllabus</Link>
          <Link to="/search">Search</Link>
          <Link to="/about">About & Methodology</Link>
          <Link to="/help">Help & Privacy</Link>
        </nav>
        <small>Designed for RPSC RAS candidates. Independent academic study resource; not affiliated with the government examination authority.</small>
      </footer>
    </PlatformContext.Provider>
  )
}
