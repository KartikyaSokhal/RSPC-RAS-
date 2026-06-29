import express from "express";
import {
    addOrUpdateContent,
    getContentBySubtopic,
} from "../controllers/content.controller.js";

const router = express.Router();

router.post("/", addOrUpdateContent);
router.get("/:subtopicId", getContentBySubtopic);

export default router;
