import axios from 'axios'
export const topic = { id: 1, title: 'Fixture History', slug: 'fixture-history', revision: 1, children: [], has_children: false, breadcrumbs: [], related: [], resources: [], is_bookmarked: true, is_completed: true,
  blocks: [{ id: 11, anchor: 'block-11', block_type: 'text', content: '<p>Curated fixture notes.</p>', order: 1 }] }
export const quiz = { id: 7, title: 'Fixture quiz', revision_token: 'fixture-signed-token', questions: [{ id: 11, question_text: 'Which fixture answer?', choices: [{ id: 21, choice_text: 'Correct fixture' }, { id: 22, choice_text: 'Other fixture' }] }] }
export const config = { csrf_token: 'fixture-csrf', ai_enabled: true, demo: true }
export function mockAPI({ lesson = topic, practice = quiz, chat = { response: 'Mocked tutor explanation.', citations: [] } } = {}) {
  axios.get.mockReset().mockImplementation(url => {
    if (url.endsWith('/config/')) return Promise.resolve({ data: config })
    if (url.includes('/topics/')) return Promise.resolve({ data: [lesson] })
    if (url.endsWith('/quiz/')) return Promise.resolve({ data: practice })
    if (url.includes(`/topic/${lesson.slug}/`)) return Promise.resolve({ data: lesson })
    return Promise.reject({ response: { status: 404, data: { error: { code: 'not_found' } } } })
  })
  axios.post.mockReset().mockImplementation(url => {
    if (url.endsWith('/chat/')) return Promise.resolve({ data: chat })
    if (url.endsWith('/quiz/check/')) return Promise.resolve({ data: { quiz_id: 7, score: 1, total: 1, percentage: 100, results: [{ question_id: 11, question_text: 'Which fixture answer?', user_answer: 21, correct_answer: 21, is_correct: true, explanation: 'The source supports this fixture.' }] } })
    throw new Error(`Unapproved endpoint: ${url}`)
  })
}
