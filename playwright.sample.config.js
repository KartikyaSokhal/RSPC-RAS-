import { defineConfig } from '@playwright/test'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'
import integration from './playwright.integration.config.js'

const marker = JSON.parse(readFileSync(join(process.env.PREPAL_DEMO_ROOT, '.sample-demo.json'), 'utf8'))
if (marker.kind !== 'prepal-academic-sample-v1' || marker.state !== 'ready') {
  throw new Error('Use a prepared isolated academic sample demo for this suite.')
}
export default defineConfig({ ...integration, testDir: './e2e-sample', timeout: 180000 })
