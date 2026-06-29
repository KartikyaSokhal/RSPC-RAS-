import dotenv from "dotenv";
dotenv.config();

import mongoose from "mongoose";

const connectDB = async () => {
    try {
        console.log("Connecting to MongoDB with URI:");
        console.log(process.env.MONGO_URI);

        await mongoose.connect(process.env.MONGO_URI);
        console.log("MongoDB connected ✅");
    } catch (err) {
        console.error("MongoDB connection failed ❌");
        console.error(err);
        process.exit(1);
    }
};

export default connectDB;
