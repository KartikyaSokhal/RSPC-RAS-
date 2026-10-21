import { render, screen } from '@testing-library/react'
import { beforeEach, expect, it } from 'vitest'
import axios from 'axios'
import App from '../App.jsx'
import { mockAPI } from './fixtures.js'

beforeEach(() => { mockAPI() })

it('keeps header search and theme controls without student navigation or status probes', async () => {
  window.history.replaceState({}, '', '/')
  render(<App />)
  await screen.findByText(/Master the Rajasthan/i)
  const header = screen.getByRole('banner')
  expect(header.querySelector('a[href="/search"]')).toBeVisible()
  expect(header.querySelector('a[href="/syllabus"],a[href="/about"]')).toBeNull()
  expect(screen.getByRole('button', { name: /Switch to (dark|light) theme/i })).toBeVisible()
  expect(screen.queryByRole('link', { name: /Sign in|Sign up|Dashboard/i })).toBeNull()
  expect(fetch).not.toHaveBeenCalled()
  expect(axios.get.mock.calls.some(([url]) => /auth|dashboard|bookmarks|progress/.test(url))).toBe(false)
})

it('preserves the search interface', async () => {
  window.history.replaceState({}, '', '/search')
  render(<App />)
  expect(await screen.findByText(/Discoverable Knowledge Library/i)).toBeVisible()
  expect(screen.getByPlaceholderText(/Try 'Palaeolithic'/i)).toBeVisible()
})

for (const route of ['/login', '/signup', '/dashboard']) {
  it(`explains the release boundary at ${route} without mounting student forms or fetching records`, async () => {
    window.history.replaceState({}, '', route)
    render(<App />)
    expect(await screen.findByRole('heading', { name: 'Personalized features are unavailable.' })).toBeVisible()
    expect(screen.getByText(/Student accounts, bookmarks, completion tracking/)).toBeVisible()
    expect(screen.queryByLabelText(/Password|Username/i)).toBeNull()
    expect(screen.getByRole('link', { name: 'Browse the syllabus' })).toBeVisible()
    expect(fetch).not.toHaveBeenCalled()
    expect(axios.get.mock.calls.some(([url]) => /auth|dashboard|bookmarks|progress/.test(url))).toBe(false)
  })
}
