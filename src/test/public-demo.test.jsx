import { expect, it, vi } from 'vitest'
import { useState } from 'react'
import { act, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes, useLocation } from 'react-router-dom'
import axios from 'axios'
import App from '../App.jsx'
import LearningRoute from '../components/auth/LearningRoute.jsx'
import { returnLocation } from '../components/auth/returnLocation.js'
import { PlatformContext } from '../components/layout/platformContext.js'
import { AuthContext } from '../context/authContextDef.js'
import AuthProvider from '../context/AuthContext.jsx'
import useAuth from '../hooks/useAuth.js'
import LoginPage from '../pages/loginPage.jsx'
import { get } from '../api/client.js'

const policy = { learning_auth_required: true, student_features_enabled: true, registration_enabled: false, password_reset_enabled: false, ai_enabled: false, demo: true, public_summary: { subjects: 5, topics: 142 } }

function guest() {
  axios.get.mockImplementation(url => url === '/api/config/' ? Promise.resolve({ data: policy }) : Promise.reject(new Error('Guest content request forbidden: '+url)))
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => ({ authenticated: false, user: null }) })))
}

it('loads a public homepage with aggregate counts and no syllabus or notes request', async () => {
  guest(); window.history.replaceState({}, '', '/')
  render(<App />)
  expect(await screen.findByRole('heading', { name: 'Sign in to explore the syllabus' })).toBeVisible()
  expect(screen.getByText('5 Subjects · 142 Curriculum Topics')).toBeVisible()
  expect(await within(screen.getByRole('banner')).findByRole('link', {name: 'Sign In'})).toBeVisible()
  expect(axios.get.mock.calls.every(([url]) => url === '/api/config/')).toBe(true)
})

it('keeps signup public without accepting personal data or issuing protected requests', async () => {
  guest(); window.history.replaceState({}, '', '/signup')
  render(<App />)
  expect(await screen.findByRole('heading', { name: 'Student registration is not available' })).toBeVisible()
  expect(screen.queryByRole('textbox')).not.toBeInTheDocument()
  expect(axios.get.mock.calls.every(([url]) => url === '/api/config/')).toBe(true)
})

it.each(['/syllabus', '/topic/a-temples', '/practice/history', '/quiz/a-temples', '/tags/history', '/resources/1', '/search?q=temple', '/dashboard', '/planner', '/attempts/1'])('redirects guest %s to friendly Sign In before fetching content', async path => {
  guest(); window.history.replaceState({}, '', path)
  render(<App />)
  expect(await screen.findByRole('heading', { name: 'Welcome back' })).toBeVisible()
  expect(window.location.pathname).toBe('/login')
  expect(axios.get.mock.calls.every(([url]) => url === '/api/config/')).toBe(true)
})

function Location() { const location = useLocation(); return <h1>{location.pathname+location.search+location.hash}</h1> }
function Account({ children }) {
  const [authenticated, setAuthenticated] = useState(false)
  return <AuthContext.Provider value={{ loading: false, authenticated, login: async () => { setAuthenticated(true) } }}>{children}</AuthContext.Provider>
}

it('returns login to the requested path including query and reading anchor', async () => {
  render(<MemoryRouter initialEntries={['/topic/a-temples?view=notes#block-1']}><PlatformContext.Provider value={policy}><Account><Routes>
    <Route path="/topic/:slug" element={<LearningRoute><Location /></LearningRoute>} />
    <Route path="/login" element={<LoginPage />} />
    <Route path="*" element={<Location />} />
  </Routes></Account></PlatformContext.Provider></MemoryRouter>)
  const user = userEvent.setup()
  await user.type(await screen.findByLabelText('Username'), 'demo-reader')
  await user.type(screen.getByLabelText('Password'), 'synthetic-unused')
  await user.click(screen.getByRole('button', {name: /Sign in to Dashboard/}))
  expect(await screen.findByRole('heading', {name: '/topic/a-temples?view=notes#block-1'})).toBeVisible()
})

it.each(['//evil.example', '/\\evil.example', '/login', '/signup?next=/syllabus', 'https://evil.example', '/reset-password#token=x'])('rejects unsafe or looping return path %s', pathname => {
  expect(returnLocation({pathname})).toBe('/dashboard')
})

it('revokes protected UI when a content request reports an expired session', async () => {
  vi.stubGlobal('fetch', vi.fn(async () => ({ok: true, json: async () => ({ authenticated: true, user: {id: 1} })})))
  render(<MemoryRouter initialEntries={['/syllabus']}><PlatformContext.Provider value={policy}><AuthProvider enabled><Routes>
    <Route path="/syllabus" element={<LearningRoute><h1>Private syllabus</h1></LearningRoute>} />
    <Route path="/login" element={<h1>Sign in again</h1>} />
  </Routes></AuthProvider></PlatformContext.Provider></MemoryRouter>)
  expect(await screen.findByRole('heading', {name: 'Private syllabus'})).toBeVisible()
  axios.get.mockRejectedValue({response: {status: 401, data: {error: {code: 'auth_required'}}}})
  await act(async () => { await get('/topics/').catch(() => {}) })
  await waitFor(() => expect(screen.getByRole('heading', {name: 'Sign in again'})).toBeVisible())
  expect(screen.queryByText('Private syllabus')).not.toBeInTheDocument()
})

function SessionStatus() {
  const { authenticated, logout } = useAuth()
  return <><p>{authenticated ? 'Signed in' : 'Signed out'}</p><button onClick={logout}>Logout</button></>
}

it('does not restore a logged-out session when an earlier status request finishes late', async () => {
  let finishStatus
  const pending = new Promise(resolve => { finishStatus = resolve })
  const response = () => ({ok:true, json:async () => ({authenticated:true,user:{id:1}})})
  const fetch = vi.fn().mockResolvedValueOnce(response()).mockReturnValueOnce(pending).mockResolvedValue({ok:true})
  vi.stubGlobal('fetch', fetch)
  document.cookie = 'csrftoken=synthetic-test-csrf'
  render(<AuthProvider enabled><SessionStatus /></AuthProvider>)
  expect(await screen.findByText('Signed in')).toBeVisible()
  act(() => window.dispatchEvent(new Event('focus')))
  await userEvent.setup().click(screen.getByRole('button', {name:'Logout'}))
  expect(await screen.findByText('Signed out')).toBeVisible()
  await act(async () => { finishStatus(response()) })
  expect(screen.getByText('Signed out')).toBeVisible()
})
