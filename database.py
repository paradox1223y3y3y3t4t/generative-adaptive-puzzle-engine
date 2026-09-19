import sqlite3
from pathlib import Path


# This finds the main project folder.
BASE_DIR = Path(__file__).resolve().parent

# This is where our SQLite database file will be saved.
DATABASE_PATH = BASE_DIR / "database" / "puzzle_engine.db"


def get_connection():
    """
    Create and return a connection to the SQLite database.
    """
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """
    Create all required database tables.
    'IF NOT EXISTS' means the code is safe to run more than once.
    """
    connection = get_connection()
    cursor = connection.cursor()

    # Stores registration and login details.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    # Stores every generated puzzle.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS puzzles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            category TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            option1 TEXT,
            option2 TEXT,
            option3 TEXT,
            option4 TEXT,
            correct_answer TEXT NOT NULL,
            explanation TEXT NOT NULL
        )
    """)

    # Stores each answer submitted by a learner.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            puzzle_id INTEGER NOT NULL,
            selected_answer TEXT NOT NULL,
            correct INTEGER NOT NULL,
            response_time REAL NOT NULL,
            difficulty TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (puzzle_id) REFERENCES puzzles(id)
        )
    """)

    # Stores the learner's overall performance.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learner_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            total_attempts INTEGER DEFAULT 0,
            correct_answers INTEGER DEFAULT 0,
            wrong_answers INTEGER DEFAULT 0,
            accuracy REAL DEFAULT 0,
            average_response_time REAL DEFAULT 0,
            performance_score REAL DEFAULT 0,
            current_difficulty TEXT DEFAULT 'Easy',
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()

    print("Database and tables created successfully.")


# Run this file directly to create the database.
if __name__ == "__main__":
    initialize_database()