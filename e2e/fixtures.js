export const fixture = { id: 1, title: 'Fixture History', slug: 'fixture-history', revision: 1, has_children: false, children: [], related: [], resources: [], is_bookmarked: true, is_completed: true, blocks: [{ id: 11, anchor: 'block-11', block_type: 'text', content: '<p>Curated browser fixture notes.</p>' }] }
export async function intercept(page, { topic = fixture, quiz, chat = { response: 'Offline mocked browser answer.', citations: [] } } = {}) {
  await page.route('**/*', async route => {
    const url = new URL(route.request().url())
    if (url.origin !== 'http://127.0.0.1:4173') return route.abort('blockedbyclient')
    if (!url.pathname.startsWith('/api/')) return route.continue()
    if (url.pathname === '/api/config/') return route.fulfill({ json: { demo: true, csrf_token: 'fixture', ai_enabled: true } })
    if (url.pathname === '/api/auth/status/') return route.fulfill({ json: { authenticated: false, user: null } })
    if (url.pathname === '/api/topics/') return route.fulfill({ json: [topic] })
    if (url.pathname === `/api/topic/${topic.slug}/`) return route.fulfill({ json: topic })
    if (url.pathname === `/api/topic/${topic.slug}/quiz/`) return quiz ? route.fulfill({ json: quiz }) : route.fulfill({ status: 404, json: { error: { code: 'quiz_unavailable' } } })
    if (url.pathname === `/api/topic/${topic.slug}/chat/`) return route.fulfill({ json: chat })
    throw new Error(`Unexpected fixture API: ${route.request().method()} ${url.pathname}`)
  })
}
