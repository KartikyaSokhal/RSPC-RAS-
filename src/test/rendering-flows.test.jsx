import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, expect, it } from 'vitest'
import axios from 'axios'
import App from '../App.jsx'
import { mockAPI, topic } from './fixtures.js'
const response = '## Safe explanation\n\n**Key fact**\n\n| Year | Event |\n| --- | --- |\n| 1947 | Independence |\n\n<img src=x onerror="alert(1)">\n\n[Unsafe](javascript:alert%281%29)'
beforeEach(() => {
  window.history.replaceState({}, '', '/topic/fixture-history')
  mockAPI({ lesson: { ...topic, blocks: [{ id: 11, block_type: 'text', content: '<h2>Authored lesson</h2><p>Keep <strong>this fact</strong>.</p><img src=x onerror="alert(1)"><script>alert(1)</script>' }] }, chat: { response, citations: [] } })
})
it('preserves safe notes and strips executable markup in the reader', async () => {
  const { container } = render(<App />)
  expect(await screen.findByRole('heading', { name: 'Authored lesson' })).toBeVisible()
  expect(screen.getByText('this fact').tagName).toBe('STRONG')
  expect(container.querySelector('.block-text script')).toBeNull(); expect(container.querySelector('.block-text img')).not.toHaveAttribute('onerror')
})
it('renders chatbot Markdown tables without interpreting raw HTML', async () => {
  const user = userEvent.setup(); const { container } = render(<App />)
  await screen.findByRole('heading', { name: 'Authored lesson' })
  await user.click(screen.getByRole('button', { name: 'Ask AI Tutor' }))
  await user.type(screen.getByRole('textbox', { name: 'Ask the tutor' }), 'Explain')
  await user.click(screen.getByRole('button', { name: 'Send question' }))
  expect(await screen.findByRole('heading', { name: 'Safe explanation' })).toBeVisible()
  expect(screen.getByRole('table')).toHaveTextContent('Independence')
  expect(container.querySelector('.chat-msg-bot img,.chat-msg-bot script')).toBeNull(); expect(screen.getByText('Unsafe')).not.toHaveAttribute('href')
})
it('keeps weakness reporting out of the reader without loading shared history', async () => {
  render(<App />); await screen.findByRole('heading', { name: 'Authored lesson' })
  expect(screen.queryByRole('button', { name: /Revision Room/ })).toBeNull()
  expect(axios.get.mock.calls.some(([url]) => url.includes('/profile/weaknesses/'))).toBe(false)
})
