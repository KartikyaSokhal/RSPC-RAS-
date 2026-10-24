import { useEffect, useState } from 'react'

export default function useTheme() {
  const [preference, setPreference] = useState(() => {
    try {
      const saved = localStorage.getItem('prepal-theme')
      if (saved === 'light' || saved === 'dark') return saved
      return 'system'
    } catch {
      return 'system'
    }
  })

  const [systemDark, setSystemDark] = useState(() => {
    return window.matchMedia?.('(prefers-color-scheme: dark)').matches ?? false
  })

  useEffect(() => {
    const media = window.matchMedia?.('(prefers-color-scheme: dark)')
    const update = e => setSystemDark(e.matches)
    media?.addEventListener('change', update)
    return () => media?.removeEventListener('change', update)
  }, [])

  const theme = preference === 'system' ? (systemDark ? 'dark' : 'light') : preference

  useEffect(() => {
    document.documentElement.dataset.theme = theme
    document.documentElement.style.colorScheme = theme
    try {
      localStorage.setItem('prepal-theme', preference)
      // Clean up legacy multi-palette setting
      localStorage.removeItem('prepal-palette')
      document.documentElement.removeAttribute('data-palette')
    } catch {
      /* Storage is optional */
    }
  }, [preference, theme])

  const toggleTheme = () => {
    setPreference(current => {
      const effective = current === 'system' ? (systemDark ? 'dark' : 'light') : current
      return effective === 'dark' ? 'light' : 'dark'
    })
  }

  return { theme, toggleTheme, preference, setPreference }
}
