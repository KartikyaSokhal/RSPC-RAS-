import { Link, useParams } from 'react-router-dom'
import useAuth from '../hooks/useAuth.js'
import useResource from '../hooks/useResource.js'
import Skeleton from '../components/ui/Skeleton.jsx'
import StatusPanel from '../components/ui/StatusPanel.jsx'
export default function AttemptPage() {
  const {id} = useParams()
  const {authenticated} = useAuth()
  const {data, loading, error, retry} = useResource(authenticated ? `/attempts/${id}/` : null)
  if (!authenticated) return <div className="page"><h1>Practice history</h1><Link to="/login">Sign in to view your attempts</Link></div>
  if (loading) return <div className="page"><Skeleton label="Loading your practice history…" /></div>
  if (error || !data) return <div className="page"><StatusPanel title="Practice history is unavailable." retry={retry}>Only your own attempts are accessible.</StatusPanel></div>
  const snapshot=data.snapshot
  return <div className="page quiz-page"><Link to="/dashboard">← Dashboard</Link><h1>{snapshot.title || 'Previous practice attempt'}</h1><p>{data.score} / {data.total} correct · {new Date(data.attempted_at).toLocaleString()}</p><p>Saved answers and explanations reflect the reviewed version used for this attempt.</p>
    {!data.history_available ? <p>Detailed question snapshots are unavailable for this legacy attempt.</p> : <><Link className="button" to={`/${snapshot.kind === 'collection' ? 'practice' : 'quiz'}/${snapshot.source_slug}`}>Reattempt current reviewed practice</Link>{snapshot.questions.map((question,index) => {
      const choice = id => question.choices.find(c => c.id === id)?.choice_text || 'Not answered'
      return <article className="answer-review" key={question.question_id}><h2>Question {index+1}: {question.question_text}</h2><p>{question.is_correct ? 'Correct' : 'Review this question'}</p><p>Your answer: {choice(question.user_answer)}</p><p>Supported answer: {choice(question.correct_answer)}</p><p>{question.explanation}</p><small>{question.subject_title} · {question.topic_title}</small></article>
    })}</>}
  </div>
}
