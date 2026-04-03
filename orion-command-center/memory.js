const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = path.resolve(__dirname, 'orion_memory.db');
const db = new sqlite3.Database(dbPath);

// Initialize DB schema
db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS memory (
    key TEXT PRIMARY KEY,
    value TEXT
  )`);
});

/**
 * Save a memory entry. Updates if existing.
 */
function save(key, value) {
  return new Promise((resolve, reject) => {
    db.run(
      `INSERT INTO memory (key, value) VALUES (?, ?)
       ON CONFLICT(key) DO UPDATE SET value = ?`,
      [key, value, value],
      function (err) {
        if (err) reject(err);
        else resolve();
      }
    );
  });
}

/**
 * Retrieve a specific memory entry.
 */
function retrieve(key) {
  return new Promise((resolve, reject) => {
    db.get(`SELECT value FROM memory WHERE key = ?`, [key], (err, row) => {
      if (err) reject(err);
      else resolve(row ? row.value : null);
    });
  });
}

/**
 * Get all stored memories as a single string to inject into LLM prompt.
 */
function getAllContext() {
  return new Promise((resolve, reject) => {
    db.all(`SELECT key, value FROM memory`, (err, rows) => {
      if (err) reject(err);
      else {
        if (!rows || rows.length === 0) {
          resolve("No prior memories.");
        } else {
          const contextLines = rows.map(r => `${r.key}: ${r.value}`);
          resolve(contextLines.join('\n'));
        }
      }
    });
  });
}

module.exports = {
  save,
  retrieve,
  getAllContext
};
