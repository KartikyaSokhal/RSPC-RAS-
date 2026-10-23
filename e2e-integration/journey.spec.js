import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test('content-first desktop journey through Django, mock tutor, PDF and stateless quiz', async ({ page }) => {
  const errors=[];page.on('pageerror',e=>errors.push(e.message))
  await page.goto('/');await page.getByRole('link',{name:/Explore Syllabus/}).first().click()
  await page.locator('summary').filter({hasText:'historical thinking'}).click();await page.getByRole('link',{name:/Reading the past, one source at a time/}).click()
  await expect(page.getByRole('heading',{name:'Observation and inference'})).toBeVisible()
  await page.locator('.block-text').nth(1).evaluate(node => {
    const range=document.createRange();range.selectNodeContents(node.querySelector('p'))
    const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range)
    node.dispatchEvent(new MouseEvent('mouseup',{bubbles:true}))
  })
  await expect(page.getByText('Selected passage',{exact:true})).toBeVisible()
  await page.getByRole('button',{name:'Explain simply'}).click()
  await expect(page.getByText('PREPAL · MOCK RESPONSE',{exact:true})).toBeVisible()
  await page.locator('.citation-link').first().click();await expect(page).toHaveURL(/#block-/)
  await page.getByRole('button',{name:'Clear selected passage'}).click()
  await expect(page.getByRole('checkbox',{name:'Include reviewed related lessons'})).toHaveCount(0)
  await page.getByRole('textbox',{name:'Ask the tutor'}).fill('Explain quantum entanglement')
  await page.getByRole('button',{name:'Send question'}).click()
  await expect(page.locator('.chat-msg-bot')).toHaveCount(2)
  await expect(page.locator('.chat-msg-bot').last().locator('.citation-link')).toHaveCount(0);
  await expect(page.locator('.chat-msg-bot').last()).toContainText('do not contain enough information');
  await page.locator('.related-lessons a[href="/topic/building-chronology"]').click();await expect(page).toHaveURL(/building-chronology$/)
  await page.locator('.resource-card').click();await expect(page.locator('canvas')).toBeVisible()
  await expect(page.getByText('Opening page 1…')).toHaveCount(0)
  await page.getByRole('button',{name:'Next PDF page'}).click();await expect(page.getByRole('combobox',{name:'PDF page'})).toHaveValue('2')
  await page.getByText('Read accessible page text').click();await expect(page.locator('.pdf-text p')).toContainText('Observation describes')
  await page.goto('/search?q=observation');await expect(page.locator('.search-result')).not.toHaveCount(0)
  await page.goto('/quiz/reading-evidence');await page.getByRole('radio').first().check()
  await page.getByRole('button',{name:'Check my answers →'}).click();await expect(page.getByRole('heading',{name:'Understand your answers.'})).toBeVisible()
  await expect(page.locator('.answer-review')).toHaveCount(5)
  await page.getByRole('button',{name:'Try again ↻'}).click();await expect(page.getByRole('radio').first()).not.toBeChecked()
  await page.goto('/topic/reading-evidence');await page.getByRole('button',{name:'Ask AI Tutor'}).click();await page.getByRole('textbox',{name:'Ask the tutor'}).fill('Explain observation and inference');await page.getByRole('button',{name:'Send question'}).click();await expect(page.locator('.citation-link')).toHaveAttribute('href', /topic\/reading-evidence#block-/);await page.locator('.citation-link').click();await expect(page.locator('.study-reader')).toBeVisible();
  expect(errors).toEqual([])
})

test('mobile navigation, themes, selected text and responsive pages', async ({ page }) => {
  await page.setViewportSize({width:390,height:844})
  await page.goto('/');await page.getByRole('button',{name:'Switch to dark theme'}).click()
  await expect(page.locator('html')).toHaveAttribute('data-theme','dark')
  await page.getByRole('link',{name:/Explore Syllabus/}).first().click()
  await page.locator('summary').filter({hasText:'historical thinking'}).click();await page.getByRole('link',{name:/Reading the past, one source at a time/}).click()
  await expect(page.locator('.study-reader')).toBeVisible();await expect(page.locator('.floating-tutor-popup')).toHaveCount(0)
  await page.getByRole('button',{name:'Explain this passage'}).nth(1).click()
  await expect(page.locator('.floating-tutor-popup')).toBeVisible()
  await page.getByRole('button',{name:'Explain simply'}).click();await expect(page.locator('.citation-link')).toBeVisible()
  await page.locator('.citation-link').click();await expect(page.locator('.study-reader')).toBeVisible()
  for(const route of ['/','/syllabus','/search?q=observation','/resources/1?page=2','/quiz/reading-evidence','/about','/help','/missing']) {
    await page.goto(route);await page.locator('h1,h2').first().waitFor()
    await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  }
})

test('keyboard and automated accessibility checks on principal pages', async ({ page }) => {
  await page.emulateMedia({reducedMotion:'reduce'})
  for(const route of ['/','/syllabus','/topic/reading-evidence','/search?q=observation','/quiz/reading-evidence','/resources/1?page=1','/help']) {
    await page.goto(route);await page.locator('h1').first().waitFor()
    if(route.includes('/resources/')) await expect(page.getByText('Opening page 1…')).toHaveCount(0)
    for (const theme of ['light','dark']) {
      if (await page.locator('html').getAttribute('data-theme') !== theme) {
        await page.getByRole('button',{name:`Switch to ${theme} theme`}).click()
      }
      const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze()
      expect(result.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)})), `${route} / ${theme}`).toEqual([])
    }
  }
  await page.goto('/');await page.getByRole('link',{name:'Skip to content'}).waitFor({state:'attached'});await page.keyboard.press('Tab');await expect(page.getByRole('link',{name:'Skip to content'})).toBeFocused()
  await page.emulateMedia({reducedMotion:'reduce'});await expect(page.locator('html')).toHaveCSS('scroll-behavior','auto')
})

test('production CSP permits the study flow and defers PDF assets until requested', async ({ page }) => {
  const requests=[]
  page.on('request',request=>requests.push(request.url()))
  await page.addInitScript(()=>{window.prepalCspViolations=[];document.addEventListener('securitypolicyviolation',event=>window.prepalCspViolations.push(event.violatedDirective))})
  const policy="default-src 'self'; script-src 'self'; worker-src 'self' blob:; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"
  await page.route('**/*',async route=>{
    if(route.request().isNavigationRequest()) {
      const response=await route.fetch()
      await route.fulfill({response,headers:{...response.headers(),'content-security-policy':policy}})
    } else await route.continue()
  })
  await page.goto('/');await page.getByRole('link',{name:/Explore Syllabus/}).waitFor()
  expect(requests.some(url=>/pdf\.worker|\/assets\/pdf-/.test(url))).toBe(false)
  await page.goto('/resources/1?page=2');await page.locator('canvas').waitFor();await page.locator('.pdf-loading').waitFor({state:'hidden'})
  expect(requests.some(url=>/pdf\.worker/.test(url))).toBe(true)
  expect(await page.evaluate(()=>window.prepalCspViolations)).toEqual([])
})
