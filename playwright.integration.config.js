import { defineConfig, devices } from '@playwright/test'
export default defineConfig({
  testDir: './e2e-integration', workers: 1, retries: 0, reporter: 'list', timeout: 60000,
  use: { baseURL: 'http://127.0.0.1:4175', trace: 'retain-on-failure' },
  projects: [{ name: 'chromium-integration', use: { ...devices['Desktop Chrome'] } }],
  webServer: [
    { command: 'backend/.venv/bin/python backend/manage.py runserver 127.0.0.1:8000 --settings=core.demo_settings --noreload', url: 'http://127.0.0.1:8000/api/config/', reuseExistingServer: !process.env.CI },
    { command: 'npm run build && npm run preview -- --host 127.0.0.1 --port 4175 --strictPort', url: 'http://127.0.0.1:4175', reuseExistingServer: false },
  ],
})
