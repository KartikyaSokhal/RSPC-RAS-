import mongoose from "mongoose";

const contentSchema = new mongoose.Schema(
    {
        subtopic: {
            type: mongoose.Schema.Types.ObjectId,
            ref: "Subtopic",
            required: true,
            unique: true,
        },
        content: {
            type: String,
            required: true,
        },
    },
    { timestamps: true }
);

export default mongoose.model("Content", contentSchema);
