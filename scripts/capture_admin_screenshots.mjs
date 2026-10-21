// Explicitly invoked local demo capture. Never embed or print credentials.
import { chromium } from '@playwright/test'
import { mkdir, readFile } from 'node:fs/promises'
import path from 'node:path'

const demoRoot = process.env.PREPAL_DEMO_ROOT
const base = process.env.PREPAL_ADMIN_URL || 'http://127.0.0.1:8000'
if (!demoRoot || !path.isAbsolute(demoRoot) || !/^http:\/\/127\.0\.0\.1:\d+$/.test(base)) {
  throw new Error('Set an absolute PREPAL_DEMO_ROOT and a loopback-only PREPAL_ADMIN_URL.')
}
const output = path.join(demoRoot, 'screenshots', new Date().toISOString().replaceAll(':', '-'))
const browser = await chromium.launch({ headless: true })
try {
  const page = await browser.newPage({ viewport: { width: 1380, height: 950 } })
  await page.route('**/*', route => new URL(route.request().url()).origin === base ? route.continue() : route.abort())
  const config = await (await page.request.get(`${base}/api/config/`)).json()
  if (!config.demo) throw new Error('Refusing capture outside an isolated demo.')
  const credentials = await readFile(path.join(demoRoot, 'admin-credentials.txt'), 'utf8')
  const username = credentials.match(/^Username: (.+)$/m)?.[1]
  const password = credentials.match(/^Password: (.+)$/m)?.[1]
  if (!username || !password) throw new Error('Demo credential file is incomplete.')
  await mkdir(output, { recursive: true, mode: 0o700 })
  await page.goto(`${base}/admin/login/?next=/admin/`)
  await page.locator('[name=username]').fill(username)
  await page.locator('[name=password]').fill(password)
  await page.locator('input[type=submit]').click()
  await page.waitForURL(`${base}/admin/`)
  await page.screenshot({ path: path.join(output, 'admin-dashboard.png'), fullPage: true })
  const hierarchy = await (await page.request.get(`${base}/api/topics/?tree=1`)).json()
  function firstLesson(nodes) {
    for (const node of nodes) {
      if (node.has_notes) return node
      const child = firstLesson(node.children || [])
      if (child) return child
    }
  }
  const lesson = firstLesson(hierarchy)
  if (!lesson) throw new Error('No published demo lesson is available to capture.')
  for (const [name, route] of [
    ['topic-tree', '/admin/content/topic/tree/'],
    ['topic-editor', `/admin/content/topic/${lesson.id}/change/`],
    ['draft-preview', `/admin/content/topic/${lesson.id}/preview/`],
    ['practice-questions', '/admin/content/quiz/'],
  ]) {
    await page.goto(base + route)
    await page.locator('main,#content').first().waitFor()
    await page.screenshot({ path: path.join(output, `${name}.png`), fullPage: true })
  }
  console.log('Demo Admin screenshots saved under the selected private demo directory.')
} finally {
  await browser.close()
}
