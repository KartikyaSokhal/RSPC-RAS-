import express from "express";
import {
    createTopic,
    getTopicsByCourse,
} from "../controllers/topic.controller.js";

const router = express.Router();

router.post("/", createTopic);
router.get("/course/:courseId", getTopicsByCourse);

export default router;
