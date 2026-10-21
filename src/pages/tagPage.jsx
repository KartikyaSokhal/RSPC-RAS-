import { Link, useParams, useSearchParams } from 'react-router-dom'
import useResource from '../hooks/useResource.js'
import Skeleton from '../components/ui/Skeleton.jsx'
import StatusPanel from '../components/ui/StatusPanel.jsx'

export default function TagPage() {
  const { slug } = useParams()
  const [params, setParams] = useSearchParams()
  const page = params.get('page') || '1'
  const { data, loading, error, retry } = useResource(`/tags/${encodeURIComponent(slug)}/?page=${encodeURIComponent(page)}`)
  return <div className="page tag-page"><Link to="/syllabus" className="back-link">← Syllabus</Link>
    {loading ? <Skeleton label="Opening tag…" /> : error || !data ? <StatusPanel title={error?.response?.status === 404 ? 'This tag is not available.' : 'The tag could not load.'} retry={error?.response?.status !== 404 ? retry : undefined}>Browse the syllabus for published study material.</StatusPanel> : <>
      <h1>{data.tag.name}</h1><p>{data.count} published {data.count === 1 ? 'article' : 'articles'}</p>
      {data.results.length ? <div className="search-results">{data.results.map(item => <Link className="search-result" key={item.id} to={`/topic/${item.slug}`}>
        <div><p className="result-path">{item.syllabus_location.map(node => node.title).join(' › ')}</p><h2>{item.title}</h2>{item.read_minutes && <p>About {item.read_minutes} min read</p>}</div>
      </Link>)}</div> : <p role="status">No published articles are available for this tag yet.</p>}
      <nav className="pagination" aria-label="Tag pages"><button className="button" disabled={data.page <= 1} onClick={() => setParams({page: String(data.page - 1)})}>Previous</button><span>Page {data.page}</span><button className="button" disabled={data.page * data.page_size >= data.count} onClick={() => setParams({page: String(data.page + 1)})}>Next</button></nav>
    </>}
  </div>
}
