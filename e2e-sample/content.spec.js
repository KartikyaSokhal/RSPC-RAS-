import { test, expect } from '@playwright/test'
import { readFileSync } from 'node:fs'
import AxeBuilder from '@axe-core/playwright'

const corpus = JSON.parse(readFileSync(new URL('../backend/content/fixtures/sample_lessons_v1.json', import.meta.url)))
const hierarchy = JSON.parse(readFileSync(new URL('../backend/content/fixtures/syllabus_142.json', import.meta.url)))
const topics = new Map(hierarchy.map(topic => [topic.id, topic]))

test.beforeEach(async ({ context }) => {
  await context.route('**/*', route => {
    const url = new URL(route.request().url())
    return ['127.0.0.1', 'localhost'].includes(url.hostname) ? route.continue() : route.abort()
  })
})

test('all 15 actual syllabus lessons render notes, references, approved links and related topics', async ({ page }) => {
  for (const lesson of corpus.lessons) {
    await page.goto(`/topic/${topics.get(lesson.topic_id).slug}`)
    const notes = page.locator('.lesson-content')
    await expect(notes).toContainText('Local development sample — not production material.')
    for (const section of lesson.sections) {
      await expect(notes.getByRole('heading', { name: section.heading, exact: true })).toBeVisible()
      await expect(notes).toContainText(section.paragraphs[0])
    }
    for (const key of lesson.sources) {
      await expect(notes.getByRole('link', { name: corpus.sources[key].title, exact: true })).toHaveAttribute('href', corpus.sources[key].url)
    }
    await expect(notes.locator('a.keyword-connection')).toHaveCount(lesson.connections.length)
    for (const edge of lesson.connections) {
      await expect(page.locator(`.related-lessons a[href="/topic/${topics.get(edge.target_id).slug}"]`)).toHaveCount(1)
    }
    await notes.locator('a.keyword-connection').first().click()
    await expect(page.getByRole('dialog').getByRole('link', { name: /Open Full Topic/ })).toBeVisible()
    await page.keyboard.press('Escape')
    await expect(page.getByRole('dialog')).toHaveCount(0)
  }
})

test('all controlled tag pages list the right published sample articles', async ({ page, request }) => {
  const seen = new Set()
  for (const lesson of corpus.lessons) {
    const detail = await (await request.get(`/api/topic/${topics.get(lesson.topic_id).slug}/`)).json()
    for (const tag of detail.tags) {
      if (seen.has(tag.slug)) continue
      seen.add(tag.slug)
      const expected = corpus.lessons.filter(row => row.tags.includes(tag.name))
      await page.goto(`/tags/${tag.slug}`)
      await expect(page.getByRole('heading', { level: 1, name: tag.name })).toBeVisible()
      await expect(page.locator('.search-result')).toHaveCount(expected.length)
      for (const row of expected) {
        await expect(page.locator(`.search-result[href="/topic/${topics.get(row.topic_id).slug}"]`)).toHaveCount(1)
      }
    }
  }
  expect(seen.size).toBe(19)
})

test('five subject pools have 15 distinct relevant questions each and grade all 75 correctly', async ({ page, request }) => {
  const used = new Set()
  const answers = new Map(corpus.lessons.flatMap(lesson => lesson.questions.map(q => [q.question, q.choices[q.answer]])))
  for (const root of hierarchy.filter(row => row.parent_id === null)) {
    const preview = await (await request.get(`/api/topic/${root.slug}/practice/`)).json()
    expect(preview.count).toBe(15)
    for (const question of preview.questions) {
      expect(used.has(question.id)).toBe(false)
      used.add(question.id)
    }
    await page.goto(`/practice/${root.slug}`)
    await expect(page.locator('fieldset')).toHaveCount(15)
    for (const question of preview.questions) {
      const field = page.locator('fieldset').filter({ hasText: question.question_text })
      await field.getByRole('radio', { name: answers.get(question.question_text), exact: true }).check()
    }
    await page.getByRole('button', { name: 'Check my answers →' }).click()
    await expect(page.getByRole('heading', { name: 'Understand your answers.' })).toBeVisible()
    await expect(page.locator('.answer-review.correct')).toHaveCount(15)
    await expect(page.getByText('These results are held only in this page. No learner attempt has been saved.')).toBeVisible()
  }
  expect(used.size).toBe(75)
})

test('mobile sample reader keeps popup focus, new-tab navigation and readable light/dark layout', async ({ page, context }, testInfo) => {
  await page.setViewportSize({ width: 390, height: 844 })
  await page.goto('/topic/a-temples')
  const trigger = page.locator('.lesson-content a.keyword-connection').first()
  await trigger.scrollIntoViewIfNeeded()
  await trigger.focus()
  const position = await page.evaluate(() => scrollY)
  await page.keyboard.press('Enter')
  const dialog = page.getByRole('dialog')
  await expect(dialog.getByRole('button', { name: 'Close topic preview' })).toBeFocused()
  const fullLink = dialog.getByRole('link', { name: /Open Full Topic/ })
  await expect(fullLink).toBeVisible()
  const opened = context.waitForEvent('page')
  await fullLink.click()
  const tab = await opened
  await expect(tab.locator('.lesson-content')).toContainText('Local development sample')
  await tab.close()
  await page.keyboard.press('Escape')
  await expect(trigger).toBeFocused()
  expect(await page.evaluate(() => scrollY)).toBe(position)
  for (const theme of ['light', 'dark']) {
    if (theme === 'dark') await page.getByRole('button', { name: /Switch to dark/i }).click()
    await page.evaluate(async () => {
      await Promise.all(document.getAnimations().filter(a => a.effect?.getComputedTiming().iterations !== Infinity).map(a => a.finished.catch(() => {})))
    })
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
    const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()
    expect(results.violations.map(v => v.id)).toEqual([])
    await page.screenshot({ path: testInfo.outputPath(`sample-mobile-${theme}.png`) })
  }
})
