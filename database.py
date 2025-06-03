import sqlite3
from datetime import datetime
import os

DB_NAME = 'bot_database.db'

def init_db():
    is_new_db = not os.path.exists(DB_NAME)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")
    
    if is_new_db:
        print("Creating new database with tables...")
    
    # Create users table to store user information for public comments
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        username TEXT,
        last_name TEXT,
        language_code TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create messages table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    # Create scheduled_posts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scheduled_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER NOT NULL,
        channel_id TEXT NOT NULL,
        scheduled_time TIMESTAMP NOT NULL,
        posted BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
    )
    ''')
    

    
    # Create indexes for better performance
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn



# Initialize database and run migrations
init_db()
