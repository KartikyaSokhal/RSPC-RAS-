import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState, useRef } from "react";
import axios from "axios";
import "../App.css";

const API_BASE = "http://127.0.0.1:8000/api";
const MEDIA_BASE = "http://127.0.0.1:8000";

export default function TopicPage() {
  const { slug } = useParams();
  const navigate = useNavigate();
  
  // Data States
  const [data, setData] = useState(null);
  const [sidebarTopics, setSidebarTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [scrollProgress, setScrollProgress] = useState(0);

  // Bookmark & Progress States
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);

  // Chat & AI Panel States
  const [activeTab, setActiveTab] = useState("chat"); // "chat" or "revision"
  const [messages, setMessages] = useState([]);
  const [chatInput, setChatInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [weaknessReport, setWeaknessReport] = useState("");
  const [loadingReport, setLoadingReport] = useState(false);

  // References
  const readingPanelRef = useRef(null);
  const chatEndRef = useRef(null);

  // Fetch Topic content and Sidebar list
  useEffect(() => {
    setLoading(true);
    
    const fetchTopic = axios.get(`${API_BASE}/topic/${slug}/`);
    const fetchRootTopics = axios.get(`${API_BASE}/topics/`);

    Promise.all([fetchTopic, fetchRootTopics])
      .then(([topicRes, rootRes]) => {
        setData(topicRes.data);
        setSidebarTopics(rootRes.data);
        setIsBookmarked(topicRes.data.is_bookmarked);
        setIsCompleted(topicRes.data.is_completed);
        setLoading(false);
        setScrollProgress(0); // Reset scroll tracker
        
        // Reset chat history with default greeting
        setMessages([
          {
            sender: "bot",
            text: `Ask me anything related to **${topicRes.data.title}**! You can also use the quick-action presets below to generate study cards or quiz questions.`
          }
        ]);
      })
      .catch((err) => {
        console.error("Failed to load topic page details:", err);
        setLoading(false);
      });
  }, [slug]);

  // Auto scroll chat to bottom
  useEffect(() => {
    if (activeTab === "chat") {
      chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isSending, activeTab]);

  // Track Reading Scroll Progress
  const handleScroll = () => {
    if (!readingPanelRef.current) return;
    const element = readingPanelRef.current;
    const totalHeight = element.scrollHeight - element.clientHeight;
    if (totalHeight > 0) {
      const progress = (element.scrollTop / totalHeight) * 100;
      setScrollProgress(progress);
    }
  };

  // Toggle Bookmark
  const handleBookmarkToggle = async () => {
    try {
      const res = await axios.post(`${API_BASE}/topic/${slug}/bookmark/`);
      setIsBookmarked(res.data.bookmarked);
    } catch (err) {
      console.error("Failed to toggle bookmark:", err);
    }
  };

  // Toggle Progress Completion
  const handleProgressToggle = async () => {
    try {
      const res = await axios.post(`${API_BASE}/topic/${slug}/progress/`);
      setIsCompleted(res.data.is_completed);
    } catch (err) {
      console.error("Failed to toggle progress completion:", err);
    }
  };

  // Fetch Weakness Report
  const fetchWeaknessReport = async () => {
    setLoadingReport(true);
    try {
      const res = await axios.get(`${API_BASE}/profile/weaknesses/`);
      setWeaknessReport(res.data.report);
    } catch (err) {
      console.error("Failed to fetch weakness report:", err);
      setWeaknessReport("Failed to analyze quiz attempt history. Make sure you have taken some practice quizzes!");
    } finally {
      setLoadingReport(false);
    }
  };

  // Chat message submit handler
  const handleSend = async (textToSend = chatInput, presetName = null) => {
    const msgText = textToSend.trim();
    if (!msgText && !presetName) return;

    if (!presetName) {
      setChatInput("");
    }

    const userMsg = {
      sender: "user",
      text: presetName ? `[Command: ${presetName.replace("_", " ").toUpperCase()}]` : msgText
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsSending(true);

    try {
      const payload = { message: msgText };
      if (presetName) {
        payload.preset = presetName;
      }

      const res = await axios.post(`${API_BASE}/topic/${slug}/chat/`, payload);
      
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: res.data.response }
      ]);
    } catch (err) {
      console.error("Failed to chat with AI Companion:", err);
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "I encountered an error connecting to my AI core. Please check if the backend is running and Gemini API key is configured."
        }
      ]);
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  if (loading) {
    return (
      <div className="topic-page-container">
        <aside className="sidebar-tree">
          <div className="skeleton-line" style={{ height: "20px", marginBottom: "16px", width: "50%" }}></div>
          <div className="skeleton-line" style={{ height: "32px", marginBottom: "8px" }}></div>
          <div className="skeleton-line" style={{ height: "32px", marginBottom: "8px" }}></div>
        </aside>
        <main className="reading-panel">
          <div className="reading-body">
            <div className="skeleton-line" style={{ height: "45px", marginBottom: "24px", width: "70%" }}></div>
            <div className="skeleton-line" style={{ height: "200px", marginBottom: "16px" }}></div>
            <div className="skeleton-line" style={{ height: "100px", marginBottom: "16px" }}></div>
          </div>
        </main>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="app">
        <header className="navbar">
          <div className="logo-container" onClick={() => navigate("/")}>
            <div className="logo-badge">RPSC</div>
            <div className="logo-text">Prepal AI</div>
          </div>
        </header>
        <h2 style={{ textAlign: "center", marginTop: "80px", color: "var(--text-secondary)" }}>Topic not found</h2>
      </div>
    );
  }

  const hasChildren = data.children && data.children.length > 0;
  const hasBlocks = data.blocks && data.blocks.length > 0;

  return (
    <div className="app">
      <header className="navbar">
        <div className="logo-container" onClick={() => navigate("/")}>
          <div className="logo-badge">RPSC</div>
          <div className="logo-text">Prepal AI</div>
        </div>
        <div className="nav-actions">
          <button className="btn btn-outline" onClick={() => navigate("/")}>
            ← Dashboard
          </button>
        </div>
      </header>

      <div className="topic-page-container">
        {/* LEFT SYLLABUS SIDEBAR */}
        <aside className="sidebar-tree">
          <h4 className="sidebar-title">Syllabus Index</h4>
          {sidebarTopics.map((topic) => (
            <div
              key={topic.slug}
              className={`sidebar-link ${topic.slug === slug ? "active" : ""} ${topic.is_completed ? "completed-mark" : ""}`}
              onClick={() => navigate(`/topic/${topic.slug}`)}
            >
              {topic.is_completed ? "✔ " : ""}{topic.title}
            </div>
          ))}
        </aside>

        {/* CENTER CONTENT CONTAINER */}
        <main
          className="reading-panel"
          ref={readingPanelRef}
          onScroll={handleScroll}
        >
          {/* Scroll progress tracker */}
          <div className="progress-bar-container">
            <div
              className="progress-bar-fill"
              style={{ width: `${scrollProgress}%` }}
            ></div>
          </div>

          <div className="reading-body">
            {/* BREADCRUMBS */}
            <div className="breadcrumbs">
              <span style={{ cursor: "pointer" }} onClick={() => navigate("/")}>Home</span>
              <span className="breadcrumb-separator">/</span>
              <span className="breadcrumb-active">{data.title}</span>
            </div>

            {/* Title & Bookmark header deck */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "16px", marginBottom: "24px" }}>
              <h1 className="reading-title" style={{ marginBottom: 0 }}>{data.title}</h1>
              <button 
                className="btn btn-outline"
                onClick={handleBookmarkToggle}
                style={{ borderColor: isBookmarked ? "var(--accent-warning)" : "var(--border-color)", color: isBookmarked ? "var(--accent-warning)" : "var(--text-secondary)", flexShrink: 0 }}
              >
                {isBookmarked ? "⭐ Bookmarked" : "☆ Bookmark"}
              </button>
            </div>

            {/* Drill-down subtopics list */}
            {hasChildren && (
              <div className="subtopics" style={{ background: "var(--bg-card)", border: "1px solid var(--border-color)" }}>
                <h4 style={{ fontFamily: "var(--font-heading)", marginBottom: "12px", color: "white" }}>Subtopics in this Section</h4>
                <ul style={{ listStyleType: "none" }}>
                  {data.children.map((child) => (
                    <li key={child.slug} style={{ marginBottom: "6px" }}>
                      <button
                        className="link-btn"
                        onClick={() => navigate(`/topic/${child.slug}`)}
                        style={{ color: "var(--accent-primary)", fontStyle: "normal" }}
                      >
                        • {child.title}
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Content blocks */}
            {hasBlocks ? (
              data.blocks.map((block, index) => {
                if (block.block_type === "heading") {
                  return <h2 key={index} className="block-heading">{block.content}</h2>;
                }

                if (block.block_type === "text") {
                  return (
                    <div
                      key={index}
                      className="block-text"
                      dangerouslySetInnerHTML={{ __html: block.content }}
                    />
                  );
                }

                if (block.block_type === "image" && block.file) {
                  return (
                    <img
                      key={index}
                      src={`${MEDIA_BASE}${block.file}`}
                      alt=""
                      className="block-image"
                    />
                  );
                }

                if (block.block_type === "pdf" && block.file) {
                  return (
                    <div key={index} className="block-pdf-card">
                      <span className="pdf-icon">📂</span>
                      <div className="pdf-info">
                        <div className="pdf-title">Syllabus Reference PDF File</div>
                      </div>
                      <a
                        href={`${MEDIA_BASE}${block.file}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="pdf-action"
                      >
                        Open PDF
                      </a>
                    </div>
                  );
                }

                return null;
              })
            ) : (
              !hasChildren && <p className="block-text">No content material has been uploaded yet.</p>
            )}

            {/* Reading completion progress toggle box */}
            <div style={{ marginTop: "40px", padding: "20px", background: "var(--bg-secondary)", borderRadius: "12px", border: "1px solid var(--border-color)", display: "flex", justifyContent: "space-between", alignItems: "center", gap: "16px" }}>
              <div>
                <h4 style={{ color: "white", marginBottom: "4px" }}>Reading Completion</h4>
                <p style={{ fontSize: "13px", color: "var(--text-secondary)" }}>Mark this chapter as read to track your RPSC prep progress.</p>
              </div>
              <button 
                className="btn" 
                style={{ background: isCompleted ? "var(--accent-success)" : "var(--bg-card)", color: isCompleted ? "white" : "var(--text-secondary)", border: "1px solid var(--border-color)", flexShrink: 0 }}
                onClick={handleProgressToggle}
              >
                {isCompleted ? "✔ Completed" : "Mark Completed"}
              </button>
            </div>

            {/* Quiz Launch Card */}
            <div className="quiz-launch-card" style={{ marginTop: "24px" }}>
              <div className="quiz-launch-info">
                <h3 className="quiz-launch-title">Practice Timed Quiz</h3>
                <p className="quiz-launch-desc">Test your understanding of {data.title} under RPSC exam time limits.</p>
              </div>
              <button className="btn btn-primary" onClick={() => navigate(`/quiz/${slug}`)} style={{ background: "var(--accent-success)" }}>
                Start Quiz ⚡
              </button>
            </div>
          </div>
        </main>

        {/* RIGHT AI STUDY COMPANION MENTOR */}
        <aside className="ai-companion-panel">
          {/* Header tabs */}
          <div style={{ display: "flex", borderBottom: "1px solid var(--border-color)", background: "var(--bg-card)" }}>
            <button 
              className="btn" 
              style={{ flex: 1, borderRadius: 0, padding: "14px", background: activeTab === "chat" ? "rgba(59, 130, 246, 0.08)" : "transparent", borderBottom: activeTab === "chat" ? "2px solid var(--accent-primary)" : "none", color: activeTab === "chat" ? "white" : "var(--text-secondary)", justifyContent: "center" }}
              onClick={() => setActiveTab("chat")}
            >
              💬 Mentor Chat
            </button>
            <button 
              className="btn" 
              style={{ flex: 1, borderRadius: 0, padding: "14px", background: activeTab === "revision" ? "rgba(59, 130, 246, 0.08)" : "transparent", borderBottom: activeTab === "revision" ? "2px solid var(--accent-primary)" : "none", color: activeTab === "revision" ? "white" : "var(--text-secondary)", justifyContent: "center" }}
              onClick={() => {
                setActiveTab("revision");
                fetchWeaknessReport();
              }}
            >
              🎯 Revision Room
            </button>
          </div>

          {activeTab === "chat" ? (
            <>
              <div className="ai-chatbox">
                {messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`chat-msg ${msg.sender === "user" ? "chat-msg-user" : "chat-msg-bot"}`}
                  >
                    {msg.sender === "bot" ? (
                      <div
                        dangerouslySetInnerHTML={{
                          __html: msg.text
                            .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
                            .replace(/\*(.*?)\*/g, "<em>$1</em>")
                            .replace(/\n/g, "<br />")
                        }}
                      />
                    ) : (
                      msg.text
                    )}
                  </div>
                ))}

                {isSending && (
                  <div className="typing-indicator">
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                  </div>
                )}
                <div ref={chatEndRef} />
              </div>

              {/* Quick Action Presets Button Grid */}
              <div className="presets-grid">
                <button className="preset-btn" onClick={() => handleSend("Explain beginner details.", "explain_beginner")}>
                  🎓 Simple Explain
                </button>
                <button className="preset-btn" onClick={() => handleSend("Analyze past exam patterns.", "pyq_analysis")}>
                  🔍 PYQ Trends
                </button>
                <button className="preset-btn" onClick={() => handleSend("Explain key syllabus highlights.", "revision")}>
                  ⚡ 5-Min Summary
                </button>
                <button className="preset-btn" onClick={() => handleSend("Create memory mnemonics.", "mnemonics")}>
                  🧠 Memory Tricks
                </button>
                <button className="preset-btn" onClick={() => handleSend("Draft 3 MCQ questions.", "generate_mcqs")}>
                  📝 Practice MCQs
                </button>
                <button className="preset-btn" onClick={() => handleSend("Test my knowledge.", "examiner_mode")}>
                  🎯 Ask Me (AI Exam)
                </button>
              </div>

              {/* Chat input box */}
              <div className="chat-input-area">
                <input
                  type="text"
                  placeholder="Ask a doubt or type request..."
                  className="ai-input"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  disabled={isSending}
                />
                <button className="btn btn-primary" onClick={() => handleSend()} disabled={isSending}>
                  Send
                </button>
              </div>
            </>
          ) : (
            /* REVISION & WEAKNESS DASHBOARD */
            <div style={{ flex: 1, padding: "20px", overflowY: "auto", background: "var(--bg-primary)" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
                <h4 style={{ fontFamily: "var(--font-heading)", color: "white" }}>AI Weakness Analysis</h4>
                <button 
                  className="btn btn-outline" 
                  style={{ padding: "4px 8px", fontSize: "11px" }} 
                  onClick={fetchWeaknessReport}
                  disabled={loadingReport}
                >
                  🔄 Reload
                </button>
              </div>

              {loadingReport ? (
                <div>
                  <div className="skeleton-line" style={{ height: "16px", marginBottom: "8px", width: "100%" }}></div>
                  <div className="skeleton-line" style={{ height: "16px", marginBottom: "8px", width: "95%" }}></div>
                  <div className="skeleton-line" style={{ height: "16px", marginBottom: "8px", width: "80%" }}></div>
                </div>
              ) : (
                <div 
                  className="block-text"
                  style={{ fontSize: "13px", lineHeight: "1.6", whiteSpace: "pre-line" }}
                  dangerouslySetInnerHTML={{
                    __html: weaknessReport
                      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
                      .replace(/\*(.*?)\*/g, "<em>$1</em>")
                  }}
                />
              )}
            </div>
          )}
        </aside>
      </div>
    </div>
  );
}
