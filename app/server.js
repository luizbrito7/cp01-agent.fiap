const express = require("express");
const router = require("./routes");
const { init } = require("./db");

const PORT = process.env.PORT || 3000;

const app = express();
app.use(express.json());
app.use(express.static("public"));
app.use(router);

app.listen(PORT, () => console.log(`[app] listening on port ${PORT}`));

init().catch((error) =>
  console.error(`[app] database init failed: ${error.message}`)
);
