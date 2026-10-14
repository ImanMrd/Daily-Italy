import sqlite3
import os

def migrate():
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "italian_vocab.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    def add_col_if_missing(table, col, defn):
        cursor.execute(f"PRAGMA table_info({table})")
        cols = [row[1] for row in cursor.fetchall()]
        if col not in cols:
            print(f"Adding {col} to {table}...")
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {defn}")
        else:
            print(f"{table}.{col} already exists.")

    add_col_if_missing("exercises", "chapter_id", "INTEGER")
    add_col_if_missing("words", "chapter_id", "INTEGER")
    add_col_if_missing("users", "unlocked_levels", "VARCHAR(100) DEFAULT 'A1'")

    conn.commit()
    conn.close()
    print("Migration finished!")

if __name__ == "__main__":
    migrate()
