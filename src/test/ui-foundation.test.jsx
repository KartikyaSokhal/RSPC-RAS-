import { render, screen, within, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { beforeEach, expect, it } from 'vitest'
import axios from 'axios'
import App from '../App.jsx'
import SyllabusTree from '../components/study/SyllabusTree.jsx'
import { mockAPI, topic } from './fixtures.js'
import { uiHierarchy } from './uiHierarchy.js'

beforeEach(() => { window.history.replaceState({}, '', '/'); mockAPI() })
function hierarchyAPI() {
  const fallback = axios.get.getMockImplementation()
  axios.get.mockImplementation((url, ...args) => url.includes('/topics/')
    ? Promise.resolve({ data: uiHierarchy }) : fallback(url, ...args))
}

it('keeps Search and working themes in the header, with existing search routing', async () => {
  const user = userEvent.setup(); render(<App />)
  const header = within(await screen.findByRole('banner'))
  expect(header.getByRole('link', { name: 'Prepal home' })).toHaveAttribute('href', '/')
  expect(header.queryByRole('link', { name: /Syllabus|About|Sign In|Sign Up/i })).toBeNull()
  await user.click(header.getByRole('button', { name: 'Switch to dark theme' }))
  expect(document.documentElement).toHaveAttribute('data-theme', 'dark')
  await user.click(header.getByRole('button', { name: 'Switch to light theme' }))
  expect(document.documentElement).toHaveAttribute('data-theme', 'light')
  await user.click(header.getByRole('link', { name: 'Search' }))
  expect(await screen.findByRole('searchbox', { name: /Search syllabus topics/ })).toBeVisible()
  expect(window.location.pathname).toBe('/search')
})

it('uses one hierarchy response for honest homepage/footer counts and all subject buttons', async () => {
  hierarchyAPI(); render(<App />)
  const subjects = await screen.findByRole('navigation', { name: 'Jump to a subject' })
  expect(within(subjects).getAllByRole('button')).toHaveLength(5)
  const stats = screen.getByRole('region', { name: 'Curriculum Overview Statistics' })
  expect(stats).toHaveTextContent('Total Curriculum Topics:14')
  expect(stats).toHaveTextContent('Core Subjects:5')
  expect(screen.getByLabelText('Syllabus statistics')).toHaveTextContent('5 Subjects · 14 Curriculum Topics')
  expect(screen.getByRole('contentinfo')).toHaveTextContent('Prepal Academic Syllabus')
  expect(screen.queryByText('Verified Notes Ready:')).toBeNull()
  expect(screen.queryByRole('searchbox')).toBeNull()
  expect(screen.queryByRole('link', { name: /Search Topics|About & Methodology/ })).toBeNull()
  expect(screen.getByRole('link', { name: /Explore Syllabus/ })).toHaveAttribute('href', '#syllabus-explorer')
  expect(axios.get.mock.calls.filter(([url]) => url.includes('/topics/'))).toHaveLength(1)
})

it('subject navigation scrolls and focuses the matching original root without filtering others', async () => {
  hierarchyAPI(); const user = userEvent.setup(); render(<App />)
  await user.click(await screen.findByRole('button', { name: '5. Fifth subject' }))
  const root = document.getElementById('home-subject-5')
  expect(root.querySelector('summary')).toHaveFocus()
  expect(root.scrollIntoView).toHaveBeenCalledWith({ block: 'start' })
  expect(document.querySelectorAll('.syllabus-tree > details')).toHaveLength(5)
  expect(window.location.pathname).toBe('/')
})

it('does not invent counts while the hierarchy is loading', async () => {
  const fallback = axios.get.getMockImplementation()
  axios.get.mockImplementation((url, ...args) => url.includes('/topics/') ? new Promise(() => {}) : fallback(url, ...args))
  render(<App />)
  expect(await screen.findByLabelText('Syllabus statistics')).toHaveTextContent('Loading syllabus statistics')
  expect(screen.getByRole('region', { name: 'Curriculum Overview Statistics' })).not.toHaveTextContent('152')
})

it('reports hierarchy failure without false counts and refreshes homepage and footer together', async () => {
  const fallback = axios.get.getMockImplementation()
  axios.get.mockImplementation((url, ...args) => url.includes('/topics/')
    ? Promise.reject(new Error('unavailable')) : fallback(url, ...args))
  const user = userEvent.setup(); render(<App />)
  await screen.findByRole('heading', { name: 'Syllabus directory is temporarily unreachable' })
  expect(screen.getByLabelText('Syllabus statistics')).toHaveTextContent('temporarily unavailable')
  expect(screen.getByLabelText('Syllabus statistics')).not.toHaveTextContent(/0 Subjects|152/)
  hierarchyAPI()
  await user.click(screen.getByRole('button', { name: /Try again/i }))
  expect(await screen.findByText('5 Subjects · 14 Curriculum Topics')).toBeVisible()
})

it('fully expands/collapses the hierarchy and allows individual toggles after both actions', async () => {
  const user = userEvent.setup()
  const { container } = render(<MemoryRouter><SyllabusTree topics={uiHierarchy} showControls /></MemoryRouter>)
  await user.click(screen.getByRole('button', { name: 'Expand All' }))
  expect([...container.querySelectorAll('details')].every(node => node.open)).toBe(true)
  expect(screen.getByRole('link', { name: /Nested concept/ })).toBeVisible()
  const firstRoot = container.querySelector('summary')
  await user.click(firstRoot)
  expect(firstRoot.parentElement.open).toBe(false)
  await user.click(screen.getByRole('button', { name: 'Collapse All' }))
  expect([...container.querySelectorAll('details')].every(node => !node.open)).toBe(true)
  expect(screen.getByRole('link', { name: /Nested concept/ })).not.toBeVisible()
  expect([...container.querySelectorAll('.depth-0 > summary')]).toHaveLength(5)
  await user.click(firstRoot)
  expect(firstRoot.parentElement.open).toBe(true)
  expect(screen.queryByRole('button', { name: /Default View/i })).toBeNull()
})

it('preserves root, child and restarting alphabetic numbers across filtered trees', async () => {
  const user = userEvent.setup()
  const filtered = [{ ...uiHierarchy[0], children: [{ ...uiHierarchy[0].children[1], children: [uiHierarchy[0].children[1].children[1]] }] }, uiHierarchy[4]]
  const { container } = render(<MemoryRouter><SyllabusTree topics={filtered} originalTopics={uiHierarchy} showControls /></MemoryRouter>)
  await user.click(screen.getByRole('button', { name: 'Expand All' }))
  const numbers = [...container.querySelectorAll('.tree-number')].map(node => node.textContent)
  expect(numbers).toEqual(['1', '1.2', 'B', 'A', '5', '5.1'])
  expect(screen.getByRole('link', { name: /Nested concept/ })).toHaveAttribute('href', '/topic/ui-1221')
})

it('keeps one Tutor launcher and restores keyboard focus on Escape and Close', async () => {
  window.history.replaceState({}, '', '/topic/fixture-history')
  const user = userEvent.setup(); render(<App />)
  await screen.findByText('Curated fixture notes.')
  expect(document.querySelectorAll('.floating-tutor-launcher')).toHaveLength(1)
  expect(document.querySelector('.toolbar-tutor-btn')).toBeNull()
  expect(within(screen.getByRole('group', { name: 'Study panels' })).queryByRole('button', { name: /Tutor/i })).toBeNull()
  const launcher = screen.getByRole('button', { name: 'Ask AI Tutor' })
  await user.click(launcher)
  const close = within(screen.getByRole('dialog', { name: 'AI Study Assistant' })).getByRole('button', { name: 'Close AI Assistant' })
  expect(close).toHaveFocus()
  await user.keyboard('{Escape}')
  expect(screen.queryByRole('dialog')).toBeNull(); expect(launcher).toHaveFocus()
  await user.keyboard('{Enter}')
  await user.click(screen.getByRole('button', { name: 'Close AI Assistant' }))
  expect(launcher).toHaveFocus()
  expect(axios.post).not.toHaveBeenCalled()
})

it('reader sidebar filtering preserves original numbering and the current topic route', async () => {
  hierarchyAPI()
  window.history.replaceState({}, '', '/topic/fixture-history')
  const user = userEvent.setup(); render(<App />)
  await screen.findByText('Curated fixture notes.')
  await user.type(screen.getByRole('searchbox', { name: 'Filter sidebar syllabus' }), 'Fifth subject unit')
  await waitFor(() => expect(document.querySelectorAll('.study-sidebar .tree-number')).toHaveLength(2))
  expect([...document.querySelectorAll('.study-sidebar .tree-number')].map(n => n.textContent)).toEqual(['5', '5.1'])
  expect(window.location.pathname).toBe(`/topic/${topic.slug}`)
})
