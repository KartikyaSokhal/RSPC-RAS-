import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, expect, it } from 'vitest'
import axios from 'axios'
import App from '../App.jsx'
import { mockAPI, config, topic } from './fixtures.js'
beforeEach(() => { window.history.replaceState({}, '', '/quiz/fixture-history'); mockAPI() })
it('explains unavailable reviewed practice and retains reading navigation', async () => {
  const user = userEvent.setup()
  axios.get.mockImplementation(url => url.endsWith('/quiz/') ? Promise.reject({ response: { status: 404 } }) : Promise.resolve({ data: url.endsWith('/config/') ? config : url.includes('/topics/') ? [] : topic }))
  render(<App />)
  expect(await screen.findByRole('heading', { name: 'No reviewed quiz is available yet.' })).toBeVisible()
  await user.click(screen.getAllByRole('link', { name: /Back to the lesson/ })[0])
  expect(await screen.findByText('Curated fixture notes.')).toBeVisible(); expect(axios.post).not.toHaveBeenCalled()
})
it('distinguishes network failure without exposing private diagnostics', async () => {
  axios.get.mockImplementation(url => url.endsWith('/config/') ? Promise.resolve({ data: config }) : Promise.reject(new Error('Private diagnostic')))
  render(<App />)
  expect(await screen.findByRole('heading', { name: 'Practice could not load.' })).toBeVisible()
  expect(screen.queryByText('Private diagnostic')).toBeNull()
})
it('ignores a late response from a previously selected quiz', async () => {
  let resolveOld
  axios.get.mockImplementation(url => url.endsWith('/config/') ? Promise.resolve({ data: config }) : url.includes('/fixture-history/') ? new Promise(resolve => { resolveOld = resolve }) : Promise.reject({ response: { status: 404 } }))
  render(<App />)
  await screen.findByText('Opening the practice set…')
  await act(async () => { window.history.pushState({}, '', '/quiz/other-topic'); window.dispatchEvent(new PopStateEvent('popstate')) })
  await screen.findByRole('heading', { name: 'No reviewed quiz is available yet.' })
  await act(async () => { resolveOld({ data: { id: 1, title: 'Stale quiz', questions: [] } }) })
  expect(screen.queryByText('Stale quiz')).toBeNull()
})
