import { chromium } from '@playwright/test'
import { mkdir, readFile, writeFile } from 'node:fs/promises'
import path from 'node:path'
const base = process.env.PREPAL_GALLERY_URL || 'http://127.0.0.1:5173'
if (!/^http:\/\/127\.0\.0\.1:\d+$/.test(base)) throw Error('Gallery requires the local isolated demo')
const output = path.resolve('docs/design/screenshots')
await mkdir(output, { recursive: true })
const browser = await chromium.launch()
const manifest = []
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, reducedMotion: 'reduce' })
await page.route('**/*', route => ['127.0.0.1', 'localhost'].includes(new URL(route.request().url()).hostname) ? route.continue() : route.abort())
const config = await (await page.request.get(base + '/api/config/')).json()
if (!config.demo) throw Error('Refusing screenshots outside the synthetic demo')

async function visit(route) {
  await page.goto(base + route)
  await page.waitForLoadState('networkidle')
  await page.locator('h1:visible,h2:visible').first().waitFor()
}

async function shot(name, purpose, variant = 'Desktop · light', note = 'Actual React/Django; synthetic content; mocked AI') {
  await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }))
  await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))))
  if (await page.locator('.pdf-canvas-area').count()) await page.locator('.pdf-loading').waitFor({ state: 'hidden' })
  await page.screenshot({ path: path.join(output, name + '.png'), fullPage: true, animations: 'disabled' })
  manifest.push({ name, purpose, variant, note })
}

async function setTheme(value) {
  const isDark = await page.evaluate(() => document.documentElement.dataset.theme === 'dark')
  if ((value === 'dark' && !isDark) || (value === 'light' && isDark)) {
    const toggle = page.locator('.theme-toggle-btn').first()
    if (await toggle.count()) {
      await toggle.click()
    } else {
      await page.evaluate(t => {
        document.documentElement.dataset.theme = t
        localStorage.setItem('prepal-theme', t)
      }, value)
    }
  }
}

async function answerQuiz() {
  for (const field of await page.locator('fieldset').all()) {
    await field.getByRole('radio').first().check()
  }
  await page.getByRole('button', { name: 'Check my answers →' }).click()
  await page.getByRole('heading', { name: 'Understand your answers.' }).waitFor()
}

