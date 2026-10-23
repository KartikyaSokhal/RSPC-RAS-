import { beforeEach, expect, it, vi } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Routes, Route } from 'react-router-dom'
import axios from 'axios'
import { AuthContext } from '../context/authContextDef.js'
import { AuthProvider } from '../context/AuthContext.jsx'
import LoginPage from '../pages/loginPage.jsx'
import DashboardPage from '../pages/dashboardPage.jsx'
import TopicPage from '../pages/topicPage.jsx'
import AttemptPage from '../pages/attemptPage.jsx'
import PlannerPage from '../pages/plannerPage.jsx'
import ResetPasswordPage from '../pages/resetPasswordPage.jsx'
import { SyllabusContext } from '../components/study/syllabusContext.js'
import { topic, mockAPI } from './fixtures.js'

beforeEach(() => { mockAPI(); document.cookie = 'csrftoken=synthetic-csrf' })
const account = { featuresEnabled: true, authenticated: true, loading: false, user: {name: 'Reader'}, logout: vi.fn() }
function wrap(ui) { return render(<MemoryRouter><AuthContext.Provider value={account}>{ui}</AuthContext.Provider></MemoryRouter>) }

it('signs in using a CSRF-protected session without browser token storage', async () => {
  const fetch = vi.fn(async url => ({ok: true, json: async () => url.endsWith('status/') ? {authenticated: false, user: null} : {authenticated: true, user: {id: 1, name: 'Reader'}}}))
  vi.stubGlobal('fetch', fetch)
  render(<MemoryRouter><AuthProvider enabled><LoginPage /></AuthProvider></MemoryRouter>)
  const user = userEvent.setup()
  await user.type(screen.getByLabelText('Username'), 'reader')
  await user.type(screen.getByLabelText('Password'), 'synthetic-password')
  await user.click(screen.getByRole('button', {name: /Sign in to Dashboard/}))
  expect(fetch).toHaveBeenCalledWith('/api/auth/login/', expect.objectContaining({credentials: 'same-origin', method: 'POST', headers: expect.objectContaining({'X-CSRFToken': 'synthetic-csrf'})}))
  expect(localStorage.length).toBe(0)
})

it('shows real zero totals and empty states on a new account without invented syllabus counts', async () => {
  axios.get.mockResolvedValue({data: {stats: {total_topics: 0, total_completed: 0, total_bookmarks: 0, total_quizzes_taken: 0, average_quiz_accuracy: null}, subject_progress: [], recent_activity: [], quiz_attempts: [], bookmarks: [], completed_topics: [], suggested_next: []}})
  wrap(<DashboardPage />)
  const overview = await screen.findByRole('region', {name: 'Learning Progress Overview'})
  expect(overview).toHaveTextContent('/ 0')
  expect(overview).not.toHaveTextContent('152')
  expect(await screen.findByText('No bookmarks saved yet.')).toBeVisible()
  expect(screen.getByText('No quiz attempts yet.')).toBeVisible()
})

it('records an explicit visit and changes owned controls only after successful responses', async () => {
  const lesson = {...topic, is_published: true, is_learning_unit: true, is_bookmarked: false, is_completed: false}
  mockAPI({lesson})
  axios.post.mockImplementation(async (url, payload) => ({data: url.endsWith('bookmark/') ? {is_bookmarked: payload.is_bookmarked} : url.endsWith('progress/') ? {is_completed: payload.is_completed} : {visited: true}}))
  render(<MemoryRouter initialEntries={['/topic/fixture-history']}><AuthContext.Provider value={account}><SyllabusContext.Provider value={{data: [lesson], retry: vi.fn()}}><Routes><Route path="topic/:slug" element={<TopicPage />} /></Routes></SyllabusContext.Provider></AuthContext.Provider></MemoryRouter>)
  const user = userEvent.setup()
  await user.click(await screen.findByRole('button', {name: /Bookmark Topic/}))
  expect(await screen.findByRole('button', {name: /Remove Bookmark/})).toHaveAttribute('aria-pressed', 'true')
  await user.click(screen.getByRole('button', {name: /Mark as Completed/}))
  expect(await screen.findByRole('button', {name: /Mark as Incomplete/})).toHaveAttribute('aria-pressed', 'true')
  expect(axios.post).toHaveBeenCalledWith('/api/topic/fixture-history/visit/', {}, expect.anything())
  expect(within(screen.getByRole('article')).getByRole('status')).toHaveTextContent('Lesson completed.')
})

