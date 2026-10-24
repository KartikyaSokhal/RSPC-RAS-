import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { indexSyllabus } from './syllabusUtils.js'

function TreeNode({ item, current, depth = 0, expanded, toggle, index, rootAnchorPrefix }) {
  const children = item.children || []
  const hasChildren = children.length > 0
  const containsCurrent = node => node.slug === current || Boolean(node.children?.some(containsCurrent))
  const isCurrent = current === item.slug
  const number = index.get(item.slug)?.number
  const anchor = depth === 0 && rootAnchorPrefix ? `${rootAnchorPrefix}-${item.id}` : undefined

  if (hasChildren) {
    return (
      <details
        className={`tree-group depth-${depth} ${containsCurrent(item) ? 'has-current' : ''}`}
        id={anchor}
        open={expanded.has(item.slug)}
      >
        <summary className="tree-group-summary" onClick={event => { event.preventDefault(); toggle(item.slug) }}>
          <div className="group-title-wrap">
            <span className="tree-number">{number}</span>
            <span className="group-title">{item.title}</span>
            {item.has_notes && (
              <span className="status-badge notes-ready" title="Notes ready">
                Notes
              </span>
            )}
            {!item.has_notes && (
              <span className="status-badge coming-soon" title="Under preparation">
                Prep
              </span>
            )}
          </div>
          <span className="tree-chevron" aria-hidden="true">⌄</span>
        </summary>
        <div className="tree-children">
          <Link
            className={`tree-overview ${isCurrent ? 'active' : ''}`}
            to={`/topic/${item.slug}`}
            aria-current={isCurrent ? 'page' : undefined}
          >
            <span>Overview →</span>
          </Link>
          {children.map(child => (
            <TreeNode
              key={child.slug}
              item={child}
              current={current}
              depth={depth + 1}
              expanded={expanded}
              toggle={toggle}
              index={index}
            />
          ))}
        </div>
      </details>
    )
  }

  return (
    <div id={anchor} className={`tree-leaf-wrap depth-${depth}`}>
      <Link
        className={`tree-leaf ${isCurrent ? 'active' : ''}`}
        aria-current={isCurrent ? 'page' : undefined}
        to={`/topic/${item.slug}`}
      >
        <span className="tree-number">{number}</span>
        <span className="leaf-title">{item.title}</span>
        <span className="leaf-badges">
          {item.has_notes && (
            <span className="status-badge notes-ready" title="Study notes published">
              Notes
            </span>
          )}
          {!item.has_notes && (
            <span className="status-badge coming-soon" title="Notes under preparation">
              Prep
            </span>
          )}
          {item.has_quiz && (
            <span className="feature-badge quiz-badge" title="Practice questions ready">
              Quiz
            </span>
          )}
          {item.has_resources && (
            <span className="feature-badge pdf-badge" title="Source PDF guide available">
              PDF
            </span>
          )}
        </span>
      </Link>
    </div>
  )
}

export default function SyllabusTree({ topics, originalTopics = topics, current, showControls = false, rootAnchorPrefix }) {
  const index = useMemo(() => indexSyllabus(originalTopics), [originalTopics])
  const [expanded, setExpanded] = useState(() => new Set([...index].filter(([, node]) => {
    const currentPath = index.get(current)?.path || []
    return node.path.length === 1 || node.path.every((part, i) => currentPath[i] === part)
  }).map(([slug]) => slug)))

  function toggle(slug) {
    setExpanded(previous => {
      const next = new Set(previous)
      if (next.has(slug)) next.delete(slug)
      else next.add(slug)
      return next
    })
  }

  return (
    <div className="syllabus-tree-container">
      {showControls && (
        <div className="tree-controls" role="group" aria-label="Syllabus tree controls">
          <button type="button" className="tree-control-btn" onClick={() => setExpanded(new Set(index.keys()))}>Expand All</button>
          <button type="button" className="tree-control-btn" onClick={() => setExpanded(new Set())}>Collapse All</button>
        </div>
      )}
      <nav className="syllabus-tree" aria-label="Official RPSC RAS syllabus hierarchy">
        {topics.map(topic => (
          <TreeNode key={topic.slug} item={topic} current={current} expanded={expanded} toggle={toggle} index={index} rootAnchorPrefix={rootAnchorPrefix} />
        ))}
      </nav>
    </div>
  )
}
