import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState, useRef } from "react";
import axios from "axios";
import "../App.css";

const API_BASE = "http://127.0.0.1:8000/api";

export default function QuizPage() {
  const { slug } = useParams();
  const navigate = useNavigate();

  // State Variables
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(0);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [scorecard, setScorecard] = useState(null);

  // References
  const timerRef = useRef(null);

  // Fetch Quiz details
  useEffect(() => {
    setLoading(true);
    axios
      .get(`${API_BASE}/topic/${slug}/quiz/`)
      .then((res) => {
        setQuiz(res.data);
        setTimeLeft(res.data.time_limit_seconds || 180);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load quiz details:", err);
        setLoading(false);
      });

    // Cleanup timer on unmount
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [slug]);

  // Start countdown timer
  useEffect(() => {
    if (loading || isSubmitted || timeLeft <= 0) return;

    timerRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timerRef.current);
          handleAutoSubmit();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timerRef.current);
  }, [loading, isSubmitted, timeLeft]);

  // Option selection handler
  const handleSelectChoice = (questionId, choiceId) => {
    if (isSubmitted) return;
    setAnswers((prev) => ({
      ...prev,
      [questionId]: choiceId
    }));
  };

  // Submit answers handler
  const handleSubmit = async () => {
    if (isSubmitted) return;
    if (timerRef.current) clearInterval(timerRef.current);
    
    setIsSubmitted(true);
    setLoading(true);

    try {
      const res = await axios.post(`${API_BASE}/topic/${slug}/quiz/submit/`, {
        answers: answers
      });
      setScorecard(res.data);
    } catch (err) {
      console.error("Failed to submit quiz responses:", err);
    } finally {
      setLoading(false);
    }
  };

  // Auto submit when time runs out
  const handleAutoSubmit = () => {
    alert("Time is up! Your quiz is being auto-submitted.");
    handleSubmit();
  };

  // Format seconds into MM:SS
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  if (loading && !isSubmitted) {
    return (
      <div className="app">
        <header className="navbar">
          <div className="logo-container" onClick={() => navigate("/")}>
            <div className="logo-badge">RPSC</div>
            <div className="logo-text">Prepal AI</div>
          </div>
        </header>
        <div className="quiz-page-container">
          <div className="skeleton-line" style={{ height: "80px", marginBottom: "24px" }}></div>
          <div className="skeleton-line" style={{ height: "250px", marginBottom: "24px" }}></div>
        </div>
      </div>
    );
  }

  if (!quiz) {
    return (
      <div className="app">
        <header className="navbar">
          <div className="logo-container" onClick={() => navigate("/")}>
            <div className="logo-badge">RPSC</div>
            <div className="logo-text">Prepal AI</div>
          </div>
        </header>
        <h2 style={{ textAlign: "center", marginTop: "80px", color: "var(--text-secondary)" }}>
          Quiz not found for this topic.
        </h2>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="navbar">
        <div className="logo-container" onClick={() => navigate("/")}>
          <div className="logo-badge">RPSC</div>
          <div className="logo-text">Prepal AI</div>
        </div>
        <div className="nav-actions">
          <button className="btn btn-outline" onClick={() => navigate(`/topic/${slug}`)}>
            ← Back to Topic
          </button>
        </div>
      </header>

      <div className="quiz-page-container">
        {/* TIMER BAR */}
        <div className="quiz-header">
          <div>
            <h2 style={{ fontFamily: "var(--font-heading)", color: "white" }}>{quiz.title}</h2>
            <span style={{ fontSize: "13px", color: "var(--text-secondary)" }}>
              Solve RPSC-standard multiple-choice questions
            </span>
          </div>

          {!isSubmitted && (
            <div className="timer-box">
              <span>⏱️ Time Remaining:</span>
              <span>{formatTime(timeLeft)}</span>
            </div>
          )}
        </div>

        {/* QUESTIONS LIST */}
        <div className="questions-list">
          {quiz.questions.map((question, qIdx) => {
            const selectedChoiceId = answers[question.id];
            
            return (
              <div key={question.id} className="question-card">
                <div className="question-text">
                  Q{qIdx + 1}. {question.question_text}
                </div>

                <div className="choices-list">
                  {question.choices.map((choice) => {
                    const isSelected = selectedChoiceId === choice.id;
                    return (
                      <div
                        key={choice.id}
                        className={`choice-option ${isSelected ? "selected" : ""}`}
                        onClick={() => handleSelectChoice(question.id, choice.id)}
                      >
                        <div className="choice-radio">
                          <div className="choice-radio-inner"></div>
                        </div>
                        <span className="choice-text">{choice.choice_text}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>

        {/* SUBMIT BUTTON */}
        {!isSubmitted && (
          <button
            className="btn btn-primary"
            style={{ width: "100%", padding: "16px", background: "var(--accent-success)", fontSize: "16px" }}
            onClick={handleSubmit}
          >
            Submit Quiz Answers
          </button>
        )}

        {/* SCORE CARD MODAL OVERLAY */}
        {isSubmitted && scorecard && (
          <div className="score-card-modal">
            <div className="score-card-content">
              <div className="score-circle">
                <span className="score-num">{scorecard.score}</span>
                <span className="score-label">out of {scorecard.total}</span>
              </div>

              <h2 style={{ fontFamily: "var(--font-heading)", color: "white", marginBottom: "8px" }}>
                Quiz Submission Result
              </h2>
              <p style={{ color: "var(--text-secondary)", fontSize: "14px", marginBottom: "24px" }}>
                Score: <strong>{scorecard.percentage.toFixed(1)}%</strong>
              </p>

              {/* DETAILS AND EXPLANATION REVIEW */}
              <div style={{ textAlign: "left", maxHeight: "250px", overflowY: "auto", marginBottom: "24px" }}>
                <h4 style={{ color: "white", marginBottom: "12px", borderBottom: "1px solid var(--border-color)", paddingBottom: "6px" }}>
                  Question Review:
                </h4>
                {scorecard.results.map((res, idx) => (
                  <div key={res.question_id} style={{ marginBottom: "16px" }}>
                    <div style={{ fontSize: "13px", color: "var(--text-secondary)", fontWeight: "600" }}>
                      Q{idx + 1}: {res.question_text}
                    </div>
                    <div style={{ fontSize: "13px", marginTop: "4px" }}>
                      Status:{" "}
                      <span style={{ color: res.is_correct ? "var(--accent-success)" : "red", fontWeight: "bold" }}>
                        {res.is_correct ? "Correct ✔" : "Incorrect ✘"}
                      </span>
                    </div>
                    {res.explanation && (
                      <div style={{ fontSize: "12px", color: "var(--text-muted)", marginTop: "4px", background: "var(--bg-primary)", padding: "6px", borderRadius: "4px" }}>
                        <strong>Explanation:</strong> {res.explanation}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              <div style={{ display: "flex", gap: "12px" }}>
                <button
                  className="btn btn-outline"
                  style={{ flex: 1, justifyContent: "center" }}
                  onClick={() => {
                    setIsSubmitted(false);
                    setAnswers({});
                    setScorecard(null);
                    setLoading(true);
                    // Reload to fetch fresh questions
                    axios.get(`${API_BASE}/topic/${slug}/quiz/`).then((res) => {
                      setQuiz(res.data);
                      setTimeLeft(res.data.time_limit_seconds || 180);
                      setLoading(false);
                    });
                  }}
                >
                  Retake Quiz
                </button>
                <button
                  className="btn btn-primary"
                  style={{ flex: 1, justifyContent: "center" }}
                  onClick={() => navigate(`/topic/${slug}`)}
                >
                  Done
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
