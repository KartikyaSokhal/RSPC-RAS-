import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import { defineConfig, globalIgnores } from 'eslint/config'

export default defineConfig([
  globalIgnores(['dist/**', 'coverage/**', 'test-results/**', 'playwright-report/**', 'backend/**']),
  {
    files: ['src/**/*.{js,jsx}'],
    extends: [js.configs.recommended, reactHooks.configs.flat.recommended, reactRefresh.configs.vite],
    languageOptions: {
      ecmaVersion: 'latest', globals: globals.browser,
      parserOptions: { ecmaFeatures: { jsx: true } },
    },
    rules: { 'no-unused-vars': ['error', { varsIgnorePattern: '^[A-Z_]' }] },
  },
  {
    files: ['*.config.js', 'e2e/**/*.js', 'e2e-integration/**/*.js', 'scripts/*.mjs'],
    extends: [js.configs.recommended],
    languageOptions: { ecmaVersion: 'latest', globals: { ...globals.node, ...globals.browser } },
  },
])
