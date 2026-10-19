import SafeHtml from '../content/SafeHtml.jsx'

export default function ContentRenderer({ blocks = [], onSelection, revision }) {
  function select(event, block) {
    if (block.block_type !== 'text') return
    const selection = window.getSelection()
    if (!selection || selection.isCollapsed || !event.currentTarget.contains(selection.anchorNode) || !event.currentTarget.contains(selection.focusNode)) return
    const text = selection.toString().trim()
    if (text && text.length <= 1000) onSelection?.({ text, source_id: `b${block.id}`, revision })
  }
  return <div className="lesson-content">{blocks.map((block, i) => <section key={block.id ?? i} id={block.anchor || `block-${block.id ?? i}`} tabIndex={-1} className="content-block" onMouseUp={e => select(e, block)} onKeyUp={e => select(e, block)}>
    {block.block_type === 'heading' && <h2>{block.content}</h2>}
    {block.block_type === 'text' && <><SafeHtml html={block.content} className="block-text" />{onSelection && block.id && <button className="passage-action" onClick={() => {
      const element = document.getElementById(block.anchor || `block-${block.id}`)
      onSelection({ text: (element.querySelector('.block-text p') || element.querySelector('.block-text')).textContent.trim().slice(0, 1000), source_id: `b${block.id}`, revision })
    }}>Explain this passage <span aria-hidden="true">↗</span></button>}</>}
    {block.block_type === 'image' && block.file && <figure><img src={block.file} alt={block.alt_text || ''} loading="lazy" width="760" height="480" />{block.caption && <figcaption>{block.caption}</figcaption>}</figure>}
    {block.file && block.block_type !== 'image' && (
      <div className="block-attachment" data-testid="block-attachment">
        <div className="attachment-card">
          <span className="attachment-icon" aria-hidden="true">{block.is_pdf ? '📄' : '📎'}</span>
          <div className="attachment-info">
            <strong className="attachment-title">
              {block.file_name || block.caption || (block.file ? decodeURIComponent(block.file.split('/').pop()) : '') || (block.is_pdf ? 'Attached PDF Document' : 'Attached Document')}
            </strong>
            <span className="attachment-subtext">{block.is_pdf ? 'Verified PDF study material' : 'Attached course material'}</span>
          </div>
          <a
            href={block.file}
            target="_blank"
            rel="noopener noreferrer"
            className="attachment-action-btn"
          >
            Open in new tab <span aria-hidden="true">↗</span>
          </a>
        </div>
        {block.is_pdf && (
          <div className="pdf-embed-wrapper">
            <iframe
              src={block.file}
              title={block.file_name || block.caption || 'Attached PDF document'}
              className="pdf-viewer-frame"
            />
          </div>
        )}
      </div>
    )}
    {block.source_reference && block.block_type === 'text' && <small className="source-note">Source: {block.source_reference}</small>}
  </section>)}</div>
}
