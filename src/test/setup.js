import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/react'
import { afterEach, beforeEach, vi } from 'vitest'
import { resetClient } from '../api/client.js'

// Every request must be explicitly mocked; never reach Django or Gemini.
vi.mock('axios', () => ({ default: { get: vi.fn(), post: vi.fn() } }))
beforeEach(() => {
  resetClient()
  localStorage.clear()
  window.scrollTo = vi.fn()
  vi.stubGlobal('fetch', vi.fn(() => { throw new Error('Unexpected test network request') }))
  vi.spyOn(XMLHttpRequest.prototype, 'send').mockImplementation(() => {
    throw new Error('Unexpected test XMLHttpRequest')
  })
  Element.prototype.scrollIntoView = vi.fn() // jsdom has no layout.
})
afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})
