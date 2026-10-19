// Shared navigation policy for authored HTML and model-generated Markdown.
export const CONTENT_LINK_REL = 'noopener noreferrer'

export function safeContentUrl(value, { image = false } = {}) {
  if (typeof value !== 'string') return undefined
  const url = value.trim()
  // Reject browser-normalized controls/backslashes and implicit external schemes.
  if (!url || /[\p{Cc}\\]/u.test(url) || url.startsWith('//')) {
    return undefined
  }
  try {
    const parsed = new URL(url, 'https://prepal.invalid/')
    if (parsed.protocol === 'https:' || parsed.protocol === 'http:' ||
        (!image && parsed.protocol === 'mailto:')) return url
  } catch {
    // Malformed URLs are rendered as text, never repaired into executable links.
  }
  return undefined
}
