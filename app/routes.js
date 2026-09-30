const express = require("express");
const client = require("prom-client");

const DEFAULT_LEAK_RATE_MB_S = 1;
const BYTES_PER_MB = 1024 * 1024;

client.collectDefaultMetrics();

const retainedBlocks = [];
let leakTimer = null;

const router = express.Router();

router.post("/api/leak", (req, res) => {

  // env que guarda quanto de memória vai ser alocada 
  const rate = Number(req.body.rate_mb_s) || DEFAULT_LEAK_RATE_MB_S;

  // para o processo em execução caso a rota da api seja chamada novamente 
  clearInterval(leakTimer);
  
  // função que vai executar a cada 1s provocando o vazamento de memória 
  leakTimer = setInterval(() => {
    // função que vai alocar mémoria para provovar o vazameanto
    retainedBlocks.push(Buffer.alloc(rate * BYTES_PER_MB, 1));
  }, 1000);
  console.log(`[leak] started at ${rate} MB/s`);
  res.json({ status: "leak started", rate_mb_s: rate });
});

router.get("/liveness", (req, res) => {
  res.json({ status: "alive" });
});

router.get("/metrics", async (req, res) => {
  res.set("Content-Type", client.register.contentType);
  res.send(await client.register.metrics());
});

module.exports = router;
