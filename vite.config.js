import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
const apiOrigin = process.env.PREPAL_API_ORIGIN || 'http://127.0.0.1:8000'
export default defineConfig({
  plugins: [react()],
  optimizeDeps: { entries: ['index.html'] },
  server: { fs: { deny: ['.env', '.env.*', '*.{crt,pem}', '**/.git/**', '**/backend/**', '**/.local/**', '**/docs/evidence/**'] }, host: '127.0.0.1', proxy: { '/api': apiOrigin } },
  preview: { host: '127.0.0.1', proxy: { '/api': apiOrigin } },
})
