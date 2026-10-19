import { useRef, useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import useResource from '../hooks/useResource.js'
import { post, errorMessage } from '../api/client.js'
import Skeleton from '../components/ui/Skeleton.jsx'
import StatusPanel from '../components/ui/StatusPanel.jsx'

function Practice({ quiz, slug, reload }) {
  const [answers, setAnswers] = useState({})
  const [result, setResult] = useState(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const controller = useRef(null)
  const resultHeading = useRef(null)
  useEffect(() => () => controller.current?.abort(), [])
  useEffect(() => { if (result) resultHeading.current?.focus() }, [result])
  async function check(event) {
    event.preventDefault()
    if (busy || !quiz.revision_token) return
    const request = new AbortController(); controller.current = request
    setBusy(true); setError('')
    try {
      const response = await post(`/topic/${slug}/quiz/check/`, { quiz_id: quiz.id, revision_token: quiz.revision_token, answers }, request.signal)
      if (!request.signal.aborted) setResult(response)
    } catch (err) {
      if (!request.signal.aborted) setError(errorMessage(err, 'Your answers could not be checked. They are still here; please try again.'))
    } finally { if (!request.signal.aborted) setBusy(false) }
  }
  if (result) return <div className="quiz-results"><section className="result-summary"><div className="score-ring" style={{ '--score': `${result.percentage}%` }}><div><strong>{result.score}<small>/{result.total}</small></strong><span>CORRECT</span></div></div><div><span className="eyebrow">A pause to reflect</span><h1 ref={resultHeading} tabIndex={-1}>Every answer<br /><em>is a starting point.</em></h1><p>You scored {Math.round(result.percentage)}%. Review the explanations, return to the lesson, and try again whenever you’re ready.</p><div className="button-row"><button className="button primary" onClick={reload}>Try again ↻</button><Link className="button" to={`/topic/${slug}`}>Back to the lesson →</Link></div></div></section><div className="section-heading"><h2>Understand your answers.</h2><span className="label">{result.total} QUESTIONS</span></div>{result.results.map((row, index) => {
    const question = quiz.questions.find(q => q.id === row.question_id)
    const choiceText = id => question?.choices.find(c => c.id === id)?.choice_text || 'Not answered'
    return <article key={row.question_id} className={`answer-review ${row.is_correct ? 'correct' : 'incorrect'}`}><div className="row"><span className="eyebrow">QUESTION {String(index+1).padStart(2, '0')}</span><span className="answer-badge">{row.is_correct ? '✓ Correct' : row.user_answer ? '↻ Keep exploring' : '— Not answered'}</span></div><h3>{row.question_text}</h3><p><span className="label">YOUR ANSWER</span><br />{choiceText(row.user_answer)}</p>{!row.is_correct && <p><span className="label">SUPPORTED ANSWER</span><br />{choiceText(row.correct_answer)}</p>}<div className="explanation"><strong>Why this answer?</strong><p>{row.explanation}</p><Link to={`/topic/${slug}`} className="text-link">Return to the source lesson ↗</Link></div></article>
  })}<p className="privacy-note">These results are held only in this page. No learner attempt has been saved.</p></div>
  return <><div className="page-intro quiz-intro"><span className="eyebrow">Practice, at your pace</span><h1>A moment<br /><em>to put it together.</em></h1><p>{quiz.title}</p><div className="quiz-meta"><span>{quiz.questions.length} questions</span><span>Untimed practice</span><span>No saved attempts</span></div></div>{!quiz.revision_token && <p className="notice" role="status">Preview only. Answer checking is unavailable for this quiz.</p>}<form onSubmit={check}>
    <div className="quiz-progress"><span>{Object.keys(answers).length} of {quiz.questions.length} answered</span><div><span style={{ width: `${Object.keys(answers).length / quiz.questions.length * 100}%` }} /></div></div>
    {quiz.questions.map((question, index) => <fieldset className="question-card" key={question.id}><legend><span className="eyebrow">QUESTION {String(index+1).padStart(2, '0')}</span><span className="question-title">{question.question_text}</span></legend><div className="choices-list">{question.choices.map((choice, i) => <label className={`choice-option ${answers[question.id] === choice.id ? 'selected' : ''}`} key={choice.id}><input type="radio" name={`question-${question.id}`} value={choice.id} checked={answers[question.id] === choice.id} onChange={() => setAnswers(prev => ({ ...prev, [question.id]: choice.id }))} disabled={busy} /><span className="choice-letter" aria-hidden="true">{String.fromCharCode(65+i)}</span><span>{choice.choice_text}</span></label>)}</div></fieldset>)}
    {error && <div role="alert" className="inline-error">{error}<button type="button" className="text-link" onClick={reload}>Reload practice set</button></div>}<div className="quiz-submit"><p>Unanswered questions score zero.<br />Take your time. The explanation matters.</p><button className="button primary" disabled={busy || !quiz.revision_token}>{busy ? 'Checking answers…' : 'Check my answers →'}</button></div>
  </form><p className="privacy-note">+1 for a correct answer; 0 for an incorrect or unanswered question. Practice scoring is not an official examination marking scheme.</p></>
}
export default function QuizPage() {
  const { slug } = useParams()
  const { data, loading, error, retry } = useResource(`/topic/${encodeURIComponent(slug)}/quiz/`)
  const [run, setRun] = useState(0)
  return <div className="page quiz-page"><Link className="back-link" to={`/topic/${slug}`}>← Back to the lesson</Link>{loading ? <Skeleton label="Opening the practice set…" /> : error || !data ? <StatusPanel title={error?.response?.status === 404 ? 'No reviewed quiz is available yet.' : 'Practice could not load.'} to={`/topic/${slug}`} linkLabel="Back to the lesson" retry={error?.response?.status !== 404 ? retry : undefined}>Continue with the lesson while this practice set is unavailable.</StatusPanel> : <Practice key={`${slug}:${data.id}:${run}`} quiz={data} slug={slug} reload={() => { setRun(n => n + 1); retry() }} />}</div>
}
