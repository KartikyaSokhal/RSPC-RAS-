import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'
import { uiHierarchy } from '../src/test/uiHierarchy.js'

const target = { id: 2, title: 'Second subject', slug: 'ui-2', description: 'A published context from approved sources.' }
const topic = { id: 1221, title: 'Nested concept', slug: 'ui-1221', is_published: true, revision: 1, children: [], resources: [],
  blocks: [{ id: 1, block_type: 'text', content: '<h2>Reading with context</h2><p>Second subject offers published context.</p>' }],
  keyword_links: [{ block_id: 1, node_index: 1, start: 0, end: 14, text: 'Second subject', target }],
  related: [{ ...target, kind: 'related', reason: 'Reviewed connection' }], tags: [{ id: 1, slug: 'ui-tag', name: 'Fixture tag' }],
}

test.beforeEach(async ({ page }) => {
  await page.route('**/*', async route => {
    const url = new URL(route.request().url())
    if (url.origin !== 'http://127.0.0.1:4173') return route.abort('blockedbyclient')
    if (!url.pathname.startsWith('/api/')) return route.continue()
    if (url.pathname === '/api/config/') return route.fulfill({ json: { demo: true, csrf_token: 'fixture', ai_enabled: false } })
    if (url.pathname === '/api/topics/') return route.fulfill({ json: uiHierarchy })
    if (url.pathname === '/api/topic/ui-1221/') return route.fulfill({ json: topic })
    if (url.pathname === '/api/topic/ui-2/context/') return route.fulfill({ json: target })
    throw new Error(`Unexpected UI test API request: ${route.request().method()} ${url.pathname}`)
  })
})

async function settleMotion(page) {
  await page.evaluate(() => Promise.all(document.getAnimations()
    .filter(animation => animation.effect?.getComputedTiming().iterations !== Infinity)
    .map(animation => animation.finished.catch(() => {}))))
}

async function fitsViewport(locator) {
  expect(await locator.evaluateAll(nodes => nodes.every(node => {
    const box = node.getBoundingClientRect()
    return box.left >= -1 && box.right <= innerWidth + 1
  }))).toBe(true)
}

