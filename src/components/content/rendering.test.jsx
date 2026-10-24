import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import SafeHtml from './SafeHtml.jsx'
import SafeMarkdown from './SafeMarkdown.jsx'

describe('authored HTML allowlist', () => {
  it('preserves educational structure, Hindi, formatting and table semantics', () => {
    const { container } = render(<SafeHtml html={`
      <h1>History</h1><h2>राजस्थान</h2><h3>Sources</h3><h4>Period</h4><h5>Detail</h5><h6>Note</h6>
      <p lang="hi">पाठ <strong>bold</strong> <em>emphasis</em> <u>underline</u>
      H<sub>2</sub>O x<sup>2</sup> <mark>remember</mark><br>continued</p>
      <ol start="3"><li value="4">First</li></ol><ul><li>Second</li></ul>
      <blockquote>Source passage</blockquote><pre><code>&lt;tag&gt;</code></pre>
      <dl><dt>Term</dt><dd>Definition</dd></dl>
      <table><caption>Timeline</caption><thead><tr><th scope="col">Year</th></tr></thead>
      <tbody><tr><td colspan="2" rowspan="2">1947</td></tr></tbody></table>`} />)
    expect(screen.getAllByRole('heading')).toHaveLength(6)
    expect(container.querySelector('p')).toHaveAttribute('lang', 'hi')
    expect(container.querySelector('strong')).toHaveTextContent('bold')
    expect(container.querySelector('em')).toHaveTextContent('emphasis')
    expect(container.querySelector('sub')).toHaveTextContent('2')
    expect(container.querySelector('sup')).toHaveTextContent('2')
    expect(container.querySelector('ol')).toHaveAttribute('start', '3')
    expect(screen.getAllByRole('listitem')).toHaveLength(2)
    expect(container.querySelector('code')).toHaveTextContent('<tag>')
    expect(screen.getByRole('table')).toHaveTextContent(/Timeline\s*Year\s*1947/)
    expect(screen.getByRole('columnheader')).toHaveAttribute('scope', 'col')
    expect(screen.getByRole('cell')).toHaveAttribute('colspan', '2')
    expect(screen.getByRole('cell')).toHaveAttribute('rowspan', '2')
  })

  it('keeps safe links, enforces rel, namespaces ids and preserves local references', () => {
    render(<SafeHtml html={`<h2 id="sources">Sources</h2>
      <a href="#sources">Jump</a><a href="/topic/history">Internal</a>
      <a href="https://example.org/notes" target="_blank" rel="opener">Source</a>
      <a href="mailto:editor@example.org">Contact</a>`} />)
    expect(screen.getByRole('heading')).toHaveAttribute('id', 'user-content-sources')
    expect(screen.getByText('Jump')).toHaveAttribute('href', '#user-content-sources')
    expect(screen.getByText('Internal')).toHaveAttribute('href', '/topic/history')
    expect(screen.getByText('Source')).toHaveAttribute('target', '_blank')
    for (const link of screen.getAllByRole('link')) expect(link).toHaveAttribute('rel', 'noopener noreferrer')
    expect(screen.getByText('Contact')).toHaveAttribute('href', 'mailto:editor@example.org')
  })

  it('preserves authored safe images and captions without event handlers or srcset', () => {
    const { container } = render(<SafeHtml html={`<figure><img src="/media/map.png" alt="Map"
      width="200" onerror="alert(1)" srcset="https://tracker.invalid/pixel 2x"><figcaption>Region</figcaption></figure>`} />)
    expect(screen.getByRole('img')).toHaveAttribute('src', '/media/map.png')
    expect(screen.getByRole('img')).toHaveAttribute('alt', 'Map')
    expect(screen.getByRole('img')).not.toHaveAttribute('onerror')
    expect(screen.getByRole('img')).not.toHaveAttribute('srcset')
    expect(container.querySelector('figcaption')).toHaveTextContent('Region')
  })

  it.each([
    '<script>window.pwned=1</script>',
    '<svg onload="alert(1)"><a xlink:href="javascript:alert(1)">x</a></svg>',
    '<iframe srcdoc="<script>alert(1)</script>" src="javascript:alert(1)"></iframe>',
    '<object data="data:text/html,<script>alert(1)</script>"></object><embed src="x">',
    '<style>body{display:none}</style><link rel="stylesheet" href="https://evil.invalid/x">',
    '<form id="location" action="javascript:alert(1)"><input name="cookie"><button formaction="javascript:alert(1)">x</button></form>',
    '<math><mtext><table><mglyph><style><!--</style><img title="--><img src=x onerror=alert(1)>">',
    '<svg><foreignObject><p onmouseover="alert(1)">x</p></foreignObject></svg>',
    '<template shadowrootmode="open"><img src=x onerror=alert(1)></template>',
    '<img src="data:image/svg+xml,<svg onload=alert(1)>" onerror="alert(1)">',
  ])('rejects active markup: %s', (payload) => {
    const { container } = render(<SafeHtml html={`<p>Preserved lesson</p>${payload}`} />)
    expect(screen.getByText('Preserved lesson')).toBeVisible()
    expect(container.querySelector('script,style,svg,math,iframe,object,embed,form,input,button,template,link')).toBeNull()
    for (const node of container.querySelectorAll('*')) {
      for (const attribute of node.attributes) {
        expect(attribute.name).not.toMatch(/^on|^style$|^srcdoc$/i)
        if (['href', 'src'].includes(attribute.name)) {
          expect(attribute.value).not.toMatch(/^(javascript|vbscript|data|blob|file):/i)
        }
      }
    }
  })

  it('strips styling, spoofed app classes, data attributes and clobbering names', () => {
    const { container } = render(<SafeHtml html='<p class="navbar" style="position:fixed" onclick="alert(1)" data-command="run" name="cookie">Lesson</p>' />)
    expect(container.querySelector('p').getAttributeNames()).toEqual([])
    expect(screen.getByText('Lesson')).toBeVisible()
  })

  it('accepts empty or non-string data without inserting objects as markup', () => {
    const { container, rerender } = render(<SafeHtml html={null} />)
    expect(container.textContent).toBe('')
    rerender(<SafeHtml html={{ toString: () => '<script>alert(1)</script>' }} />)
    expect(container.textContent).toBe('')
  })
})

