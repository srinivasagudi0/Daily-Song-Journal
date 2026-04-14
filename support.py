import sqlite3

db = "song_journal.db"

def init_db():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS journals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            song TEXT NOT NULL,
            artist TEXT NOT NULL,
            opinion TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_entry(song, artist, opinion):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''
        INSERT INTO journals (song, artist, opinion, created_at)
        VALUES (?, ?, ?, ?)
    ''', (song, artist, opinion, sqlite3.datetime.datetime.now()))
    conn.commit()
    conn.close()

