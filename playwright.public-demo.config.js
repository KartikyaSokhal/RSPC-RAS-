import { defineConfig } from '@playwright/test'
import integration from './playwright.integration.config.js'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'

const marker = JSON.parse(readFileSync(join(process.env.PREPAL_DEMO_ROOT, '.public-demo.json'), 'utf8'))
if (marker.kind !== 'prepal-local-public-demo-v1' || marker.state !== 'ready' || !marker.database.startsWith('prepal_local_public_demo_')) throw new Error('Prepare a NEW local synthetic PostgreSQL public demo first.')
export default defineConfig({ ...integration, testDir: './e2e-public-demo', timeout: 120000,
  webServer: integration.webServer.map(server => server.command.includes('manage.py')
    ? { ...server, command: server.command.replace('core.demo_settings', 'core.public_demo_settings')+' --insecure' }
    : server),
})
