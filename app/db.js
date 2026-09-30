const { Pool } = require("pg");

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

async function init() {
  await pool.query(
    "CREATE TABLE IF NOT EXISTS notes (id SERIAL PRIMARY KEY, content TEXT NOT NULL)"
  );
}

module.exports = { pool, init };
