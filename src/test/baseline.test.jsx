import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it } from 'vitest'
import axios from 'axios'
import App from '../App.jsx'
import { mockAPI, topic } from './fixtures.js'

beforeEach(() => { window.history.replaceState({}, '', '/'); mockAPI() })
describe('published learning flow', () => {
  it('navigates from catalog to topic and renders authored HTML', async () => {
    const user = userEvent.setup(); render(<App />)
    await user.click(await screen.findByText('Fixture History'))
    expect(await screen.findByText('Curated fixture notes.')).toBeVisible()
    expect(window.location.pathname).toBe('/topic/fixture-history')
    expect(screen.getByRole('link', { name: 'Practice this lesson →' })).toBeVisible()
  })
  it('shows an honest empty lesson', async () => {
    mockAPI({ lesson: { ...topic, blocks: [] } }); window.history.replaceState({}, '', '/topic/fixture-history'); render(<App />)
    expect(await screen.findByText('No learning material has been published for this lesson yet.')).toBeVisible()
  })
  it('shows unavailable topic without exposing internal errors', async () => {
    window.history.replaceState({}, '', '/topic/missing'); render(<App />)
    expect(await screen.findByRole('heading', { name: 'This lesson is not available.' })).toBeVisible()
  })
  it('sends bounded topic-scoped chat to a mock with CSRF', async () => {
    const user = userEvent.setup(); window.history.replaceState({}, '', '/topic/fixture-history'); render(<App />)
    await screen.findByText('Curated fixture notes.')
    await user.click(screen.getByRole('button', { name: 'Ask AI Tutor' }))
    await user.type(screen.getByRole('textbox', { name: 'Ask the tutor' }), 'Explain these notes')
    await user.click(screen.getByRole('button', { name: 'Send question' }))
    expect(await screen.findByText('Mocked tutor explanation.')).toBeVisible()
    expect(axios.post).toHaveBeenCalledWith('/api/topic/fixture-history/chat/', { message: 'Explain these notes', history: [], allow_related: false }, expect.objectContaining({ headers: { 'X-CSRFToken': 'fixture-csrf' } }))
  })
  it('escapes typed messages instead of rendering markup', async () => {
    const user = userEvent.setup(); window.history.replaceState({}, '', '/topic/fixture-history'); render(<App />)
    await screen.findByText('Curated fixture notes.'); const text = '<img src=x onerror=alert(1)>'
    await user.click(screen.getByRole('button', { name: 'Ask AI Tutor' }))
    await user.type(screen.getByRole('textbox', { name: 'Ask the tutor' }), text)
    await user.click(screen.getByRole('button', { name: 'Send question' }))
    expect(await screen.findByText(text)).toBeVisible(); expect(document.querySelector('.chat-msg-user img')).toBeNull()
  })
  it('checks stateless answers, shows explanations and retries', async () => {
    const user = userEvent.setup(); window.history.replaceState({}, '', '/quiz/fixture-history'); render(<App />)
    await user.click(await screen.findByRole('radio', { name: /Correct fixture/ }))
    await user.click(screen.getByRole('button', { name: 'Check my answers →' }))
    expect(await screen.findByText('The source supports this fixture.')).toBeVisible()
    expect(axios.post).toHaveBeenCalledWith('/api/topic/fixture-history/quiz/check/', { quiz_id: 7, revision_token: 'fixture-signed-token', answers: { 11: 21 } }, expect.any(Object))
    await user.click(screen.getByRole('button', { name: 'Try again ↻' }))
    expect(await screen.findByRole('radio', { name: /Correct fixture/ })).not.toBeChecked()
  })
  it('keeps entered answers after a failed check', async () => {
    const user = userEvent.setup(); axios.post.mockRejectedValue(new Error('private diagnostic'))
    window.history.replaceState({}, '', '/quiz/fixture-history'); render(<App />)
    await user.click(await screen.findByRole('radio', { name: /Correct fixture/ }))
    await user.click(screen.getByRole('button', { name: 'Check my answers →' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('They are still here')
    expect(screen.getByRole('radio', { name: /Correct fixture/ })).toBeChecked()
    expect(screen.queryByText('private diagnostic')).toBeNull()
  })
})
