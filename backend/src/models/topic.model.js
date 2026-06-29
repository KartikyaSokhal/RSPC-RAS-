import mongoose from "mongoose";

const topicSchema = new mongoose.Schema(
    {
        title: { type: String, required: true },
        course: {
            type: mongoose.Schema.Types.ObjectId,
            ref: "Course",
            required: true,
        },
    },
    { timestamps: true }
);

export default mongoose.model("Topic", topicSchema);
