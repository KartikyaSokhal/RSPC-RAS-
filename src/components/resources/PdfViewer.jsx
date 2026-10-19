import { useEffect, useRef, useState } from 'react'
import workerUrl from 'pdfjs-dist/build/pdf.worker.min.mjs?url'

export default function PdfViewer({ url, page, zoom, title }) {
  const canvas = useRef(null)
  const container = useRef(null)
  const [document, setDocument] = useState(null)
  const [width, setWidth] = useState(600)
  const [state, setState] = useState({ key: '', error: false })
  const key = `${url}:${page}:${zoom}:${width}`
  useEffect(() => {
    const observer = new ResizeObserver(entries => setWidth(Math.max(240, entries[0].contentRect.width - 40)))
    observer.observe(container.current)
    return () => observer.disconnect()
  }, [])
  useEffect(() => {
    let active = true; let task
    import('pdfjs-dist').then(pdfjs => {
      if (!active) return
      pdfjs.GlobalWorkerOptions.workerSrc = workerUrl
      task = pdfjs.getDocument({ url, isEvalSupported: false, enableXfa: false, useSystemFonts: true, disableAutoFetch: true, disableStream: true })
      return task.promise
    }).then(pdf => { if (active && pdf) setDocument({ url, pdf }) }).catch(() => { if (active) setDocument({ url, error: true }) })
    return () => { active = false; task?.destroy() }
    // Render state belongs to the separate page effect; document fetch only follows URL.
  }, [url])
  useEffect(() => {
    if (!document || document.url !== url || document.error) return undefined
    let active = true; let render
    document.pdf.getPage(page).then(pdfPage => {
      if (!active) return
      const natural = pdfPage.getViewport({ scale: 1 })
      const viewport = pdfPage.getViewport({ scale: Math.min(width / natural.width, 1.4) * zoom })
      const target = canvas.current
      target.width = viewport.width * Math.min(window.devicePixelRatio || 1, 2)
      target.height = viewport.height * Math.min(window.devicePixelRatio || 1, 2)
      target.style.width = `${viewport.width}px`; target.style.height = `${viewport.height}px`
      render = pdfPage.render({ canvasContext: target.getContext('2d'), viewport, transform: [target.width / viewport.width, 0, 0, target.height / viewport.height, 0, 0] })
      return render.promise
    }).then(() => { if (active) setState({ key, error: false }) }).catch(error => { if (active && error.name !== 'RenderingCancelledException') setState({ key, error: true }) })
    return () => { active = false; render?.cancel() }
  }, [document, url, page, zoom, width, key])
  return <div className="pdf-canvas-area" ref={container}>{!document?.error && state.key !== key && <p role="status" className="pdf-loading">Opening page {page}…</p>}{(document?.error || (state.error && state.key === key)) ? <p role="status" className="inline-error">The PDF page could not render. The accessible page text below is still available.</p> : <canvas ref={canvas} role="img" aria-label={`${title}, page ${page}. Accessible text follows the viewer.`} />}</div>
}
