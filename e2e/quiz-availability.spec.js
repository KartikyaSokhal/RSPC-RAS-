import { test, expect } from '@playwright/test'
import { intercept } from './fixtures.js'
for(const available of [false,true])test(`reviewed preview availability ${available} preserves reading`,async({page})=>{
 await intercept(page,{quiz:available?{id:1,title:'Reviewed fixture',questions:[{id:1,question_text:'Which choice?',choices:[{id:1,choice_text:'First choice'},{id:2,choice_text:'Second choice'}]}]}:undefined})
 await page.goto('/quiz/fixture-history')
 if(available){await page.getByRole('radio',{name:/Second choice/}).check();await expect(page.locator('.choice-option.selected')).toContainText('Second choice')}
 else await expect(page.getByRole('heading',{name:'No reviewed quiz is available yet.'})).toBeVisible()
 await page.getByRole('link',{name:/Back to the lesson/}).first().click();await expect(page.getByText('Curated browser fixture notes.')).toBeVisible()
})
