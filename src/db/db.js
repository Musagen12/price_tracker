// src/db/db.js
import Database from 'better-sqlite3';
import path from 'path';

// Create a database instance with the path to your database file
const dbPath = path.join(process.cwd(), 'src', 'db', 'database.sqlite');
const db = new Database(dbPath);

// Initialize your database schema (create tables)
const initDb = () => {
  db.exec(`
    CREATE TABLE IF NOT EXISTS price_checks (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT NOT NULL,
      target_price REAL NOT NULL,
      product_id TEXT NOT NULL,  -- product_id is now included as a TEXT field
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  `);

  // Optionally ensure the product_id column exists in case table was created before the column was added
  try {
    db.exec(`
      ALTER TABLE price_checks
      ADD COLUMN product_id TEXT;
    `);
  } catch (error) {
    if (error.message.includes("duplicate column name")) {
      console.log("The 'product_id' column already exists.");
    } else {
      console.error("Error adding 'product_id' column:", error);
    }
  }
};

initDb(); // Call the function to initialize the database

// Function to add a new price check entry to the database
export const addPriceCheck = (email, targetPrice, productId) => {
  const stmt = db.prepare(`
    INSERT INTO price_checks (email, target_price, product_id)
    VALUES (?, ?, ?)
  `);
  return stmt.run(email, targetPrice, productId);
};


// Fetch the target price from the database using product_id
export const getTargetPrice = (productId) => {
    const stmt = db.prepare('SELECT target_price FROM price_checks WHERE product_id = ?');
    return stmt.get(productId);
};

// Add other database-related functions as needed
