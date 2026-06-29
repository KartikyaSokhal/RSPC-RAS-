import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../App.css";

const API_BASE = "http://127.0.0.1:8000/api";

function TopicItem({ item, level = 0, searchQuery = "" }) {
  const [open, setOpen] = useState(level === 0);
  const [children, setChildren] = useState(item.children ?? null);
  const [loadingChildren, setLoadingChildren] = useState(false);
  const navigate = useNavigate();

  const hasChildren = Array.isArray(children) && children.length > 0;

  // Filter children based on search query
  const filteredChildren = hasChildren
    ? children.filter((child) =>
        child.title.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : [];

  // Determine if this topic matches search query
  const matchesSearch = item.title.toLowerCase().includes(searchQuery.toLowerCase());
  
  // If search query is active, only render if this item or any of its children match
  const shouldRender =
    searchQuery === "" || matchesSearch || filteredChildren.length > 0;

  const handleToggle = async (e) => {
    e.stopPropagation();

    // Lazy-load children on first expand
    if (children === null) {
      try {
        setLoadingChildren(true);
        const res = await axios.get(`${API_BASE}/topic/${item.slug}/`);
        setChildren(res.data.children || []);
      } catch (err) {
        console.error("Failed to load children:", err);
        setChildren([]);
      } finally {
        setLoadingChildren(false);
      }
    }

    setOpen((prev) => !prev);
  };

  const handleNavigate = () => {
    navigate(`/topic/${item.slug}`);
  };

  useEffect(() => {
    if (level === 0 && children === null) {
      handleToggle({ stopPropagation: () => {} });
    }
  }, []);

  // Force open state if search is active and child elements are matched
  useEffect(() => {
    if (searchQuery !== "" && filteredChildren.length > 0) {
      setOpen(true);
    }
  }, [searchQuery, filteredChildren.length]);

  if (!shouldRender) return null;

  return (
    <div style={{ marginLeft: level > 0 ? 16 : 0 }} className="topic-node">
      <div className="topic-header" onClick={handleNavigate}>
        <div className="topic-title-wrapper">
          <span className="topic-index">{level + 1}.</span>
          <span className="topic-title">
            {item.is_completed && <span style={{ color: "var(--accent-success)", marginRight: "6px" }}>✔</span>}
            {item.title}
            {item.is_bookmarked && <span style={{ color: "var(--accent-warning)", marginLeft: "8px" }}>⭐</span>}
          </span>
        </div>

        {item.has_children && (
          <div
            className={`arrow-icon ${open ? "open" : ""}`}
            onClick={handleToggle}
          >
            ▶
          </div>
        )}
      </div>

      {open && (
        <div className="subtopics-list">
          {loadingChildren && <div className="loading block-text">Loading subtopics…</div>}

          {!loadingChildren &&
            (searchQuery !== "" ? filteredChildren : children || []).map((child) => (
              <TopicItem
                key={child.slug}
                item={child}
                level={level + 1}
                searchQuery={searchQuery}
              />
            ))}
        </div>
      )}
    </div>
  );
}

export default function Home() {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    axios
      .get(`${API_BASE}/topics/`)
      .then((res) => {
        setTopics(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load topics:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="app">
      <header className="navbar">
        <div className="logo-container" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
          <div className="logo-badge">RPSC</div>
          <div className="logo-text">Prepal AI</div>
        </div>
        <div className="nav-actions">
          <button className="btn btn-outline" onClick={() => window.open('https://rpsc.rajasthan.gov.in/', '_blank')}>
            Official Site
          </button>
        </div>
      </header>

      <section className="hero">
        <div className="hero-content">
          <span className="hero-tag">AI-Powered Prep</span>
          <h1 className="hero-title">Master the RPSC RAS Syllabus</h1>
          <p className="hero-desc">
            Explore the official syllabus with granular notes, test yourself with timed quizzes, and resolve doubts instantly with your personal AI Study Companion.
          </p>
          <button className="btn btn-primary" onClick={() => document.getElementById("syllabus").scrollIntoView({ behavior: 'smooth' })}>
            Start Exploring 📚
          </button>
        </div>
      </section>

      <main className="syllabus-container" id="syllabus">
        <div className="syllabus-card">
          <div className="search-container">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              placeholder="Search syllabus segments and subtopics..."
              className="search-input"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          {loading ? (
            <div style={{ padding: "40px 0" }}>
              <div className="skeleton-line" style={{ height: "40px", marginBottom: "12px", width: "100%" }}></div>
              <div className="skeleton-line" style={{ height: "40px", marginBottom: "12px", width: "95%" }}></div>
              <div className="skeleton-line" style={{ height: "40px", marginBottom: "12px", width: "90%" }}></div>
            </div>
          ) : (
            <div className="syllabus-tree">
              {topics.map((topic) => (
                <TopicItem
                  key={topic.slug}
                  item={topic}
                  searchQuery={searchQuery}
                />
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
