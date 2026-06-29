import Topic from "../models/topic.model.js";

export const createTopic = async (req, res) => {
    const topic = await Topic.create(req.body);
    res.status(201).json(topic);
};

export const getTopicsByCourse = async (req, res) => {
    const topics = await Topic.find({ course: req.params.courseId });
    res.json(topics);
};