for (const width of [1280, 1024, 768, 390, 320]) {
  test(`homepage, hierarchy and reader stay usable at ${width}px`, async ({ page }, testInfo) => {
    const errors = []; page.on('pageerror', error => errors.push(error.message))
    await page.setViewportSize({ width, height: 850 })
    await page.goto('/')
    await expect(page.locator('.footer-center')).toContainText('5 Subjects · 14 Curriculum Topics')
    const header = page.getByRole('banner')
    await expect(header.getByRole('link')).toHaveCount(2)
    await expect(header.getByRole('link', { name: 'Search' })).toBeVisible()
    await fitsViewport(header.locator('.brand, .header-controls'))
    await expect(page.getByRole('searchbox')).toHaveCount(0)
    await expect(page.locator('.subject-navigation button')).toHaveCount(5)
    await fitsViewport(page.locator('.subject-navigation button'))
    const map = await page.locator('.rajasthan-vector-svg').boundingBox()
    expect(Math.abs(map.width / map.height - 600 / 560)).toBeLessThan(0.01)
    for (const theme of ['light', 'dark']) {
      if (await page.locator('html').getAttribute('data-theme') !== theme) await header.getByRole('button', { name: `Switch to ${theme} theme` }).click()
      // Measure the selected theme after finite transitions/entrance motion.
      await settleMotion(page)
      if ([1280, 390].includes(width)) {
        const scan = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()
        expect(scan.violations.map(v => ({ id: v.id, nodes: v.nodes.map(n => ({ target: n.target, summary: n.failureSummary })) }))).toEqual([])
      }
      await page.screenshot({ path: testInfo.outputPath(`home-${theme}.png`) })
    }
    await page.getByRole('button', { name: '5. Fifth subject' }).click()
    await expect(page.locator('#home-subject-5 > summary')).toBeFocused()
    expect(await page.locator('#home-subject-5').evaluate(node => node.getBoundingClientRect().top)).toBeGreaterThanOrEqual(-1)
    await page.getByRole('button', { name: 'Expand All' }).click()
    await expect(page.getByRole('link', { name: /Nested concept/ })).toBeVisible()
    await fitsViewport(page.locator('.tree-leaf'))
    await page.getByRole('button', { name: 'Collapse All' }).click()
    await expect(page.locator('.syllabus-tree > details > summary')).toHaveCount(5)
    await expect(page.locator('.syllabus-tree details[open]')).toHaveCount(0)
    await expect(page.getByRole('link', { name: /Nested concept/ })).toHaveCount(0)
    const first = page.locator('#home-subject-1 > summary')
    await first.focus(); await page.keyboard.press('Enter')
    await expect(page.locator('#home-subject-1')).toHaveAttribute('open', '')
    await page.keyboard.press('Space')
    await expect(page.locator('#home-subject-1')).not.toHaveAttribute('open')
    await page.getByRole('button', { name: 'Expand All' }).click()
    await page.getByRole('link', { name: /Nested concept/ }).click()
    await expect(page).toHaveURL(/\/topic\/ui-1221$/)
    await expect(page.getByRole('heading', { name: 'Reading with context' })).toBeVisible()
    if (width < 1024) await page.getByRole('button', { name: 'Syllabus', exact: true }).click()
    await page.getByRole('searchbox', { name: 'Filter sidebar syllabus' }).fill('Fifth subject unit')
    await expect(page.locator('.study-sidebar .tree-number')).toHaveText(['5', '5.1'])
    if (width < 1024) await page.getByRole('button', { name: 'Reading', exact: true }).click()
    for (const theme of ['light', 'dark']) {
      if (await page.locator('html').getAttribute('data-theme') !== theme) await header.getByRole('button', { name: `Switch to ${theme} theme` }).click()
      // Measure the selected theme after finite transitions/entrance motion.
      await settleMotion(page)
      if ([1280, 390].includes(width)) {
        const scan = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()
        expect(scan.violations.map(v => ({ id: v.id, nodes: v.nodes.map(n => ({ target: n.target, summary: n.failureSummary })) }))).toEqual([])
      }
    }
    await expect(page.locator('.floating-tutor-launcher')).toHaveCount(1)
    await expect(page.locator('.toolbar-tutor-btn')).toHaveCount(0)
    await expect(page.getByRole('button', { name: 'AI tutor', exact: true })).toHaveCount(0)
    const launcher = page.getByRole('button', { name: 'Ask AI Tutor' })
    await launcher.focus(); const scrollBefore = await page.evaluate(() => scrollY)
    await page.keyboard.press('Enter')
    const tutor = page.getByRole('dialog', { name: 'AI Study Assistant' })
    await expect(tutor).toBeVisible()
    await expect(tutor.getByRole('button', { name: 'Close AI Assistant' })).toBeFocused()
    await fitsViewport(tutor)
    await expect(tutor.getByRole('textbox', { name: 'Ask the tutor' })).toBeInViewport()
    await settleMotion(page)
    await page.screenshot({ path: testInfo.outputPath('tutor.png') })
    if ([1280, 390].includes(width)) {
      const scan = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()
      expect(scan.violations.map(v => ({ id: v.id, nodes: v.nodes.map(n => ({ target: n.target, summary: n.failureSummary })) }))).toEqual([])
    }
    await page.keyboard.press('Escape')
    await expect(tutor).toHaveCount(0); await expect(launcher).toBeFocused()
    expect(await page.evaluate(() => scrollY)).toBe(scrollBefore)
    await launcher.click()
    await page.getByRole('button', { name: 'Close AI Assistant' }).click()
    await expect(tutor).toHaveCount(0)
    await expect(page.locator('.related-lessons a')).toHaveAttribute('href', '/topic/ui-2')
    await expect(page.getByRole('link', { name: 'Fixture tag' })).toHaveAttribute('href', '/tags/ui-tag')
    const connection = page.locator('a.keyword-connection')
    await expect(connection).toHaveCount(1)
    await connection.click()
    await expect(page.getByRole('dialog', { name: target.title })).toBeVisible()
    await expect(page.getByRole('link', { name: /Open Full Topic/ })).toHaveAttribute('target', '_blank')
    await page.keyboard.press('Escape'); await expect(connection).toBeFocused()
    await expect.poll(() => page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
    expect(errors).toEqual([])
  })
}

test('header Search opens the existing search page and footer has no inactive social controls', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('banner').getByRole('link', { name: 'Search' }).click()
  await expect(page).toHaveURL(/\/search$/)
  await expect(page.getByRole('searchbox', { name: 'Search syllabus topics and published notes' })).toBeVisible()
  await expect(page.getByRole('contentinfo').getByRole('link', { name: /About/ })).toHaveCount(0)
  await expect(page.locator('.footer-social-space a,.footer-social-space button')).toHaveCount(0)
})
