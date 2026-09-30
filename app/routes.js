const express = require("express");
const client = require("prom-client");
const { pool } = require("./db");

const DEFAULT_LEAK_RATE_MB_S = 1;
const BYTES_PER_MB = 1024 * 1024;

client.collectDefaultMetrics();

const retainedBlocks = [];
let leakTimer = null;

const router = express.Router();

router.get("/api/notes", async (req, res) => {
  const result = await pool.query("SELECT id, content FROM notes ORDER BY id");
  res.json(result.rows);
});

router.post("/api/notes", async (req, res) => {
  const result = await pool.query(
    "INSERT INTO notes (content) VALUES ($1) RETURNING id, content",
    [req.body.content]
  );
  res.status(201).json(result.rows[0]);
});

router.put("/api/notes/:id", async (req, res) => {
  const result = await pool.query(
    "UPDATE notes SET content = $1 WHERE id = $2 RETURNING id, content",
    [req.body.content, req.params.id]
  );
  res.json(result.rows[0]);
});

router.delete("/api/notes/:id", async (req, res) => {
  await pool.query("DELETE FROM notes WHERE id = $1", [req.params.id]);
  res.status(204).end();
});

router.post("/api/leak", (req, res) => {
  const rate = Number(req.body.rate_mb_s) || DEFAULT_LEAK_RATE_MB_S;
  clearInterval(leakTimer);
  leakTimer = setInterval(() => {
    retainedBlocks.push(Buffer.alloc(rate * BYTES_PER_MB, 1));
  }, 1000);
  console.log(`[leak] started at ${rate} MB/s`);
  res.json({ status: "leak started", rate_mb_s: rate });
});

router.get("/liveness", (req, res) => {
  res.json({ status: "alive" });
});

router.get("/readiness", async (req, res) => {
  try {
    await pool.query("SELECT 1");
    res.json({ status: "ready" });
  } catch (error) {
    console.error(`[readiness] database unreachable: ${error.message}`);
    res.status(503).json({ status: "not ready", error: error.message });
  }
});

router.get("/metrics", async (req, res) => {
  res.set("Content-Type", client.register.contentType);
  res.send(await client.register.metrics());
});

module.exports = router;
