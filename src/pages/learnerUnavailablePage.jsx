import { Link } from 'react-router-dom'
import { LEARNER_FEATURES_UNAVAILABLE_MESSAGE } from '../learnerFeatures.js'

export default function LearnerUnavailablePage() {
  return <div className="page info-page">
    <div className="page-intro">
      <span className="eyebrow">Content-first release</span>
      <h1>Personalized features are unavailable.</h1>
      <p>{LEARNER_FEATURES_UNAVAILABLE_MESSAGE}</p>
      <Link to="/syllabus" className="button primary">Browse the syllabus</Link>
    </div>
  </div>
}
