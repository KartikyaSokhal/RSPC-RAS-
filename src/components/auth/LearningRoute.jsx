import { useContext } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import useAuth from '../../hooks/useAuth.js'
import { PlatformContext } from '../layout/platformContext.js'
import Skeleton from '../ui/Skeleton.jsx'

export default function LearningRoute({ children }) {
  const { loading, authenticated } = useAuth()
  const { learning_auth_required: required } = useContext(PlatformContext)
  const location = useLocation()
  if (loading) return <div className="page"><Skeleton label="Checking student session…" /></div>
  if (required && !authenticated) return <Navigate to="/login" replace state={{ from: { pathname: location.pathname, search: location.search, hash: location.hash } }} />
  return children
}
