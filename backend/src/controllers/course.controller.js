import Course from "../models/course.model.js";

export const createCourse = async (req, res) => {
    const course = await Course.create(req.body);
    res.status(201).json(course);
};

export const getCourses = async (req, res) => {
    const courses = await Course.find();
    res.json(courses);
};
