import express from "express";
import courseRoutes from "./course.router.js";
import topicRoutes from "./topic.router.js";
import subtopicRoutes from "./subtopic.router.js";
import contentRoutes from "./content.router.js";

const router = express.Router();

router.use("/courses", courseRoutes);
router.use("/topics", topicRoutes);
router.use("/subtopics", subtopicRoutes);
router.use("/content", contentRoutes);

export default router;
