import dotenv from "dotenv";
dotenv.config();

import express from "express";
import cors from "cors";
import router from "./routes/router.js";
import connectDB from "./models/database.js";

const app = express();

/* ---------- Database ---------- */
connectDB();

/* ---------- Middlewares ---------- */
app.use(cors());
app.use(express.json());

/* ---------- Routes ---------- */
app.use("/api", router);

/* ---------- Health Check ---------- */
app.get("/", (req, res) => {
    res.send("API is running 🚀");
});

export default app;
