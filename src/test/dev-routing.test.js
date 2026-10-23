import { afterEach, expect, it, vi } from 'vitest'
import { loadEnv } from 'vite'
import configuration from '../../vite.config.js'

vi.mock('vite', () => ({defineConfig: value => value, loadEnv: vi.fn()}))
vi.mock('@vitejs/plugin-react', () => ({default: () => ({name: 'react-test-fixture'})}))
afterEach(() => vi.unstubAllEnvs())

it('uses explicit local student routing even when an older development shell exports another API', () => {
  vi.stubEnv('PREPAL_API_ORIGIN', 'http://127.0.0.1:8000')
  loadEnv.mockReturnValue({PREPAL_DEV_API_ORIGIN: 'http://127.0.0.1:8002'})
  expect(configuration({mode: 'development'}).server.proxy['/api']).toBe('http://127.0.0.1:8002')
})

it('ignores development-only routing in production build/preview and respects explicit test backends', () => {
  vi.stubEnv('PREPAL_API_ORIGIN', 'http://127.0.0.1:8001')
  loadEnv.mockReturnValue({PREPAL_DEV_API_ORIGIN: 'http://127.0.0.1:8002'})
  const config = configuration({mode: 'production'})
  expect(config.server.proxy['/api']).toBe('http://127.0.0.1:8001')
  expect(config.preview.proxy['/api']).toBe('http://127.0.0.1:8001')
})
