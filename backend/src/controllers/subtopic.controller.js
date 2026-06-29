import Subtopic from "../models/subtopic.model.js";

export const createSubtopic = async (req, res) => {
    const subtopic = await Subtopic.create(req.body);
    res.status(201).json(subtopic);
};

export const getSubtopicsByTopic = async (req, res) => {
    const subtopics = await Subtopic.find({ topic: req.params.topicId });
    res.json(subtopics);
};
