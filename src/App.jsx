import { Component, lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import AppShell from './components/layout/AppShell.jsx'
import Skeleton from './components/ui/Skeleton.jsx'
import { AuthProvider } from './context/AuthContext.jsx'
import './App.css'

const Home = lazy(() => import('./pages/home.jsx'))
const Syllabus = lazy(() => import('./pages/syllabusPage.jsx'))
const Topic = lazy(() => import('./pages/topicPage.jsx'))
const Quiz = lazy(() => import('./pages/quizPage.jsx'))
const Search = lazy(() => import('./pages/searchPage.jsx'))
const Resource = lazy(() => import('./pages/resourcePage.jsx'))
const Info = lazy(() => import('./pages/infoPage.jsx'))
const Login = lazy(() => import('./pages/loginPage.jsx'))
const Signup = lazy(() => import('./pages/signupPage.jsx'))
const Dashboard = lazy(() => import('./pages/dashboardPage.jsx'))
const NotFound = lazy(() => import('./pages/notFoundPage.jsx'))

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
      <AuthProvider>
        <BrowserRouter>
          <Suspense fallback={<div className="page"><Skeleton /></div>}>
            <Routes>
              <Route element={<AppShell />}>
                <Route index element={<Home />} />
                <Route path="syllabus" element={<Syllabus />} />
                <Route path="topic/:slug" element={<Topic />} />
                <Route path="quiz/:slug" element={<Quiz />} />
                <Route path="search" element={<Search />} />
                <Route path="resources/:id" element={<Resource />} />
                <Route path="about" element={<Info />} />
                <Route path="help" element={<Info />} />
                <Route path="login" element={<Login />} />
                <Route path="signup" element={<Signup />} />
                <Route path="dashboard" element={<Dashboard />} />
                <Route path="*" element={<NotFound />} />
              </Route>
            </Routes>
          </Suspense>
        </BrowserRouter>
      </AuthProvider>
    </ErrorBoundary>
  )
}
