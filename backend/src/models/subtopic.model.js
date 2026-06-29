import mongoose from "mongoose";

const subtopicSchema = new mongoose.Schema(
    {
        title: { type: String, required: true },
        topic: {
            type: mongoose.Schema.Types.ObjectId,
            ref: "Topic",
            required: true,
        },
    },
    { timestamps: true }
);

export default mongoose.model("Subtopic", subtopicSchema);
