import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { expect, it } from 'vitest'
import { SyllabusContext } from '../components/study/syllabusContext.js'
import SyllabusPage from '../pages/syllabusPage.jsx'

function show(resource) {
  return render(<MemoryRouter><SyllabusContext.Provider value={{ loading: false, error: null, retry() {}, ...resource }}><SyllabusPage /></SyllabusContext.Provider></MemoryRouter>)
}

it('withholds invented totals during loading and failed hierarchy requests', () => {
  const view = show({ loading: true, data: null })
  const summary = within(screen.getByRole('region', { name: 'Syllabus topic summary' }))
  expect(summary.getAllByText('Loading…')).toHaveLength(3)
  expect(screen.getByRole('button', { name: 'All (Loading…)' })).toBeDisabled()
  view.unmount()
  show({ error: new Error('offline'), data: null })
  expect(within(screen.getByRole('region', { name: 'Syllabus topic summary' })).getAllByText('Unavailable')).toHaveLength(3)
  expect(screen.getByRole('button', { name: 'All (Unavailable)' })).toBeDisabled()
  expect(screen.queryByText(/152|10 Ready|five distinct streams/)).toBeNull()
})

it('retains genuine zero counts for an empty successful hierarchy', () => {
  show({ data: [] })
  const summary = within(screen.getByRole('region', { name: 'Syllabus topic summary' }))
  expect(summary.getByText('0 Ready')).toBeVisible()
  expect(summary.getByText('0 Streams')).toBeVisible()
  expect(screen.getByRole('button', { name: 'All (0)' })).toBeEnabled()
  expect(screen.getByRole('button', { name: /In preparation \(0\)/ })).toBeVisible()
})

it('counts the full hierarchy and zero ready notes independently of filtering', async () => {
  show({ data: [{ id: 1, title: 'Only subject', slug: 'only', children: [
    { id: 2, title: 'First lesson', slug: 'first', has_notes: false, children: [] },
    { id: 3, title: 'Second lesson', slug: 'second', has_notes: false, children: [] },
  ] }] })
  expect(screen.getByText('Explore 3 curriculum topics organized into 1 stream.', { exact: false })).toBeVisible()
  expect(screen.getByRole('button', { name: /Notes ready \(0\)/ })).toBeVisible()
  expect(screen.getByRole('button', { name: /In preparation \(3\)/ })).toBeVisible()
  await userEvent.type(screen.getByRole('searchbox', { name: 'Filter syllabus' }), 'First lesson')
  expect(screen.getByRole('button', { name: 'All (3)' })).toBeVisible()
})
