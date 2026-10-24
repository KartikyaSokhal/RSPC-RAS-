import { defineConfig, devices } from '@playwright/test'
import { isAbsolute, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const demoRoot = process.env.PREPAL_DEMO_ROOT
const existingDemo = fileURLToPath(new URL('./.local/demo', import.meta.url))
if (!demoRoot || !isAbsolute(demoRoot) || resolve(demoRoot) === resolve(existingDemo)) {
  throw new Error('Set PREPAL_DEMO_ROOT to a separate absolute synthetic test-demo directory. The existing .local/demo is excluded.')
}

export default defineConfig({
  testDir: './e2e-integration', workers: 1, retries: 0, reporter: 'list', timeout: 60000,
  use: { baseURL: 'http://127.0.0.1:4175', trace: 'retain-on-failure' },
  projects: [{ name: 'chromium-integration', use: { ...devices['Desktop Chrome'] } }],
  webServer: [
    { command: 'backend/.venv/bin/python backend/manage.py runserver 127.0.0.1:8001 --settings=core.demo_settings --noreload', url: 'http://127.0.0.1:8001/api/config/', reuseExistingServer: false },
    { command: 'npm run build && npm run preview -- --host 127.0.0.1 --port 4175 --strictPort', env: { PREPAL_API_ORIGIN: 'http://127.0.0.1:8001' }, url: 'http://127.0.0.1:4175', reuseExistingServer: false },
  ],
})
