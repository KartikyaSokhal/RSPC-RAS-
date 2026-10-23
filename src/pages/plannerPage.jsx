import { useState } from 'react'
import { Link } from 'react-router-dom'
import useAuth from '../hooks/useAuth.js'
import useSyllabus from '../hooks/useSyllabus.js'
import useResource from '../hooks/useResource.js'
import { get, post, errorMessage } from '../api/client.js'

const weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
const today = () => new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 10)
function Selection({ topics, selected, change }) {
  return <ul className="planner-topic-tree">{topics.map(topic => <li key={topic.id}><label><input type="checkbox" checked={selected.includes(topic.id)} disabled={!topic.is_published} onChange={e => change(e.target.checked ? [...selected, topic.id] : selected.filter(id => id !== topic.id))} />{topic.title}{!topic.is_published && ' (unpublished)'}</label>{topic.children?.length > 0 && <Selection topics={topic.children} selected={selected} change={change} />}</li>)}</ul>
}
export default function PlannerPage() {
  const { authenticated, loading: authLoading } = useAuth()
  const syllabus = useSyllabus()
  const plans = useResource(authenticated ? '/plans/' : null)
  const [draft, setDraft] = useState({title: 'My study plan', mode: 'learn', study_days: [0,1,2,3,4], daily_minutes: 120, default_estimate_minutes: 90, start_date: today(), exam_date: null, topic_ids: []})
  const [plan, setPlan] = useState(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [rescheduleDate, setRescheduleDate] = useState(today())
  const [limit, setLimit] = useState(100)
  const edit = (field, value) => setDraft(previous => ({...previous, [field]: value}))
  async function operation(work) {
    setBusy(true); setError('')
    try { const data = await work(); setPlan(data); plans.retry(); return data }
    catch (err) { setError(errorMessage(err)); return null } finally { setBusy(false) }
  }
  if (authLoading) return <div className="page"><p role="status">Loading student access…</p></div>
  if (!authenticated) return <div className="page"><h1>Your study plan</h1><p><Link to="/login">Sign in</Link> to create a private schedule.</p></div>
  return <div className="page planner-page"><Link to="/dashboard">← Dashboard</Link><h1>Create a study plan</h1><p>Approximate learning, revision and MCQ time, scheduled without AI. Completing a task tracks planned work; mark the lesson completed separately when ready.</p>
    {plans.error && <p role="alert">Your saved plans could not load. <button className="button" onClick={plans.retry}>Retry saved plans</button></p>}
    {plans.data?.length > 0 && <label className="saved-plan-select">Edit a saved plan<select value={plan?.id || ''} onChange={async e => {
      if (!e.target.value) { setPlan(null); return }
      const data = await operation(() => get(`/plans/${e.target.value}/`))
      if (data) { setDraft(Object.fromEntries(Object.keys(draft).map(key => [key, data[key]]))); setLimit(100) }
    }}><option value="">New plan</option>{plans.data.map(p => <option key={p.id} value={p.id}>{p.title}</option>)}</select></label>}
    <div className="planner-layout"><section className="card planner-inputs" aria-label="Study plan inputs"><form className="auth-form" onSubmit={async e => {
      e.preventDefault(); await operation(() => post(plan ? `/plans/${plan.id}/` : '/plans/', {...draft, ...(plan ? {revision: plan.revision} : {})}))
    }}>
      <label>Plan title<input required maxLength={120} value={draft.title} onChange={e => edit('title', e.target.value)} /></label>
      <label>Learning mode<select value={draft.mode} onChange={e => edit('mode', e.target.value)}><option value="learn">Learn from Scratch</option><option value="revision">Quick Revision</option></select></label>
      <fieldset><legend>Subjects and subtopics to cover</legend><p>Choose a subject to include its published learning units. Empty outlines are excluded.</p>{syllabus.loading ? <p role="status">Loading syllabus…</p> : syllabus.error ? <p role="alert">Syllabus unavailable. <button type="button" onClick={syllabus.retry}>Retry syllabus</button></p> : <Selection topics={syllabus.data || []} selected={draft.topic_ids} change={value => edit('topic_ids', value)} />}</fieldset>
      <fieldset><legend>Study days</legend><div className="study-day-options">{weekdays.map((day, i) => <label key={day}><input type="checkbox" checked={draft.study_days.includes(i)} onChange={e => edit('study_days', e.target.checked ? [...draft.study_days, i] : draft.study_days.filter(d => d !== i))} />{day}</label>)}</div></fieldset>
      <label>Daily study hours<input type="number" min="0.25" max="12" step="0.25" required value={draft.daily_minutes / 60} onChange={e => edit('daily_minutes', Math.round(Number(e.target.value) * 60))} /></label>
      <label>Default approximate minutes per lesson<input type="number" min="15" max="2400" required value={draft.default_estimate_minutes} onChange={e => edit('default_estimate_minutes', Number(e.target.value))} /><span className="form-hint">Used only when an editor estimate is missing. Includes learning, revision and practice. Quick Revision uses half the total, with a minimum of 15 minutes.</span></label>
      <label>Start date<input type="date" required value={draft.start_date} onChange={e => edit('start_date', e.target.value)} /></label>
      <label>Optional exam target date<input type="date" value={draft.exam_date || ''} onChange={e => edit('exam_date', e.target.value || null)} /></label>
      <button className="button primary" disabled={busy || !draft.topic_ids.length || !draft.study_days.length}>{busy ? 'Saving…' : plan ? 'Update plan' : 'Generate study plan'}</button>
    </form></section><section className="planner-output" aria-label="Your study schedule">
      {error && <p role="alert" className="inline-error">{error}</p>}
      {!plan ? <div className="card"><h2>A schedule that fits your week</h2><p>Select published subjects or subtopics, your study days and available hours. Your daily tasks and weekly/monthly targets will appear here.</p></div> : <>
        <div className="card"><h2>{plan.title}</h2><p role="status">Estimated completion: {plan.estimated_completion_date}. {plan.completed_minutes} / {plan.total_minutes} minutes completed.</p><progress aria-label="Plan work completed" value={plan.completed_minutes} max={plan.total_minutes || 1} />
          {!plan.exam_feasible && <p className="notice" role="alert">This schedule extends beyond your exam target. Increase your study capacity or reduce selected content.</p>}
          {plan.missing_estimate_topics.length > 0 && <p>{plan.missing_estimate_topics.length} learning units use your editable default estimate.</p>}
          {plan.unavailable_topic_ids.length > 0 && <p>Some saved units are no longer published. Completed history is preserved; update the plan to refresh unfinished work.</p>}
          <label>Reschedule unfinished work from<input type="date" value={rescheduleDate} onChange={e => setRescheduleDate(e.target.value)} /></label><button className="button" disabled={busy} onClick={() => operation(() => post(`/plans/${plan.id}/reschedule/`, {revision: plan.revision, start_date: rescheduleDate}))}>Reschedule unfinished tasks</button>
        </div>
        <details className="card"><summary>Weekly subject targets</summary>{plan.weekly_targets.map(w => <div key={w.week}><h3>{w.week}</h3><p>{w.completed_minutes} / {w.minutes} minutes</p>{Object.entries(w.subjects).map(([name, minutes]) => <p key={name}>{name}: {minutes} minutes</p>)}</div>)}</details>
        <details className="card"><summary>Monthly targets</summary>{plan.monthly_targets.map(m => <p key={m.month}>{m.month}: {m.completed_minutes} / {m.minutes} minutes; {m.completed_units} / {m.learning_units} units of planned work finished</p>)}</details>
        <h2>Daily tasks</h2>{plan.tasks.slice(0, limit).map(task => <article className="card planner-task" key={task.id}><span>{task.due_date} · {task.kind} · approximately {task.minutes} min</span><h3>{task.slug ? <Link to={`/topic/${task.slug}`}>{task.title}</Link> : task.title}</h3><label><input type="checkbox" checked={task.is_completed} disabled={busy || !task.slug} onChange={e => operation(() => post(`/plans/${plan.id}/tasks/${task.id}/`, {is_completed: e.target.checked}))} />Task completed</label>{task.used_default && <small>Default estimate</small>}</article>)}{plan.tasks.length > limit && <button className="button" onClick={() => setLimit(n => n + 100)}>Show more tasks</button>}
      </>}
    </section></div></div>
}
