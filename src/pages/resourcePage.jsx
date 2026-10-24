import { lazy, Suspense, useState } from 'react'
import { Link, useParams, useSearchParams } from 'react-router-dom'
import useResource from '../hooks/useResource.js'
import Skeleton from '../components/ui/Skeleton.jsx'
import StatusPanel from '../components/ui/StatusPanel.jsx'
const PdfViewer = lazy(() => import('../components/resources/PdfViewer.jsx'))

export default function ResourcePage() {
  const { id } = useParams()
  const [params, setParams] = useSearchParams()
  const page = Math.max(1, Number(params.get('page')) || 1)
  const [zoom, setZoom] = useState(1)
  const { data, loading, error, retry } = useResource(`/resources/${encodeURIComponent(id)}/?page=${page}`)
  if (loading) return <div className="page"><Skeleton label="Opening your reading material…" /></div>
  if (error || !data) return <div className="page"><StatusPanel title="This reading material is unavailable." retry={error?.response?.status !== 404 ? retry : undefined}>It may still be processing, awaiting review, or withdrawn. Only approved resources are available here.</StatusPanel></div>
  return <div className="page resource-page"><Link className="back-link" to={`/topic/${data.topic.slug}`}>← {data.topic.title}</Link><div className="resource-heading"><div><span className="eyebrow">The reading room · PDF</span><h1>{data.title}</h1><p>{data.page_count} pages · {data.source_reference}</p></div><a className="button" href={data.file_url} target="_blank" rel="noopener noreferrer">Open document ↗</a></div><div className="pdf-toolbar"><div className="button-row"><button className="icon-button" aria-label="Previous PDF page" disabled={page <= 1} onClick={() => setParams({ page: String(page - 1) })}>←</button><label>Page <select aria-label="PDF page" value={page} onChange={e => setParams({ page: e.target.value })}>{Array.from({ length: data.page_count }, (_, i) => <option key={i+1} value={i+1}>{i+1}</option>)}</select> of {data.page_count}</label><button className="icon-button" aria-label="Next PDF page" disabled={page >= data.page_count} onClick={() => setParams({ page: String(page + 1) })}>→</button></div><div className="button-row"><button className="icon-button" aria-label="Zoom out" disabled={zoom <= 0.75} onClick={() => setZoom(z => z - 0.25)}>−</button><span className="zoom-label">{Math.round(zoom * 100)}%</span><button className="icon-button" aria-label="Zoom in" disabled={zoom >= 2} onClick={() => setZoom(z => z + 0.25)}>+</button></div></div><Suspense fallback={<Skeleton label="Loading document viewer…" />}><PdfViewer url={data.file_url} page={page} zoom={zoom} title={data.title} /></Suspense><details className="pdf-text"><summary>Read accessible page text <span>PAGE {page}</span></summary><p>{data.text}</p></details><p className="privacy-note">Page numbers refer to file pages, which may differ from printed page labels. Extraction can affect reading order; check the original page when needed.</p></div>
}