describe('shared content URL boundary', () => {
  it.each([
    'javascript:alert(1)', 'JaVaScRiPt:alert(1)', 'jav&#x61;script:alert(1)',
    'java&#10;script:alert(1)', 'vbscript:msgbox(1)', 'data:text/html,payload',
    'data:image/svg+xml,payload', 'blob:https://example.org/id', 'file:///tmp/x',
    'ftp://example.org/file', '//example.org/path', '\\example.org/path',
  ])('removes unsafe authored link destinations: %s', (href) => {
    render(<SafeHtml html={`<a href="${href}">Retained label</a>`} />)
    expect(screen.getByText('Retained label')).not.toHaveAttribute('href')
  })
})

describe('model Markdown rendering', () => {
  it('renders headings, lists, quotes, emphasis, GFM tables/tasks/deletion and safe code', () => {
    const { container } = render(<SafeMarkdown>{`## Summary

**Important** and *context* with ~~old fact~~.

- First item
- [x] Reviewed

> A quoted source

| Year | Event |
| --- | --- |
| 1947 | Independence |

\`\`\`html
<script>alert(1)</script>
\`\`\`
`}</SafeMarkdown>)
    expect(screen.getByRole('heading')).toHaveTextContent('Summary')
    expect(container.querySelector('strong')).toHaveTextContent('Important')
    expect(container.querySelector('em')).toHaveTextContent('context')
    expect(container.querySelector('del')).toHaveTextContent('old fact')
    expect(screen.getByRole('checkbox')).toBeDisabled()
    expect(screen.getByRole('checkbox')).toBeChecked()
    expect(screen.getByRole('table')).toHaveTextContent('Independence')
    expect(container.querySelector('code')).toHaveTextContent('<script>alert(1)</script>')
    expect(container.querySelector('script')).toBeNull()
  })

  it('ignores raw model HTML and renders image descriptions without fetching images', () => {
    const { container } = render(<SafeMarkdown>{`Safe paragraph.

<script>alert(1)</script>

<iframe srcdoc="<script>alert(1)</script>"></iframe>

<img src=x onerror=alert(1)>

<svg onload=alert(1)></svg>

![Map description](https://tracker.invalid/pixel)
`}</SafeMarkdown>)
    expect(screen.getByText('Safe paragraph.')).toBeVisible()
    expect(screen.getByText('Map description')).toBeVisible()
    expect(container.querySelector('script,iframe,img,svg,link')).toBeNull()
  })

  it.each(['javascript:alert%281%29', 'jav&#x61;script:alert%281%29', 'data:text/html,payload', 'vbscript:msgbox%281%29', '//evil.invalid/x', 'file:///etc/passwd'])('blocks Markdown destination: %s', (url) => {
    render(<SafeMarkdown>{`[Retained label](${url})`}</SafeMarkdown>)
    expect(screen.getByText('Retained label')).toBeVisible()
    expect(screen.queryByRole('link')).toBeNull()
  })

  it('preserves safe Markdown links with the shared rel policy', () => {
    render(<SafeMarkdown>{'[Source](https://example.org/source) [Next](/topic/history) [Email](mailto:editor@example.org)'}</SafeMarkdown>)
    expect(screen.getByText('Source')).toHaveAttribute('href', 'https://example.org/source')
    expect(screen.getByText('Next')).toHaveAttribute('href', '/topic/history')
    for (const link of screen.getAllByRole('link')) expect(link).toHaveAttribute('rel', 'noopener noreferrer')
  })
})
