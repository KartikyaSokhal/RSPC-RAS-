import { test, expect } from '@playwright/test'

const attack = 'globalThis.__p001Executed += 1'
const authored = `<h2 id="lesson">Safe lesson</h2><p>Keep <strong>this fact</strong>.</p>
  <ul><li>First fact</li></ul>
  <table><caption>Timeline</caption><tr><th scope="col">Year</th><td>1947</td></tr></table>
  <a href="https://example.org/source" target="_blank" rel="opener">Reference</a>
  <a href="jav&#x61;script:${attack}">Bad reference</a>
  <img src="/missing-p001-image" alt="Broken fixture" onerror="${attack}">
  <p onclick="${attack}" onmouseover="${attack}" style="position:fixed">Event fixture</p>
  <script>${attack}</script><svg onload="${attack}"></svg>
  <iframe srcdoc="<script>${attack}</script>"></iframe>`
const modelResponse = `## Safe explanation

**Key fact**

| Year | Event |
| --- | --- |
| 1947 | Independence |

<img src="/missing-ai-image" onerror="${attack}">

<svg onload="${attack}"></svg>

<iframe srcdoc="<script>${attack}</script>"></iframe>

[Bad model link](javascript:alert%281%29)

[Model source](https://example.org/source)

![Model diagram](https://tracker.invalid/pixel)
`

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => { globalThis.__p001Executed = 0 })
  await page.route('**/*', async route => {
    const url = new URL(route.request().url())
    if (url.origin !== 'http://127.0.0.1:4173') return route.abort('blockedbyclient')
    if (url.pathname.startsWith('/missing-')) return route.fulfill({ status: 404, body: '' })
    if (!url.pathname.startsWith('/api/')) return route.continue()
    if (url.pathname === '/api/config/') return route.fulfill({ json: { csrf_token: 'fixture', demo: true } })
    if (url.pathname === '/api/auth/status/') return route.fulfill({ json: { authenticated: false, user: null } })
    if (url.pathname === '/api/topics/') return route.fulfill({ json: [] })
    if (url.pathname === '/api/topic/p001/') return route.fulfill({ json: { title: 'Security fixture', slug: 'p001', children: [], blocks: [{ id: 1, block_type: 'text', content: authored }] } })
    if (url.pathname === '/api/topic/p001/chat/') return route.fulfill({ json: { response: modelResponse, citations: [] } })
    throw new Error(`Unexpected API call: ${url.pathname}`)
  })
})

test('reader preserves educational content and blocks active HTML in Chromium', async ({ page }) => {
  const errors = []
  page.on('pageerror', (error) => errors.push(error.message))
  await page.goto('/topic/p001')
  await expect(page.getByRole('heading', { name: 'Safe lesson' })).toBeVisible()
  await expect(page.getByRole('table')).toContainText('1947')
  await expect(page.getByText('First fact')).toBeVisible()
  await expect(page.getByText('Reference', { exact: true })).toHaveAttribute('rel', 'noopener noreferrer')
  await expect(page.getByText('Bad reference')).not.toHaveAttribute('href')
  await page.getByText('Event fixture').hover()
  await page.getByText('Event fixture').click()
  await page.getByRole('img', { name: 'Broken fixture' }).evaluate((img) => {
    img.dispatchEvent(new Event('error'))
  })
  await expect(page.locator('.block-text script, .block-text svg, .block-text iframe, .block-text [onclick], .block-text [onerror]')).toHaveCount(0)
  expect(await page.evaluate(() => globalThis.__p001Executed)).toBe(0)
  expect(errors).toEqual([])
})

test('chat stays safe and revision is paused without fetching learner history', async ({ page }) => {
  const modelRequests = []
  page.on('request', (request) => {
    if (request.url().includes('tracker.invalid') || request.url().includes('missing-ai-image')) modelRequests.push(request.url())
  })
  await page.goto('/topic/p001')
  await page.getByRole('button', { name: 'Ask AI Tutor' }).click()
  await page.getByRole('textbox', { name: 'Ask the tutor' }).fill('Explain this fixture')
  await page.getByRole('button', { name: 'Send question' }).click()
  const panel = page.locator('.ai-companion-panel')
  await expect(panel.getByRole('heading', { name: 'Safe explanation' })).toBeVisible()
  await expect(panel.getByRole('table')).toContainText('Independence')
  await expect(panel.getByText('Bad model link')).not.toHaveAttribute('href')
  await expect(panel.getByText('Model source')).toHaveAttribute('href', 'https://example.org/source')
  await expect(panel.getByText('Model diagram')).toBeVisible()
  await expect(panel.locator('img, svg, script, iframe')).toHaveCount(0)
  await expect(page.getByText(/Sign in to save this topic to your bookmarks/)).toBeVisible()
  expect(await page.evaluate(() => globalThis.__p001Executed)).toBe(0)
  expect(modelRequests).toEqual([])
})
