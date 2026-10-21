import { test, expect } from '@playwright/test'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'

test('Admin creates draft rich text, reviews it, publishes explicitly and withdraws', async ({ page }) => {
  // Generated credentials belong only to the separately prepared synthetic DB.
  const credentials = readFileSync(join(process.env.PREPAL_DEMO_ROOT, 'admin-credentials.txt'), 'utf8')
  const username = credentials.match(/^Username: (.+)$/m)[1]
  const password = credentials.match(/^Password: (.+)$/m)[1]
  const admin = 'http://127.0.0.1:8001'
  const errors = []; page.on('pageerror', e => errors.push(e.message))
  await page.goto(`${admin}/admin/login/?next=/admin/`)
  await page.locator('[name=username]').fill(username)
  await page.locator('[name=password]').fill(password)
  await page.locator('input[type=submit]').click()
  await expect(page).toHaveURL(`${admin}/admin/`)
  for (const name of ['Topics', 'Content', 'Practice Questions']) {
    await expect(page.locator('caption').getByRole('link', { name, exact: true })).toBeVisible()
  }
  await page.goto(`${admin}/admin/content/tag/add/`)
  await page.locator('#id_name').fill('Browser editorial fixture')
  await page.locator('[name=_save]').click()
  await expect(page.locator('.messagelist')).toContainText('added successfully')
  await page.goto(`${admin}/admin/content/topic/add/`)
  await page.locator('#id_title').fill('Phase 2 browser editorial fixture')
  await page.locator('#id_order').fill('900')
  // The existing WYSIWYG remains the notes editor.
  await page.locator('#id_blocks-0-block_type').selectOption('text')
  await page.locator('#id_blocks-0-order').fill('1')
  const editor = page.locator('.prepal-wysiwyg-editor').first()
  await editor.evaluate(node => {
    node.innerHTML = '<h2>Browser draft evidence</h2><table><tbody><tr><th>Source</th><th>Evidence</th></tr><tr><td>Fixture</td><td>Supported</td></tr></tbody></table>'
    node.dispatchEvent(new Event('input', { bubbles: true }))
  })
  await page.locator('#id_blocks-0-source_reference').fill('Synthetic browser reference')
  await page.locator('[name=_save]').last().click()
  await expect(page.locator('.messagelist')).toContainText('added successfully')
  await page.locator('#result_list').getByRole('link', {name:'Phase 2 browser editorial fixture', exact:true}).click()
  const changeUrl = page.url()
  const slug = await page.locator('#id_slug').inputValue()
  const topicUrl = `${admin}/api/topic/${slug}/`
  await expect(page.locator('.prepal-wysiwyg-editor').first()).toContainText('Browser draft evidence')
  const previewUrl = await page.getByRole('link', {name:/Preview Draft/}).getAttribute('href')
  await page.goto(`${admin}${previewUrl}`)
  await expect(page.locator('main')).toContainText('Browser draft evidence')
  let response = await page.request.get(topicUrl)
  expect((await response.json()).status).toBe('coming_soon')
  await page.goto(changeUrl)
  await page.getByRole('button', {name:'Submit for review'}).click()
  await expect(page.locator('.messagelist')).toContainText('submitted for review')
  await expect(page.getByText('Awaiting review', {exact: true})).toBeVisible()
  await page.getByRole('button', {name:'Review & Publish'}).click()
  await expect(page.locator('.messagelist')).toContainText('Published')
  response = await page.request.get(topicUrl)
  expect((await response.json()).blocks[0].content).toContain('Browser draft evidence')
  page.once('dialog', dialog => dialog.accept())
  await page.getByRole('button', {name:/Withdraw/}).click()
  await expect(page.locator('.messagelist')).toContainText('withdrawn')
  response = await page.request.get(topicUrl)
  expect((await response.json()).status).toBe('coming_soon')
  expect(errors).toEqual([])
})
