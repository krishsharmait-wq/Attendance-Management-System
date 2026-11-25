import sqlite3
from logger_setup import get_logger


class StorageHandler:
    """Owns the SQLite connection and table creation."""

    def __init__(self, db_name="attendance.db"):
        self.db_name = db_name
        self.log = get_logger()
        self.conn = sqlite3.connect(self.db_name)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._create_tables()

    def _create_tables(self):
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_no    TEXT UNIQUE NOT NULL,
                name       TEXT NOT NULL,
                course     TEXT,
                semester   INTEGER
            );
            CREATE TABLE IF NOT EXISTS attendance (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject    TEXT NOT NULL,
                date       TEXT NOT NULL,
                status     TEXT NOT NULL CHECK (status IN ('P', 'A')),
                UNIQUE (student_id, subject, date),
                FOREIGN KEY (student_id) REFERENCES students(student_id)
                    ON DELETE CASCADE
            );
            """
        )
        self.conn.commit()
        self.log.info("Tables ready in %s", self.db_name)

    def execute(self, query, params=()):
        cur = self.conn.execute(query, params)
        self.conn.commit()
        return cur

    def fetch_all(self, query, params=()):
        return self.conn.execute(query, params).fetchall()

    def close(self):
        self.conn.close()
