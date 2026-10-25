import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'

const accounts = JSON.parse(readFileSync(join(process.env.PREPAL_DEMO_ROOT, 'accounts.json'), 'utf8'))
const corpus = JSON.parse(readFileSync(new URL('../backend/content/fixtures/sample_lessons_v1.json', import.meta.url), 'utf8'))

async function login(page, username = 'demo-reader') {
  await page.getByLabel('Username', {exact:true}).fill(username)
  await page.getByLabel('Password', {exact:true}).fill(accounts[username])
  await page.getByRole('button', {name: /Sign in to Dashboard/}).click()
}

for (const width of [390, 1280]) {
  test(`public home, protected learning and owned session journey at ${width}px`, async ({page, browser}) => {
    await page.setViewportSize({width, height:900})
    await page.emulateMedia({reducedMotion:'reduce'})
    const guestContentRequests = []
    page.on('request', request => { if (/\/api\/(topics|topic|search|tags|resources)\//.test(request.url())) guestContentRequests.push(request.url()) })
    const response = await page.goto('/')
    expect(response.status()).toBe(200)
    expect(response.headers()['www-authenticate']).toBeUndefined()
    await expect(page.getByRole('heading', {name:'Sign in to explore the syllabus'})).toBeVisible()
    await expect(page.getByText('5 Subjects · 142 Curriculum Topics')).toBeVisible()
    await page.goto('/signup')
    await expect(page.getByRole('heading', {name:'Student registration is not available'})).toBeVisible()
    await expect(page.getByRole('textbox')).toHaveCount(0)
    expect(guestContentRequests).toEqual([])
    for (const route of ['/api/topics/?tree=1', '/api/topic/a-temples/', '/api/topic/a-temples/quiz/', '/api/search/?q=temple', '/api/bookmarks/', '/api/plans/']) {
      const denied = await page.request.get(route)
      expect(denied.status()).toBe(401)
      expect(denied.headers()['www-authenticate']).toBeUndefined()
      expect((await denied.json()).error.code).toBe('auth_required')
    }
    await page.goto('/topic/a-temples?view=notes#block-1')
    await expect(page).toHaveURL(/\/login$/)
    await login(page)
    await expect(page).toHaveURL(/\/topic\/a-temples\?view=notes#block-1$/)
    await expect(page.locator('.study-reader')).toBeVisible()
    // A previous interrupted run may have changed this disposable account.
    if (await page.getByRole('button', {name:/Remove Bookmark/}).count()) await page.getByRole('button', {name:/Remove Bookmark/}).click()
    if (await page.getByRole('button', {name:/Mark as Incomplete/}).count()) await page.getByRole('button', {name:/Mark as Incomplete/}).click()
    await page.getByRole('button', {name:/Bookmark Topic/}).click()
    await expect(page.getByRole('button', {name:/Remove Bookmark/})).toHaveAttribute('aria-pressed','true')
    await page.getByRole('button', {name:/Mark as Completed/}).click()
    await page.reload()
    await expect(page.getByRole('button', {name:/Mark as Incomplete/})).toHaveAttribute('aria-pressed','true')
    await page.goto('/quiz/a-temples')
    const lesson = corpus.lessons.find(lesson => lesson.topic_id === 30)
    for (const [i,question] of lesson.questions.entries()) await page.locator('fieldset').nth(i).getByRole('radio', {name:question.choices[question.answer], exact:true}).check()
    await page.getByRole('button', {name:'Check my answers →'}).click()
    await expect(page.getByText('Saved to your account.', {exact:false})).toBeVisible()
    await page.getByRole('link', {name:'Open practice history'}).click()
    const attempt = page.url()
    await expect(page.getByText('5 / 5 correct', {exact:false})).toBeVisible()
    await page.goto('/planner')
    await page.getByLabel('a. Temples', {exact:true}).check()
    await page.getByRole('button', {name:'Generate study plan'}).click()
    await expect(page.getByText('Estimated completion:', {exact:false})).toBeVisible()
    await page.goto('/dashboard')
    await expect(page.getByRole('region', {name:'Learning Progress Overview'})).toContainText('1 / 15')
    const other = await browser.newContext({baseURL:'http://127.0.0.1:4175'})
    const otherPage = await other.newPage()
    await otherPage.goto('/login'); await login(otherPage, 'demo-other')
    await expect(otherPage).toHaveURL(/dashboard$/)
    await expect(otherPage.getByRole('region', {name:'Learning Progress Overview'})).toContainText('0 / 15')
    expect((await other.request.get(new URL(attempt).pathname.replace('/attempts/', '/api/attempts/')+'/')).status()).toBe(404)
    await other.close()
    await page.locator('.account-menu summary').click()
    await page.getByRole('button', {name:'Logout', exact:true}).click()
    await expect(page).toHaveURL(/login$/)
    expect((await page.request.get('/api/dashboard/')).status()).toBe(401)
    // Check each public surface in both themes, including keyboard-accessible controls.
    for (const route of ['/', '/login', '/signup']) {
      await page.goto(route); await page.locator('h1').waitFor()
      for (const theme of ['light','dark']) {
        if (await page.locator('html').getAttribute('data-theme') !== theme) await page.getByRole('button', {name:`Switch to ${theme} theme`}).click()
        await expect.poll(() => page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
        const scan = await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze()
        expect(scan.violations.map(v=>v.id)).toEqual([])
      }
    }
    // Restore only this new synthetic user's state so the next viewport starts clean.
    await page.goto('/login'); await login(page)
    await expect(page).toHaveURL(/dashboard$/)
    await page.goto('/topic/a-temples')
    await page.getByRole('button', {name:/Remove Bookmark/}).click()
    await page.getByRole('button', {name:/Mark as Incomplete/}).click()
  })
}

test('Admin keeps its separate staff permission check and read-only content', async ({page}) => {
  await page.goto('http://127.0.0.1:8001/admin/')
  await expect(page).toHaveURL(/admin\/login/)
  await page.getByLabel('Username').fill('demo-reader')
  await page.getByLabel('Password').fill(accounts['demo-reader'])
  await page.getByRole('button', {name:'Log in', exact:true}).click()
  await expect(page.locator('.errornote')).toBeVisible()
  await page.getByLabel('Username').fill('sample-editor')
  await page.getByLabel('Password').fill(accounts['sample-editor'])
  await page.getByRole('button', {name:'Log in', exact:true}).click()
  await expect(page.getByRole('heading', {name:'Educational Content Management'})).toBeVisible()
  await expect(page.locator('a.addlink')).toHaveCount(0)
  expect((await page.request.get('http://127.0.0.1:8001/api/topics/')).status()).toBe(401)
  const staticURL = await page.locator('link[rel="stylesheet"]').first().getAttribute('href')
  expect((await page.request.get('http://127.0.0.1:8001'+staticURL)).status()).toBe(200)
})
