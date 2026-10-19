import { test, expect } from '@playwright/test'
import { intercept } from './fixtures.js'
test.beforeEach(async ({ page }) => intercept(page))
test('catalog navigation renders safe notes from fixture API', async ({ page }) => {
  const errors=[];page.on('pageerror',e=>errors.push(e.message))
  await page.goto('/'); await page.getByText('Fixture History',{exact:true}).click()
  await expect(page).toHaveURL(/\/topic\/fixture-history$/)
  await expect(page.getByText('Curated browser fixture notes.')).toBeVisible()
  await expect(page.getByRole('link',{name:'Practice this lesson →'})).toBeVisible()
  expect(errors).toEqual([])
})
test('chat request is topic-scoped and uses a mock only', async ({ page }) => {
  await page.goto('/topic/fixture-history')
  await page.getByRole('button', { name: 'Ask AI Tutor' }).click()
  await page.getByRole('textbox', { name: 'Ask the tutor' }).fill('Explain the fixture')
  await page.getByRole('button', { name: 'Send question' }).click()
  await expect(page.getByText('Offline mocked browser answer.')).toBeVisible()
})
