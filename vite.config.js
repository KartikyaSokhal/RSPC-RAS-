import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig({
  plugins: [react()],
  optimizeDeps: { entries: ['index.html'] },
  server: { fs: { deny: ['.env', '.env.*', '*.{crt,pem}', '**/.git/**', '**/backend/**', '**/.local/**', '**/docs/evidence/**'] }, host: '127.0.0.1', proxy: { '/api': 'http://127.0.0.1:8000', '/private-media': 'http://127.0.0.1:8000' } },
  preview: { host: '127.0.0.1', proxy: { '/api': 'http://127.0.0.1:8000', '/private-media': 'http://127.0.0.1:8000' } },
})
