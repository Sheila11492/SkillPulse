import sqlite3

DB_NAME = "skillpulse.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            activity_type TEXT NOT NULL,
            duration INTEGER NOT NULL,
            energy INTEGER NOT NULL,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_activity(activity):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO activities (date, activity_type, duration, energy, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (
        activity.date,
        activity.activity_type,
        activity.duration,
        activity.energy,
        activity.notes
    ))

    conn.commit()
    conn.close()


def get_activities():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, activity_type, duration, energy, notes
        FROM activities
        ORDER BY date DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows