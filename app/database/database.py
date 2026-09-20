import sqlite3


DATABASE_PATH = "authorizations.db"


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authorizations (
            submission_id TEXT PRIMARY KEY,
            patient_name TEXT NOT NULL,
            payer TEXT NOT NULL,
            procedure TEXT NOT NULL,
            status TEXT NOT NULL,
            submitted_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()