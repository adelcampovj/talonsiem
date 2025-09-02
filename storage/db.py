import sqlite3
from datetime import datetime

DB_NAME = "talonsiem.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            host TEXT,
            username TEXT,
            success BOOLEAN,
            raw TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS brute_force_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip TEXT,
            username TEXT,
            host TEXT,
            attempts INTEGER,
            window_seconds INTEGER
        )
    ''')

    conn.commit()
    conn.close()

def insert_attempt(timestamp, host, username, success, raw):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO login_attempts (timestamp, host, username, success, raw)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, host, username, success, raw))
    conn.commit()
    conn.close()
