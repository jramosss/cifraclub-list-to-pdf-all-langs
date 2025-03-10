import express from "express";

const STATIC_PATH = "./static";

const app = express()

app.use(express.static(STATIC_PATH));

app.listen(8000);

console.log("Server started on port 8000");
