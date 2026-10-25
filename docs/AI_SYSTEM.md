## Hosted public-homepage candidate

The hosted synthetic-login profile forces Gemini, AI budgets, Google and recovery email off even if inherited environment flags differ. Student login never activates a provider. Existing mock-only retrieval/sanitization regression tests remain; no live AI acceptance, credentials or paid requests belong to this release.

---

## Local student-gated preview boundary

The new local-only public-demo profile forces Gemini, guest AI and Google credentials off. Public copy follows ai_enabled=false. Student sign-in never enables the Tutor provider or paid requests. Retrieval, sanitization and provider implementation are unchanged; this batch does not establish live AI readiness.

---

# Current-lesson Tutor

The existing Django Gemini adapter and quota/cost architecture are retained. `DatabaseRetrievalProvider.retrieve` now accepts evidence **only from note blocks in the currently open published lesson**. It never retrieves other topics, related/prerequisite documents, PDF pages, general website material or internet results. `allow_related=true` is rejected, and the provider itself enforces scope even if directly called with that argument. Reader hyperlinks do not expand Tutor evidence.

Selection must match a current note source ID, revision and text substring. History helps interpret intent and is not factual evidence. Bounded lexical ranking filters generic question terms, uses 2,400-character windows and abstains if nothing relevant remains. A PDF-only lesson can be read/completed but has no Tutor note evidence and must refuse. This is not embeddings or a claim of semantic retrieval quality.

The UI retains one bottom-right launcher, mobile/desktop closable panel, question input, Explain Simply, Summarize This Lesson and Explain Selected Passage. Raw HTML is disabled in SafeMarkdown. Server-built citations can only reference current lesson blocks; evidence scope is checked before provider invocation and publication is checked again before response. Obvious instruction-override/private-prompt requests refuse before spending. Evidence/history remain untrusted data in provider instructions. These controls constrain provenance and scope; they do not mathematically establish factual entailment or comprehensive prompt-injection immunity.

## Limits and costs

Question: 2,000 characters; history: six messages/4,000 total characters; selection: 1,000 characters; at most 12 chunks/18,000 candidate characters. Final UTF-8 upper bound plus framing is limited to 16,000 input tokens and 1,000 output tokens. Old history/low-priority chunks are trimmed before reservation. Gemini uses the pinned official SDK, 30-second timeout, one attempt, JSON output mode, no tools and thinking budget zero. Approved model compatibility still needs live evaluation.

AI_ENABLED=false and AI_GUEST_ENABLED=false are normal defaults. Authenticated requests use stable per-user identity and CSRF; guest requests require the explicit guest gate and signed visitor cookie. Default limits remain 20 requests per identity/day, 100 per IP/day and five/minute; all workers must share the PostgreSQL quota database. Trusted proxies alone may supply validated X-Real-IP. Raw IPs/prompts/answers are not stored in quota rows.

Live mode requires an owner-approved model, server-only key, positive daily cap and positive input/output microcurrency rates. Conservative reservations cover the full bounded request before one provider call. Unknown/timeout billing retains the full reservation; only verified bounded actual usage releases unused cost. Expired in-flight locks release availability, not money. PostgreSQL concurrency and settlement tests verify caps/idempotence. Do not derive rates from stale prices or enable paid requests automatically.

Demo/student-review settings clear real keys and use DemoProvider only; responses explicitly identify mock evidence quotation. Tests cover strict scope, refusal, prompt injection, citation validation, quota identity/limits, timeout/provider failure and existing cost concurrency. **No live Gemini request was made.** Remaining: explicit provider/model/budget approval, real Hindi/English grounding/refusal evaluation and billing reconciliation. [Official SDK](https://googleapis.github.io/python-genai/), [testing](TESTING.md), [deployment](DEPLOYMENT.md).
