import { test, expect } from '@playwright/test'
import { intercept } from './fixtures.js'
test.beforeEach(async ({page})=>intercept(page,{quiz:{id:1,title:'Legacy preview',time_limit_seconds:1,questions:[{id:1,question_text:'Read this fixture?',choices:[{id:1,choice_text:'Local choice'}]}]}}))
test('reader provides safe guest controls and explains student account benefits',async({page})=>{
 await page.goto('/topic/fixture-history');await expect(page.getByText(/Sign in to save this topic to your bookmarks/)).toBeVisible()
 await expect(page.getByRole('button',{name:/Bookmark/i})).toBeVisible()
 await page.getByRole('link',{name:'Practice this lesson →'}).click();await expect(page.getByText('Local choice')).toBeVisible()
})
test('legacy preview never submits manually or automatically',async({page})=>{
 const posts=[];page.on('request',r=>{if(r.method()==='POST')posts.push(r.url())});await page.clock.install()
 await page.goto('/quiz/fixture-history');await page.getByRole('radio',{name:/Local choice/}).check()
 await expect(page.getByRole('button',{name:'Check my answers →'})).toBeDisabled()
 await page.clock.fastForward(60000);await expect(page.locator('.timer-box')).toHaveCount(0);expect(posts).toEqual([])
})
