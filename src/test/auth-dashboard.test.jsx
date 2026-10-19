import { render, screen } from '@testing-library/react'
import { beforeEach, expect, it } from 'vitest'
import App from '../App.jsx'
import { mockAPI } from './fixtures.js'

beforeEach(() => {
  mockAPI()
})

it('renders simplified navbar without palette selector and with login link', async () => {
  window.history.replaceState({}, '', '/')
  render(<App />)

  // Wait for page to finish lazy loading
  await screen.findByText(/Master the Rajasthan/i)
  const syllabusLinks = screen.getAllByRole('link', { name: /^Syllabus$/i })
  expect(syllabusLinks.length).toBeGreaterThanOrEqual(1)
  expect(syllabusLinks[0]).toBeVisible()

  const searchLinks = screen.getAllByRole('link', { name: /^Search$/i })
  expect(searchLinks.length).toBeGreaterThanOrEqual(1)

  const aboutLinks = screen.getAllByRole('link', { name: /^About/i })
  expect(aboutLinks.length).toBeGreaterThanOrEqual(1)
  expect(screen.getByRole('button', { name: /Switch to (dark|light) theme/i })).toBeVisible()
  expect(screen.getByRole('link', { name: /Sign in/i })).toBeVisible()

  // Ensure old palette dropdown is completely removed
  expect(screen.queryByLabelText(/Color palette/i)).toBeNull()
})

it('renders search page with typo suggestion and search tags', async () => {
  window.history.replaceState({}, '', '/search')
  render(<App />)

  expect(await screen.findByText(/Discoverable Knowledge Library/i)).toBeVisible()
  expect(screen.getByPlaceholderText(/Try 'Palaeolithic'/i)).toBeVisible()
  expect(screen.getByText(/Palaeolithic/i)).toBeVisible()
  expect(screen.getByText(/Kalibangan/i)).toBeVisible()
})

it('renders login page with username and password fields', async () => {
  window.history.replaceState({}, '', '/login')
  render(<App />)

  expect(await screen.findByRole('heading', { name: /Welcome back/i })).toBeVisible()
  expect(screen.getByLabelText(/Username/i)).toBeVisible()
  expect(screen.getByLabelText(/Password/i)).toBeVisible()
  expect(screen.getByRole('button', { name: /Sign in to Dashboard/i })).toBeVisible()
  expect(screen.getByRole('link', { name: /Create student account/i })).toBeVisible()
})

it('renders signup page with validation fields', async () => {
  window.history.replaceState({}, '', '/signup')
  render(<App />)

  expect(await screen.findByRole('heading', { name: /Create student account/i })).toBeVisible()
  expect(screen.getByLabelText(/Full name/i)).toBeVisible()
  expect(screen.getByLabelText(/Username \*/i)).toBeVisible()
  expect(screen.getByLabelText(/Password \*/i)).toBeVisible()
  expect(screen.getByRole('button', { name: /Create Account/i })).toBeVisible()
})

it('renders dashboard with sign-in prompt for guests', async () => {
  window.history.replaceState({}, '', '/dashboard')
  render(<App />)

  expect(await screen.findByText(/Sign in to see your learning progress/i)).toBeVisible()
  expect(screen.getByRole('link', { name: /Sign In →/i })).toBeVisible()
})
