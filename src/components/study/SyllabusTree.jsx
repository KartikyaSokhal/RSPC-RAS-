import { useState } from 'react'
import { Link } from 'react-router-dom'

function TreeNode({ item, current, depth = 0, forceOpen = null }) {
  const children = item.children || []
  const hasChildren = children.length > 0
  const containsCurrent = node => node.slug === current || Boolean(node.children?.some(containsCurrent))
  const isCurrent = current === item.slug
  const defaultOpen = depth === 0 || containsCurrent(item)
  const isOpen = forceOpen !== null ? forceOpen : undefined

  if (hasChildren) {
    return (
      <details
        className={`tree-group depth-${depth} ${containsCurrent(item) ? 'has-current' : ''}`}
        open={isOpen !== undefined ? isOpen : defaultOpen}
        key={forceOpen !== null ? `${item.slug}-${forceOpen}` : undefined}
      >
        <summary className="tree-group-summary">
          <div className="group-title-wrap">
            <span className="group-indicator" aria-hidden="true">
              {depth === 0 ? '§' : depth === 1 ? '▸' : '•'}
            </span>
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
          >
            <span>Overview →</span>
          </Link>
          {children.map(child => (
            <TreeNode
              key={child.slug}
              item={child}
              current={current}
              depth={depth + 1}
              forceOpen={forceOpen}
            />
          ))}
        </div>
      </details>
    )
  }

  return (
    <div className={`tree-leaf-wrap depth-${depth}`}>
      <Link
        className={`tree-leaf ${isCurrent ? 'active' : ''}`}
        aria-current={isCurrent ? 'page' : undefined}
        to={`/topic/${item.slug}`}
      >
        <span className="leaf-marker" aria-hidden="true">
          {item.has_notes ? '◆' : '◇'}
        </span>
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

export default function SyllabusTree({ topics, current, showControls = false }) {
  const [forceOpen, setForceOpen] = useState(null)

  return (
    <div className="syllabus-tree-container">
      {showControls && (
        <div className="tree-controls" role="group" aria-label="Syllabus tree controls">
          <button
            type="button"
            className="tree-control-btn"
            onClick={() => setForceOpen(true)}
          >
            Expand all
          </button>
          <span className="control-sep" aria-hidden="true">·</span>
          <button
            type="button"
            className="tree-control-btn"
            onClick={() => setForceOpen(false)}
          >
            Collapse all
          </button>
          <span className="control-sep" aria-hidden="true">·</span>
          <button
            type="button"
            className="tree-control-btn"
            onClick={() => setForceOpen(null)}
          >
            Default view
          </button>
        </div>
      )}
      <nav className="syllabus-tree" aria-label="Official RPSC RAS syllabus hierarchy">
        {topics.map(topic => (
          <TreeNode
            key={topic.slug}
            item={topic}
            current={current}
            forceOpen={forceOpen}
          />
        ))}
      </nav>
    </div>
  )
}