try {
  // 1. Homepage & Hero with Rajasthan Map (Light & Dark)
  await visit('/')
  await setTheme('light')
  await shot('home-desktop-light', 'Homepage with Rajasthan map visual and summary stats')
  await setTheme('dark')
  await shot('home-desktop-dark', 'Homepage in dark mode with glowing Rajasthan map', 'Desktop · dark')
  await setTheme('light')

  // 2. Syllabus with Topic Counts
  await visit('/syllabus')
  await page.locator('summary').filter({ hasText: 'historical thinking' }).click()
  await shot('syllabus-desktop', 'Complete Syllabus with 152 topic count overview')

  // 3. Search Page: typo tolerance & query
  await visit('/search?q=palaeothic')
  await shot('search-palaeothic', 'Typo-tolerant search for "palaeothic" with suggestion for "palaeolithic"')
  await visit('/search?q=observation')
  await shot('search-desktop', 'Notes and PDF search results with source snippets')
  await visit('/search?q=unmatched-phrase-xyz')
  await shot('search-empty', 'Polished empty search state with suggested topics')

  // 4. Study Workspace
  await visit('/topic/reading-evidence')
  await shot('study-desktop-light', 'Study workspace with topic action controls (Bookmark & Complete)')
  await setTheme('dark')
  await shot('study-desktop-dark', 'Comfortable dark reading workspace', 'Desktop · dark')
  await setTheme('light')

  await visit('/topic/55-physiographic-divisions-of-rajasthan')
  await shot('topic-coming-soon', 'Syllabus topic with notes under editorial preparation')

  // 5. Auth Pages & Student Dashboard
  await visit('/login')
  await shot('login-desktop', 'Student account sign-in page')
  await visit('/signup')
  await shot('signup-desktop', 'Student registration page')

  await visit('/dashboard')
  await shot('dashboard-guest', 'Student dashboard guest prompt')

  // 6. AI Tutor Interaction
  await visit('/topic/reading-evidence')
  await page.getByRole('button', { name: 'Explain this passage' }).nth(1).click()
  await page.getByRole('button', { name: 'Explain simply' }).click()
  await page.locator('.citation-link').waitFor()
  await page.evaluate(() => window.scrollTo(0, 0))
  await shot('tutor-conversation-desktop', 'Selected-passage explanation with verified source link')

  // 7. Practice Quiz & Results
  await visit('/quiz/reading-evidence')
  await shot('quiz-desktop', 'Untimed student practice test')
  await answerQuiz()
  await shot('results-desktop', 'Score, explanations and return-to-lesson links')

  // 8. PDF Viewer
  await visit('/resources/1?page=2')
  await page.locator('canvas').waitFor()
  await page.getByText('Opening page 2…').waitFor({ state: 'hidden' })
  await page.getByText('Read accessible page text').click()
  await shot('pdf-desktop', 'Rendered PDF page 2 and accessible extracted text')

  // 9. About & Scope
  await visit('/about')
  await shot('about-desktop', 'Purpose and learning approach')
  await visit('/help')
  await shot('help-desktop', 'Help, privacy and student account security')

  // 10. Mobile views
  await page.setViewportSize({ width: 390, height: 844 })
  for (const [route, name, purpose] of [
    ['/', 'home-mobile', 'Responsive mobile homepage with Rajasthan graphic'],
    ['/syllabus', 'syllabus-mobile', 'Mobile syllabus directory'],
    ['/search?q=palaeothic', 'search-mobile', 'Mobile search with typo suggestion'],
    ['/topic/reading-evidence', 'study-mobile', 'Single-column lesson reading'],
    ['/login', 'login-mobile', 'Mobile student sign-in'],
    ['/resources/1?page=2', 'pdf-mobile', 'Responsive PDF page 2'],
    ['/quiz/reading-evidence', 'quiz-mobile', 'Mobile practice'],
  ]) {
    await visit(route)
    if (route === '/syllabus') await page.locator('summary').filter({ hasText: 'historical thinking' }).click()
    if (route.includes('/resources/')) {
      await page.locator('canvas').waitFor()
      await page.getByText('Opening page 2…').waitFor({ state: 'hidden' })
    }
    await shot(name, purpose, 'Mobile · light')
    if (route.includes('/quiz/')) {
      await answerQuiz()
      await shot('results-mobile', 'Mobile results and explanations', 'Mobile · light')
    }
  }

  // 11. Django Admin authoring (isolated demo)
  await page.setViewportSize({ width: 1440, height: 1000 })
  await page.goto('http://127.0.0.1:8000/admin/login/?next=/admin/')
  const credentials = await readFile('.local/demo/admin-credentials.txt', 'utf8')
  await page.getByLabel('Username:').fill('demo-editor')
  await page.getByLabel('Password:').fill(credentials.match(/Password: (.+)/)[1])
  await page.getByRole('button', { name: 'Log in' }).click()
  await page.waitForURL('**/admin/')
  await page.goto('http://127.0.0.1:8000/admin/content/topic/3/change/')
  await page.waitForLoadState('networkidle')
  await shot('admin-authoring', 'Django Admin draft content authoring', 'Desktop · Admin', 'Isolated demo Admin; synthetic content; no production login')

  await writeFile(path.join(output, 'manifest.json'), JSON.stringify({
    capturedAt: new Date().toISOString(),
    desktop: { width: 1440, height: 1000 },
    mobile: { width: 390, height: 844 },
    screens: manifest,
  }, null, 2) + '\n')
  console.log(`Captured ${manifest.length} actual application screenshots.`)
} finally {
  await browser.close()
}
