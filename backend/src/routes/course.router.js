import express from "express";
import { createCourse, getCourses } from "../controllers/course.controller.js";

const router = express.Router();

router.post("/", createCourse);
router.get("/", getCourses);

export default router;
