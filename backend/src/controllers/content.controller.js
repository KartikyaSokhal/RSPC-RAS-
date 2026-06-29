import Content from "../models/content.model.js";

export const addOrUpdateContent = async (req, res) => {
    const { subtopic, content } = req.body;

    const saved = await Content.findOneAndUpdate(
        { subtopic },
        { content },
        { upsert: true, new: true }
    );

    res.json(saved);
};

export const getContentBySubtopic = async (req, res) => {
    const content = await Content.findOne({
        subtopic: req.params.subtopicId,
    });

    if (!content) {
        return res.status(404).json({ message: "Content not found" });
    }

    res.json(content);
};
