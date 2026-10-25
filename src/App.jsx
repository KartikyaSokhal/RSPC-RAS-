import { Component, lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import AppShell from './components/layout/AppShell.jsx'
import Skeleton from './components/ui/Skeleton.jsx'
import './App.css'
import useAuth from './hooks/useAuth.js'
import LearningRoute from './components/auth/LearningRoute.jsx'

const Home = lazy(() => import('./pages/home.jsx'))
const Syllabus = lazy(() => import('./pages/syllabusPage.jsx'))
const Topic = lazy(() => import('./pages/topicPage.jsx'))
const Quiz = lazy(() => import('./pages/quizPage.jsx'))
const Tag = lazy(() => import('./pages/tagPage.jsx'))
const Search = lazy(() => import('./pages/searchPage.jsx'))
const Resource = lazy(() => import('./pages/resourcePage.jsx'))
const Info = lazy(() => import('./pages/infoPage.jsx'))
const LearnerUnavailable = lazy(() => import('./pages/learnerUnavailablePage.jsx'))
const Login = lazy(() => import('./pages/loginPage.jsx'))
const Signup = lazy(() => import('./pages/signupPage.jsx'))
const Dashboard = lazy(() => import('./pages/dashboardPage.jsx'))
const Attempt = lazy(() => import('./pages/attemptPage.jsx'))
const Planner = lazy(() => import('./pages/plannerPage.jsx'))
const ResetPassword = lazy(() => import('./pages/resetPasswordPage.jsx'))
const NotFound = lazy(() => import('./pages/notFoundPage.jsx'))

function StudentRoute({ children }) {
  const { loading, featuresEnabled } = useAuth()
  if (loading) return <div className="page"><Skeleton label="Loading student access…" /></div>
  return featuresEnabled ? children : <LearnerUnavailable />
}

class ErrorBoundary extends Component {
  state = { failed: false }
  static getDerivedStateFromError() {
    return { failed: true }
  }
  render() {
    return this.state.failed ? (
      <main className="page status-panel">
        <h1>The page needs a fresh start.</h1>
        <p>Please reload to return to the library.</p>
        <button className="button primary" onClick={() => window.location.reload()}>
          Reload page
        </button>
      </main>
    ) : (
      this.props.children
    )
  }
}

export default function App() {
  return (
    <ErrorBoundary>
        <BrowserRouter>
          <Suspense fallback={<div className="page"><Skeleton /></div>}>
            <Routes>
              <Route element={<AppShell />}>
                <Route index element={<Home />} />
                <Route path="syllabus" element={<LearningRoute><Syllabus /></LearningRoute>} />
                <Route path="topic/:slug" element={<LearningRoute><Topic /></LearningRoute>} />
                <Route path="quiz/:slug" element={<LearningRoute><Quiz /></LearningRoute>} />
                <Route path="practice/:slug" element={<LearningRoute><Quiz collection /></LearningRoute>} />
                <Route path="tags/:slug" element={<LearningRoute><Tag /></LearningRoute>} />
                <Route path="search" element={<LearningRoute><Search /></LearningRoute>} />
                <Route path="resources/:id" element={<LearningRoute><Resource /></LearningRoute>} />
                <Route path="about" element={<Info />} />
                <Route path="help" element={<Info />} />
                <Route path="login" element={<StudentRoute><Login /></StudentRoute>} />
                <Route path="signup" element={<StudentRoute><Signup /></StudentRoute>} />
                <Route path="attempts/:id" element={<StudentRoute><LearningRoute><Attempt /></LearningRoute></StudentRoute>} />
                <Route path="planner" element={<StudentRoute><LearningRoute><Planner /></LearningRoute></StudentRoute>} />
                <Route path="reset-password" element={<StudentRoute><ResetPassword /></StudentRoute>} />
                <Route path="dashboard" element={<StudentRoute><LearningRoute><Dashboard /></LearningRoute></StudentRoute>} />
                <Route path="*" element={<NotFound />} />
              </Route>
            </Routes>
          </Suspense>
        </BrowserRouter>
    </ErrorBoundary>
  )
}
