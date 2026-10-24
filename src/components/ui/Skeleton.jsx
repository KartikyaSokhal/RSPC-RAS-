export default function Skeleton({ label = 'Loading your learning space…' }) {
  return <div className="loading-space"><p role="status" className="sr-only">{label}</p><div aria-hidden="true"><div className="skeleton short" /><div className="skeleton title" /><div className="skeleton" /><div className="skeleton" /><div className="skeleton block" /></div></div>
}
