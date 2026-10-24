import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), 'PREPAL_')
  // Explicit local selection must also work when an older dev shell exports its legacy API.
  // Build/preview never use this development-only override; backend flags remain authoritative.
  const devOrigin = mode === 'development' ? env.PREPAL_DEV_API_ORIGIN : undefined
  const apiOrigin = devOrigin || process.env.PREPAL_API_ORIGIN || env.PREPAL_API_ORIGIN || 'http://127.0.0.1:8000'
  return {
  plugins: [react()],
  optimizeDeps: { entries: ['index.html'] },
  server: { fs: { deny: ['.env', '.env.*', '*.{crt,pem}', '**/.git/**', '**/backend/**', '**/.local/**', '**/docs/evidence/**'] }, host: '127.0.0.1', proxy: { '/api': apiOrigin } },
  preview: { host: '127.0.0.1', proxy: { '/api': apiOrigin } },
  }
})
