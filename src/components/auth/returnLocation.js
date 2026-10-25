export function returnLocation(from) {
  if (!from || typeof from.pathname !== 'string') return '/dashboard'
  const target = from.pathname + (from.search || '') + (from.hash || '')
  // Only local app paths; never accept protocol-relative URLs or auth loops.
  if (!target.startsWith('/') || target.startsWith('//') || target.includes('\\') || [...target].some(c => c.charCodeAt(0) <= 32) || /^\/(login|signup|reset-password)(\/|[?#]|$)/.test(target)) return '/dashboard'
  return target
}