it('renders saved explanations as text and reports inaccessible attempts without exposing another record', async () => {
  axios.get.mockResolvedValue({data: {score: 0, total: 1, attempted_at: '2026-10-23T00:00:00Z', history_available: true,
    snapshot: {title: 'Historical practice', kind: 'quiz', source_slug: 'fixture-history', questions: [{question_id: 1, question_text: '<img src=x onerror=alert(1)>', explanation: '<script>unsafe()</script>', choices: [], subject_title: 'History', topic_title: 'Lesson'}]}}})
  render(<MemoryRouter initialEntries={['/attempts/1']}><AuthContext.Provider value={account}><Routes><Route path="attempts/:id" element={<AttemptPage />} /></Routes></AuthContext.Provider></MemoryRouter>)
  expect(await screen.findByText('<script>unsafe()</script>')).toBeVisible()
  expect(document.querySelector('script, img')).toBeNull()
  expect(screen.getByRole('link', {name: 'Reattempt current reviewed practice'})).toHaveAttribute('href', '/quiz/fixture-history')
})

it('keeps planner inputs intact when scheduling validation fails', async () => {
  axios.get.mockResolvedValue({data: []})
  axios.post.mockRejectedValue({response: {status: 400, data: {error: {message: 'The exam target cannot precede the start date.'}}}})
  render(<MemoryRouter><AuthContext.Provider value={account}><SyllabusContext.Provider value={{data: [{id: 1, title: 'Published history', is_published: true}], retry: vi.fn()}}><PlannerPage /></SyllabusContext.Provider></AuthContext.Provider></MemoryRouter>)
  const user = userEvent.setup()
  await user.click(screen.getByRole('checkbox', {name: 'Published history'}))
  await user.clear(screen.getByLabelText('Plan title'))
  await user.type(screen.getByLabelText('Plan title'), 'My retained plan')
  await user.click(screen.getByRole('button', {name: 'Generate study plan'}))
  expect(await screen.findByRole('alert')).toHaveTextContent('The exam target cannot precede the start date.')
  expect(screen.getByLabelText('Plan title')).toHaveValue('My retained plan')
  expect(screen.getByRole('checkbox', {name: 'Published history'})).toBeChecked()
})

it('clears the recovery fragment and refreshes session state before returning to sign in', async () => {
  window.history.replaceState({}, '', '/reset-password#uid=synthetic&token=synthetic-token')
  const refreshStatus = vi.fn().mockResolvedValue(undefined)
  axios.post.mockResolvedValue({data: {message: 'Password changed.'}})
  render(<MemoryRouter initialEntries={['/reset-password']}><AuthContext.Provider value={{...account, refreshStatus}}><Routes>
    <Route path="/reset-password" element={<ResetPasswordPage />} /><Route path="/login" element={<LoginPage />} />
  </Routes></AuthContext.Provider></MemoryRouter>)
  expect(window.location.hash).toBe('')
  const user = userEvent.setup()
  await user.type(screen.getByLabelText('New password'), 'New-Synthetic-Password-423!')
  await user.click(screen.getByRole('button', {name: 'Change password'}))
  expect(await screen.findByRole('status')).toHaveTextContent('Password changed. Sign in with your new password.')
  expect(refreshStatus).toHaveBeenCalledOnce()
  window.history.replaceState({}, '', '/')
})
