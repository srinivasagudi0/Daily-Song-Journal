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
            mood TEXT,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    existing_columns = [row[1] for row in c.execute("PRAGMA table_info(journals)")]
    if "mood" not in existing_columns:
        c.execute("ALTER TABLE journals ADD COLUMN mood TEXT")
    if "note" not in existing_columns:
        c.execute("ALTER TABLE journals ADD COLUMN note TEXT")
    conn.commit()
    conn.close()

def add_entry(song, artist, opinion, mood, note):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''
        INSERT INTO journals (song, artist, opinion, mood, note, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (song, artist, opinion, mood, note, sqlite3.datetime.datetime.now()))
    conn.commit()
    conn.close()

def get_entries():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''
        SELECT id, song, artist, opinion, mood, note, created_at
        FROM journals
        ORDER BY created_at DESC
    ''')
    entries = c.fetchall()
    conn.close()
    return entries

def delete_entry(entry_id):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    # No ID means the user wants a clean slate.
    if entry_id is None:
        c.execute("DELETE FROM journals")
    else:
        c.execute("DELETE FROM journals WHERE id = ?", (entry_id,))

    conn.commit()
    conn.close()

def edit_entry(entry_id, song, artist, opinion, mood, note):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(
        '''
        UPDATE journals
        SET song = ?, artist = ?, opinion = ?, mood = ?, note = ?
        WHERE id = ?
        ''',
        (song, artist, opinion, mood, note, entry_id)
    )
    conn.commit()
    conn.close()
