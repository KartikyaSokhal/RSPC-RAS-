import { useMemo } from 'react'
import createDOMPurify from 'dompurify'
import { CONTENT_LINK_REL, safeContentUrl } from './contentUrls.js'

const tags = [
  'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br', 'hr', 'div', 'span',
  'strong', 'em', 'b', 'i', 'u', 's', 'del', 'ins', 'mark', 'small', 'sub', 'sup',
  'blockquote', 'q', 'cite', 'abbr', 'pre', 'code', 'kbd', 'samp', 'var',
  'ul', 'ol', 'li', 'dl', 'dt', 'dd', 'a', 'img', 'figure', 'figcaption',
  'table', 'caption', 'colgroup', 'col', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td',
]
const commonAttributes = ['id', 'title', 'lang', 'dir', 'aria-label']
const elementAttributes = {
  a: ['href', 'target', 'rel'], img: ['src', 'alt', 'width', 'height'],
  ol: ['start', 'reversed', 'type'], li: ['value'],
  th: ['colspan', 'rowspan', 'scope', 'abbr'], td: ['colspan', 'rowspan'],
  col: ['span'], colgroup: ['span'],
}
const config = {
  ALLOWED_TAGS: tags,
  ALLOWED_ATTR: [...commonAttributes, ...new Set(Object.values(elementAttributes).flat())],
  ALLOW_DATA_ATTR: false,
  ALLOW_ARIA_ATTR: false, // Only the explicit aria-label above is accepted.
  SANITIZE_DOM: true,
  SANITIZE_NAMED_PROPS: true, // Prefix ids; never expose content as named DOM globals.
  RETURN_TRUSTED_TYPE: false,
}

// Private instance: hooks cannot change another consumer's sanitization policy.
const purifier = createDOMPurify(window)
purifier.addHook?.('uponSanitizeAttribute', (node, attribute) => {
  const tag = node.nodeName.toLowerCase()
  const name = attribute.attrName
  if (!commonAttributes.includes(name) && !elementAttributes[tag]?.includes(name)) {
    attribute.keepAttr = false
  } else if (name === 'href' || name === 'src') {
    const safe = safeContentUrl(attribute.attrValue, { image: name === 'src' })
    if (safe === undefined) attribute.keepAttr = false
    else attribute.attrValue = safe
  } else if (name === 'target' && !['_blank', '_self'].includes(attribute.attrValue)) {
    attribute.keepAttr = false
  }
})
purifier.addHook?.('afterSanitizeAttributes', (node) => {
  if (node.nodeName === 'A') {
    node.setAttribute('rel', CONTENT_LINK_REL)
    const href = node.getAttribute('href')
    // Keep same-document references working with DOMPurify's namespaced ids.
    if (href?.startsWith('#') && href.length > 1) {
      node.setAttribute('href', `#user-content-${href.slice(1)}`)
    }
  }
})

/** Authored educational HTML only. AI output must use SafeMarkdown. */
const emptyConnections = []

export default function SafeHtml({ html, className, connections = emptyConnections, onConnection }) {
  const sanitized = useMemo(() => {
    if (!purifier.isSupported) return null
    const fragment = purifier.sanitize(typeof html === 'string' ? html : '', { ...config, RETURN_DOM_FRAGMENT: true })
    const walker = document.createTreeWalker(fragment, window.NodeFilter.SHOW_TEXT)
    const nodes = []; let node
    while ((node = walker.nextNode())) nodes.push(node)
    // Only metadata generated outside authored HTML can create popup controls.
    // Exact text/offset checks fail closed if the browser repaired the markup.
    for (const [index, textNode] of nodes.entries()) {
      const rows = connections.map((row, key) => ({ ...row, key })).filter(row => row.node_index === index)
        .sort((a, b) => a.start - b.start)
      const replacement = document.createDocumentFragment(); let offset = 0
      for (const row of rows) {
        if (!Number.isSafeInteger(row.start) || !Number.isSafeInteger(row.end) || row.start < offset || row.end <= row.start ||
            textNode.textContent.slice(row.start, row.end) !== row.text || typeof row.target?.slug !== 'string' ||
            !row.target.slug || row.target.slug.length > 255 || textNode.parentElement?.closest('a,pre,code,kbd,samp,h1,h2,h3,h4,h5,h6')) continue
        replacement.append(document.createTextNode(textNode.textContent.slice(offset, row.start)))
        const link = document.createElement('a')
        link.textContent = row.text
        link.href = `/topic/${encodeURIComponent(row.target.slug)}`
        link.target = '_blank'; link.rel = CONTENT_LINK_REL
        link.className = 'keyword-connection'
        link.dataset.prepalConnection = String(row.key)
        link.setAttribute('aria-haspopup', 'dialog')
        replacement.append(link); offset = row.end
      }
      if (offset) {
        replacement.append(document.createTextNode(textNode.textContent.slice(offset)))
        textNode.replaceWith(replacement)
      }
    }
    const wrapper = document.createElement('div'); wrapper.append(fragment)
    return wrapper.innerHTML
  }, [html, connections])
  const markup = useMemo(() => ({ __html: sanitized }), [sanitized])
  function activate(event) {
    const link = event.target.closest?.('a[data-prepal-connection]')
    if (!link || !event.currentTarget.contains(link) || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return
    const row = connections[Number(link.dataset.prepalConnection)]
    if (row && onConnection) { event.preventDefault(); onConnection(row.target, link) }
  }
  // DOMPurify can return unfiltered input on unsupported DOM implementations.
  // Fall back to React text escaping rather than weakening the trust boundary.
  if (sanitized === null) return <div className={className}>{typeof html === 'string' ? html : ''}</div>
  return <div className={className} onClick={activate} dangerouslySetInnerHTML={markup} />
}
