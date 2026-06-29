import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/home";
import TopicPage from "./pages/topicPage";
import QuizPage from "./pages/quizPage";
import "./App.css";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/topic/:slug" element={<TopicPage />} />
        <Route path="/quiz/:slug" element={<QuizPage />} />
      </Routes>
    </BrowserRouter>
  );
}

