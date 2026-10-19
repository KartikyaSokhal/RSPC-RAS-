import { Link } from 'react-router-dom'
export default function TopicBreadcrumbs({ items = [] }) {
  return <nav className="breadcrumbs" aria-label="Breadcrumb"><Link to="/syllabus">Library</Link>{items.map((item, i) => <span key={item.slug}><span className="crumb-divider" aria-hidden="true">/</span>{i === items.length - 1 ? <span aria-current="page">{item.title}</span> : <Link to={`/topic/${item.slug}`}>{item.title}</Link>}</span>)}</nav>
}
