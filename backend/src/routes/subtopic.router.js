import express from "express";
import {
    createSubtopic,
    getSubtopicsByTopic,
} from "../controllers/subtopic.controller.js";

const router = express.Router();

router.post("/", createSubtopic);
router.get("/topic/:topicId", getSubtopicsByTopic);

export default router;
