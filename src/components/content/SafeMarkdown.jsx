import Markdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { CONTENT_LINK_REL, safeContentUrl } from './contentUrls.js'

function MarkdownLink({ href, title, children, id, 'aria-label': ariaLabel }) {
  if (!href) return <span>{children}</span>
  return <a href={href} title={title} id={id} aria-label={ariaLabel} rel={CONTENT_LINK_REL}>{children}</a>
}

function ImageDescription({ alt }) {
  // Model-provided image URLs must not make automatic tracking/resource requests.
  return <span>{alt || '[Image omitted]'}</span>
}

const plugins = [remarkGfm]
const components = { a: MarkdownLink, img: ImageDescription }
const transformUrl = (url, key) => key === 'href' ? safeContentUrl(url) : undefined

/** Model text is parsed into React nodes; raw HTML is never interpreted. */
export default function SafeMarkdown({ children }) {
  return (
    <Markdown skipHtml remarkPlugins={plugins} components={components} urlTransform={transformUrl}>
      {typeof children === 'string' ? children : ''}
    </Markdown>
  )
}
