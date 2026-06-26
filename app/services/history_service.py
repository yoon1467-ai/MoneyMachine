import sqlite3
from pathlib import Path
from datetime import datetime


DB_PATH = Path("data") / "history.db"


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS content_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT NOT NULL,
        content_type TEXT NOT NULL,
        file_path TEXT,
        seo_score INTEGER,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def add_history(keyword, content_type, file_path="", seo_score=None):
    init_db()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO content_history (
        keyword,
        content_type,
        file_path,
        seo_score,
        created_at
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        keyword,
        content_type,
        str(file_path),
        seo_score,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_written_keywords():
    init_db()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT DISTINCT keyword
    FROM content_history
    WHERE content_type = 'blog'
    """)

    rows = cur.fetchall()
    conn.close()

    return {row[0] for row in rows if row[0]}


def get_recent_history(limit=50):
    init_db()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT
        keyword,
        content_type,
        file_path,
        seo_score,
        created_at
    FROM content_history
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    return rows


def clear_history():
    init_db()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DELETE FROM content_history")

    conn.commit()
    conn.close()
