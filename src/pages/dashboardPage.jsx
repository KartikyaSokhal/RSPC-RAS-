import { Link } from 'react-router-dom'
import useAuth from '../hooks/useAuth.js'
import useResource from '../hooks/useResource.js'
import Skeleton from '../components/ui/Skeleton.jsx'
import StatusPanel from '../components/ui/StatusPanel.jsx'

export default function DashboardPage() {
  const { user, authenticated, loading: authLoading } = useAuth()
  const { data: dashboard, loading: dashLoading, error, retry } = useResource(
    authenticated ? '/dashboard/' : null
  )

  if (authLoading) {
    return <div className="page dashboard-page"><Skeleton label="Loading your student profile…" /></div>
  }

  if (!authenticated) {
    return (
      <div className="page dashboard-page">
        <div className="page-intro">
          <span className="eyebrow">Student Learning Dashboard</span>
          <h1>Your Personal Study Workspace</h1>
          <p>Sign in or create a student account to track syllabus completion, save bookmarks, and view your quiz practice records.</p>
        </div>
        <div className="dashboard-auth-prompt card">
          <div className="auth-prompt-content">
            <span className="brand-mark small" aria-hidden="true">p<span>·</span></span>
            <h2>Sign in to see your learning progress</h2>
            <p>Every student's progress is saved securely and privately in their own account.</p>
            <div className="auth-prompt-actions">
              <Link to="/login" className="button primary">Sign In →</Link>
              <Link to="/signup" className="button">Create Account</Link>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (dashLoading) {
    return <div className="page dashboard-page"><Skeleton label="Loading your personalized dashboard…" /></div>
  }

  if (error) {
    return (
      <div className="page dashboard-page">
        <StatusPanel title="Unable to load dashboard." retry={retry}>
          We couldn't load your study records right now. Please try again.
        </StatusPanel>
      </div>
    )
  }

  const { stats, bookmarks, completed_topics, quiz_attempts, suggested_next } = dashboard || {}

  return (
    <div className="page dashboard-page">
      {/* WELCOME SECTION */}
      <header className="dashboard-header">
        <div className="dashboard-welcome">
          <span className="eyebrow">Student Dashboard</span>
          <h1>Welcome back, {user?.name || user?.username}</h1>
          <p className="welcome-subtitle">
            Rajasthan Administrative Services (RPSC RAS) Academic Preparation.
          </p>
        </div>
        <div className="dashboard-header-actions">
          <Link className="button" to="/planner">Create Study Plan</Link>
          <Link to={dashboard?.continue_studying ? `/topic/${dashboard.continue_studying.slug}` : "/syllabus"} className="button primary">
            Continue Studying →
          </Link>
        </div>
      </header>

      {/* METRICS / STATS OVERVIEW */}
      <section className="dashboard-stats-grid" aria-label="Learning Progress Overview">
        <div className="stat-card">
          <span className="stat-label">Syllabus Progress</span>
          <div className="stat-value">{stats?.total_completed || 0} <span className="stat-total">/ {stats?.total_topics ?? 0}</span></div>
          <div className="stat-bar-track">
            <div
              className="stat-bar-fill"
              style={{ width: `${Math.min(100, stats?.progress_percentage || 0)}%` }}
            />
          </div>
          <span className="stat-subtext">{stats?.progress_percentage || 0}% topics completed</span>
        </div>

        <div className="stat-card">
          <span className="stat-label">Bookmarked Topics</span>
          <div className="stat-value">{stats?.total_bookmarks || 0}</div>
          <span className="stat-subtext">Saved for quick revision</span>
        </div>

        <div className="stat-card">
          <span className="stat-label">Practice Tests Taken</span>
          <div className="stat-value">{stats?.total_quizzes_taken || 0}</div>
          <span className="stat-subtext">
            {stats?.total_quizzes_taken > 0 ? 'Verified practice attempts' : 'No tests attempted yet'}
          </span>
        </div>

        <div className="stat-card">
          <span className="stat-label">Average Quiz Accuracy</span>
          <div className="stat-value">
            {stats?.average_quiz_accuracy !== null && stats?.average_quiz_accuracy !== undefined
              ? `${stats.average_quiz_accuracy}%`
              : '—'}
          </div>
          <span className="stat-subtext">Across completed assessments</span>
        </div>
      </section>

      {/* TWO-COLUMN LAYOUT: MAIN & SIDEBAR */}
      <div className="dashboard-layout">
        <div className="dashboard-main-col">
          <section className="dashboard-section" aria-label="Subject completion">
            <h2>Subject completion</h2><p className="form-hint">{dashboard?.counting_rule}</p>
            {dashboard?.subject_progress?.map(subject => <div key={subject.id} className="card subject-progress"><Link to={`/topic/${subject.slug}`}>{subject.title}</Link><p>{subject.completed} / {subject.total} learning units · {subject.percentage}%</p><progress aria-label={`${subject.title} completion`} value={subject.completed} max={subject.total || 1} /></div>)}
            {!dashboard?.subject_progress?.length && <p>Published learning units will appear here when available.</p>}
          </section>
          <section className="dashboard-section" aria-label="Recently accessed topics"><h2>Recently accessed</h2>{dashboard?.recent_activity?.length ? dashboard.recent_activity.map(topic => <p key={topic.id}><Link to={`/topic/${topic.slug}`}>{topic.title}</Link></p>) : <p>Open a published lesson to start your reading history.</p>}</section>

          <section className="dashboard-section" aria-label="Study targets"><h2>Study targets</h2>{dashboard?.study_plans?.length ? <><p><Link to="/planner">Edit your study plans</Link></p>{dashboard.weekly_targets?.slice(0, 4).map(target => <p key={target.week}>{target.week}: {target.completed_minutes} / {target.minutes} minutes</p>)}{dashboard.monthly_targets?.slice(0, 3).map(target => <p key={target.month}>{target.month}: {target.completed_minutes} / {target.minutes} minutes; {target.completed_units} / {target.learning_units} planned units finished</p>)}</> : <p>Create a study plan to set weekly and monthly targets.</p>}</section>
          {/* SUGGESTED NEXT TOPICS */}
          {suggested_next && suggested_next.length > 0 && (
            <section className="dashboard-section" aria-label="Suggested Next Topics">
              <div className="section-header">
                <h2>Suggested Next Topics</h2>
                <span className="section-note">Deterministic curriculum sequence</span>
              </div>
              <div className="suggested-topics-list">
                {suggested_next.map(topic => (
                  <Link key={topic.id} to={`/topic/${topic.slug}`} className="suggested-topic-card">
                    <div>
                      <span className="topic-stream-badge">Curriculum Stream</span>
                      <h3>{topic.title}</h3>
                    </div>
                    <span className="card-arrow" aria-hidden="true">→</span>
                  </Link>
                ))}
              </div>
            </section>
          )}

          {/* BOOKMARKS LIST */}
          <section className="dashboard-section" aria-label="Your Bookmarks">
            <div className="section-header">
              <h2>Saved Bookmarks</h2>
              <span className="badge-count">{bookmarks?.length || 0}</span>
            </div>
            {bookmarks && bookmarks.length > 0 ? (
              <div className="bookmarks-list">
                {bookmarks.map(bm => (
                  <Link key={bm.id} to={`/topic/${bm.slug}`} className="bookmark-item">
                    <div>
                      <h3>{bm.title}</h3>
                      <span className="item-date">
                        Saved {new Date(bm.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
                      </span>
                    </div>
                    <span className="card-arrow" aria-hidden="true">→</span>
                  </Link>
                ))}
              </div>
            ) : (
              <div className="empty-box card">
                <p>No bookmarks saved yet.</p>
                <small>While exploring any topic, click the "Bookmark" button to save it here for fast revision.</small>
              </div>
            )}
          </section>

          {/* COMPLETED TOPICS */}
          <section className="dashboard-section" aria-label="Completed Topics">
            <div className="section-header">
              <h2>Completed Topics</h2>
              <span className="badge-count">{completed_topics?.length || 0}</span>
            </div>
            {completed_topics && completed_topics.length > 0 ? (
              <div className="completed-list">
                {completed_topics.map(ct => (
                  <Link key={ct.topic_id} to={`/topic/${ct.slug}`} className="completed-item">
                    <span className="check-icon" aria-hidden="true">✓</span>
                    <div>
                      <h3>{ct.title}</h3>
                      <span className="item-date">
                        Completed {new Date(ct.last_read_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
                      </span>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <div className="empty-box card">
                <p>No completed topics yet.</p>
                <small>When you finish studying a topic or lesson, mark it as completed to track your mastery.</small>
              </div>
            )}
          </section>
        </div>

        {/* SIDEBAR: RECENT QUIZ PERFORMANCE */}
        <aside className="dashboard-sidebar-col">
          <section className="dashboard-section" aria-label="Subject practice accuracy"><h2>Subject practice accuracy</h2>{dashboard?.subject_performance?.length ? dashboard.subject_performance.map(subject => <p key={subject.subject_id}>{subject.title}: {subject.correct} / {subject.total} correct ({subject.accuracy}%)</p>) : <p>Complete reviewed practice to see subject performance.</p>}</section>
          <section className="dashboard-section" aria-label="Recent Quiz Performance">
            <div className="section-header">
              <h2>Recent Practice</h2>
            </div>
            {quiz_attempts && quiz_attempts.length > 0 ? (
              <div className="quiz-history-list">
                {quiz_attempts.map(att => (
                  <div key={att.id} className="quiz-history-card">
                    <div className="quiz-history-top">
                      <Link className="quiz-title" to={`/attempts/${att.id}`}>{att.quiz_title}</Link>
                      <span className={`quiz-score-pill ${att.percentage >= 70 ? 'good' : 'fair'}`}>
                        {att.score} / {att.total_questions} ({att.percentage}%)
                      </span>
                    </div>
                    <Link to={`/topic/${att.topic_slug}`} className="quiz-topic-link">
                      Topic: {att.topic_title}
                    </Link>
                    <span className="quiz-date">
                      {new Date(att.attempted_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-box card">
                <p>No quiz attempts yet.</p>
                <small>Untimed practice quizzes are available on lessons with reviewed question banks.</small>
              </div>
            )}
          </section>
        </aside>
      </div>
    </div>
  )
}
