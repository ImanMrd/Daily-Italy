import sqlite3

def migrate():
    conn = sqlite3.connect("backend/data/italian_vocab.db")
    c = conn.cursor()
    c.execute("PRAGMA table_info(users)")
    cols = [r[1] for r in c.fetchall()]
    print("Existing user columns:", cols)
    if "role" not in cols:
        c.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user'")
        print("Added role column to users.")
    c.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")
    conn.commit()
    print("Admin user role confirmed as 'admin'.")
    conn.close()

if __name__ == "__main__":
    migrate()
