import { render, screen } from '@testing-library/react'
import { expect, it, vi } from 'vitest'

vi.mock('dompurify', () => ({ default: () => ({ isSupported: false }) }))
import SafeHtml from './SafeHtml.jsx'

it('falls back to escaped text when DOMPurify cannot sanitize the environment', () => {
  const payload = '<img src=x onerror="alert(1)"><script>alert(1)</script>'
  const { container } = render(<SafeHtml html={payload} />)
  expect(screen.getByText(payload)).toBeVisible()
  expect(container.querySelector('img, script')).toBeNull()
})
