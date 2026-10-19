// Temporary P002 product gate. The API independently rejects every identity.
// Remove only with verified owned endpoints in P010/P012; not a runtime toggle.
export const LEARNER_FEATURES_AVAILABLE = false
export const LEARNER_FEATURES_UNAVAILABLE_MESSAGE =
  'Personalized features are temporarily unavailable while learner accounts are being secured. Bookmarks, completion tracking, saved quiz history and weakness reports are paused. Reading remains available.'
