import { defineConfig } from '@playwright/test'
import integration from './playwright.integration.config.js'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'
const marker = JSON.parse(readFileSync(join(process.env.PREPAL_DEMO_ROOT, '.student-demo.json'), 'utf8'))
if (marker.kind !== 'prepal-student-review-v2' || marker.state !== 'ready') throw new Error('Prepare a NEW student review demo first.')
export default defineConfig({...integration, testDir: './e2e-student', timeout: 180000,
  webServer: integration.webServer.map(server => server.command.includes('manage.py') ? {...server, command: server.command.replace('core.demo_settings','core.student_demo_settings')} : server),
})
