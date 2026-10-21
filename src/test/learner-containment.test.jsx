import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, expect, it } from 'vitest'
import axios from 'axios'
import App from '../App.jsx'
import { mockAPI, quiz } from './fixtures.js'

beforeEach(() => { window.history.replaceState({}, '', '/topic/fixture-history'); mockAPI() })
it('disables learner controls and ignores stale owned status without requesting shared records', async () => {
  render(<App />); await screen.findByText('Curated fixture notes.')
  expect(screen.getByText(/Student accounts, bookmarks, completion tracking/)).toBeVisible()
  const bookmarkBtn = screen.getByRole('button', { name: /Bookmark/i })
  expect(bookmarkBtn).toBeDisabled()
  expect(screen.getByRole('button', { name: /Mark as Completed/i })).toBeDisabled()
  expect(screen.queryByRole('button', { name: /^Bookmarked$/i })).toBeNull()
  // As a guest, clicking bookmark does not mutate shared records on the backend
  expect(axios.post).not.toHaveBeenCalled()
  expect(axios.get.mock.calls.every(([url]) => !/weakness/.test(url))).toBe(true)
})
it('ignores stale global completion flags on the home catalog', async () => {
  window.history.replaceState({}, '', '/'); const { container } = render(<App />)
  await screen.findByText('Fixture History'); expect(container.querySelector('.completed-mark')).toBeNull()
  expect(container.textContent).not.toContain('⭐')
})
it('does not allow legacy preview payloads to call the old submission route', async () => {
  const user = userEvent.setup(); mockAPI({ practice: { ...quiz, revision_token: undefined } })
  window.history.replaceState({}, '', '/quiz/fixture-history'); render(<App />)
  await user.click(await screen.findByRole('radio', { name: /Correct fixture/ }))
  expect(screen.getByRole('button', { name: 'Check my answers →' })).toBeDisabled()
  expect(screen.getByRole('status')).toHaveTextContent('Preview only')
  expect(axios.post).not.toHaveBeenCalled()
})
it('has no timer or automatic submission in the new practice interface', async () => {
  window.history.replaceState({}, '', '/quiz/fixture-history'); const { container } = render(<App />)
  await screen.findByText('Fixture quiz')
  expect(screen.getByText('Untimed practice')).toBeVisible()
  expect(container.querySelector('.timer-box')).toBeNull()
  expect(axios.post).not.toHaveBeenCalled()
})
