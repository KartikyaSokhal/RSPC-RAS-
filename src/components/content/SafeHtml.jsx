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
export default function SafeHtml({ html, className }) {
  const sanitized = useMemo(
    () => purifier.isSupported ? purifier.sanitize(typeof html === 'string' ? html : '', config) : null,
    [html],
  )
  // DOMPurify can return unfiltered input on unsupported DOM implementations.
  // Fall back to React text escaping rather than weakening the trust boundary.
  if (sanitized === null) return <div className={className}>{typeof html === 'string' ? html : ''}</div>
  return <div className={className} dangerouslySetInnerHTML={{ __html: sanitized }} />
}
