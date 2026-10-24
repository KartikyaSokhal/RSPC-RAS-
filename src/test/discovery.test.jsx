import { render, screen, fireEvent, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Routes, Route } from 'react-router-dom'
import { expect, it } from 'vitest'
import axios from 'axios'
import ContentRenderer from '../components/study/ContentRenderer.jsx'
import TagPage from '../pages/tagPage.jsx'
import QuizPage from '../pages/quizPage.jsx'

const target = { id: 2, slug: 'rajasthan-history', title: 'Rajasthan History', description: 'Published evidence about historical sources.' }
const connection = { block_id: 11, node_index: 0, start: 0, end: 17, text: 'Rajasthan History', target }
function reader(html = '<p>Rajasthan History provides context.</p>', links = [connection]) {
  axios.get.mockResolvedValue({ data: links[0]?.target || target })
  return render(<ContentRenderer blocks={[{ id: 11, block_type: 'text', content: html }]} keywordLinks={links} />)
}

it('opens an accessible preview with a safe new-tab action and restores focus', async () => {
  const user = userEvent.setup(); reader()
  const trigger = screen.getByRole('link', { name: 'Rajasthan History' })
  const position = window.scrollY
  await user.click(trigger)
  const dialog = screen.getByRole('dialog', { name: target.title })
  expect(await within(dialog).findByText(target.description)).toBeVisible()
  const close = within(dialog).getByRole('button', { name: 'Close topic preview' })
  expect(close).toHaveFocus()
  const full = within(dialog).getByRole('link', { name: /Open Full Topic/ })
  expect(full).toHaveAttribute('href', '/topic/rajasthan-history')
  expect(full).toHaveAttribute('target', '_blank'); expect(full).toHaveAttribute('rel', 'noopener noreferrer')
  await user.tab(); expect(full).toHaveFocus()
  await user.tab(); expect(close).toHaveFocus()
  await user.tab({ shift: true }); expect(full).toHaveFocus()
  await user.keyboard('{Escape}')
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  expect(trigger).toHaveFocus(); expect(window.scrollY).toBe(position)
})

it('supports keyboard activation and outside dismissal', async () => {
  const user = userEvent.setup(); const { container } = reader()
  await user.tab(); await user.keyboard('{Enter}')
  expect(screen.getByRole('dialog')).toBeVisible()
  fireEvent.click(container.querySelector('.topic-popup-backdrop'))
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  expect(screen.getByRole('link', { name: target.title })).toHaveFocus()
})

it('fails closed on mismatched offsets, preserves Unicode and never annotates authored anchors', () => {
  const { container, unmount } = reader('<p>😀 Rajasthan History</p>', [{ ...connection, start: 3, end: 20 }])
  expect(container.querySelectorAll('.keyword-connection')).toHaveLength(1)
  unmount()
  const result = reader('<a href="https://example.org">Rajasthan History</a><p>Changed</p>')
  expect(result.container.querySelector('.keyword-connection')).toBeNull()
})

it('sanitizes scripts and forged popup controls and escapes preview metadata', async () => {
  const user = userEvent.setup()
  const { container } = reader('<p>Rajasthan History</p><script>window.pwned=1</script><a href="javascript:alert(1)" data-prepal-connection="0">Forged</a><svg onload="alert(1)"></svg>', [{ ...connection, target: { ...target, description: '<img src=x onerror=alert(1)>' } }])
  expect(container.querySelector('script,svg')).toBeNull()
  expect(screen.getByText('Forged')).not.toHaveAttribute('data-prepal-connection')
  await user.click(screen.getByRole('link', { name: target.title }))
  expect(await screen.findByText('<img src=x onerror=alert(1)>')).toBeVisible()
  expect(screen.getByRole('dialog').querySelector('img')).toBeNull()
})

function tags(data, failure) {
  axios.get.mockImplementation(() => failure ? Promise.reject(failure) : Promise.resolve({ data }))
  return render(<MemoryRouter initialEntries={['/tags/history']}><Routes><Route path="/tags/:slug" element={<TagPage />} /></Routes></MemoryRouter>)
}
it('shows approved tag articles, syllabus paths and estimated read times', async () => {
  tags({ tag: { name: 'History', slug: 'history' }, count: 1, page: 1, page_size: 30, results: [{ ...target, read_minutes: 2, syllabus_location: [{ title: 'Subject' }, { title: target.title }] }] })
  expect(await screen.findByRole('heading', { name: 'History', level: 1 })).toBeVisible()
  expect(screen.getByText('Subject › Rajasthan History')).toBeVisible()
  expect(screen.getByText('About 2 min read')).toBeVisible()
  expect(screen.getByRole('link', { name: /Subject ›/ })).toHaveAttribute('href', '/topic/rajasthan-history')
})
it('handles empty tags gracefully', async () => {
  tags({ tag: { name: 'History' }, count: 0, page: 1, page_size: 30, results: [] })
  expect(await screen.findByText('No published articles are available for this tag yet.')).toBeVisible()
})
it('handles unknown or withdrawn tags gracefully', async () => {
  tags(null, { response: { status: 404 } })
  expect(await screen.findByRole('heading', { name: 'This tag is not available.' })).toBeVisible()
})
it('checks dynamic practice statelessly through the collection endpoint', async () => {
  const user = userEvent.setup()
  const data = { id: 1, collection_id: 1, page: 1, count: 1, page_size: 50, title: 'Subject practice', revision_token: 'synthetic-token', questions: [{ id: 7, question_text: 'Which source?', choices: [{ id: 9, choice_text: 'Evidence' }, { id: 10, choice_text: 'Guess' }] }] }
  axios.get.mockImplementation(url => Promise.resolve({ data: url.includes('/config/') ? { csrf_token: 'synthetic-csrf' } : data }))
  axios.post.mockResolvedValue({ data: { collection_id: 1, score: 1, total: 1, percentage: 100, results: [{ question_id: 7, question_text: 'Which source?', user_answer: 9, correct_answer: 9, is_correct: true, explanation: 'Evidence supports the claim.' }] } })
  render(<MemoryRouter initialEntries={['/practice/subject']}><Routes><Route path="/practice/:slug" element={<QuizPage collection />} /></Routes></MemoryRouter>)
  await user.click(await screen.findByRole('radio', { name: /Evidence/ }))
  await user.click(screen.getByRole('button', { name: 'Check my answers →' }))
  expect(await screen.findByText('Evidence supports the claim.')).toBeVisible()
  expect(axios.post).toHaveBeenCalledWith('/api/topic/subject/practice/check/', { collection_id: 1, page: 1, revision_token: 'synthetic-token', answers: { 7: 9 } }, expect.any(Object))
  expect(screen.getByText('These results are held only in this page. No learner attempt has been saved.')).toBeVisible()
})

it('revalidates context and removes a link whose target was withdrawn', async () => {
  const user = userEvent.setup(); reader()
  axios.get.mockRejectedValue({ response: { status: 404 } })
  await user.click(screen.getByRole('link', { name: target.title }))
  expect(await screen.findByText('This topic preview is unavailable. Close this window to continue reading.')).toBeVisible()
  expect(screen.queryByRole('link', { name: /Open Full Topic/ })).not.toBeInTheDocument()
  expect(screen.queryByRole('link', { name: target.title })).not.toBeInTheDocument()
})
