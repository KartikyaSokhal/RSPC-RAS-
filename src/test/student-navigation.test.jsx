import { beforeEach, expect, it, vi } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import axios from 'axios'
import App from '../App.jsx'
import { config, mockAPI } from './fixtures.js'

beforeEach(() => { window.history.replaceState({}, '', '/'); mockAPI() })

function studentAPI(authenticated = false) {
  const fallback = axios.get.getMockImplementation()
  axios.get.mockImplementation((url, ...args) => url.endsWith('/config/')
    ? Promise.resolve({data: {...config, student_features_enabled: true, google_signin_enabled: false}})
    : fallback(url, ...args))
  vi.stubGlobal('fetch', vi.fn(async url => {
    if (url.endsWith('/auth/logout/')) authenticated = false
    return {ok: true, json: async () => ({authenticated, user: authenticated ? {id: 1, name: 'Student reader'} : null})}
  }))
}

it('exposes existing sign-in/up routes only after the server enables students, in navbar order', async () => {
  studentAPI(); render(<App />)
  const user = userEvent.setup()
  const header = within(await screen.findByRole('banner'))
  const signin = await header.findByRole('link', {name: 'Sign In'})
  expect(signin).toHaveAttribute('href', '/login')
  expect(header.getByRole('link', {name: 'Sign Up'})).toHaveAttribute('href', '/signup')
  const controls = document.querySelector('.header-controls')
  expect([...controls.children].map(node => node.textContent.trim())).toEqual(['Search ⌕', '', 'Sign In', 'Sign Up'])
  await user.click(signin)
  expect(await screen.findByRole('heading', {name: 'Welcome back'})).toBeVisible()
  expect(screen.getByRole('button', {name: 'Continue with Google'})).toBeDisabled()
  await user.click(header.getByRole('link', {name: 'Sign Up'}))
  expect(await screen.findByRole('button', {name: 'Create Account & Start Learning →'})).toBeVisible()
})

it('shows the persisted session account menu and clears it only after successful logout', async () => {
  studentAPI(true); render(<App />)
  const user = userEvent.setup(); const header = within(await screen.findByRole('banner'))
  expect(await header.findByRole('link', {name: 'Dashboard'})).toHaveAttribute('href', '/dashboard')
  expect(header.queryByRole('link', {name: 'Sign In'})).toBeNull()
  const menu = screen.getByLabelText('Account menu')
  await user.click(menu)
  expect(header.getByRole('button', {name: 'Logout'})).toBeVisible()
  await user.click(header.getByRole('button', {name: 'Logout'}))
  expect(await header.findByRole('link', {name: 'Sign In'})).toBeVisible()
  expect(header.queryByRole('link', {name: 'Dashboard'})).toBeNull()
})
