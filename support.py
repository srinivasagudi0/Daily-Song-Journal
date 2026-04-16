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
            reminds_me_of TEXT,
            is_favorite INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    existing_columns = [row[1] for row in c.execute("PRAGMA table_info(journals)")]
    if "mood" not in existing_columns:
        c.execute("ALTER TABLE journals ADD COLUMN mood TEXT")
    if "note" not in existing_columns:
        c.execute("ALTER TABLE journals ADD COLUMN note TEXT")
    if "reminds_me_of" not in existing_columns:
        c.execute("ALTER TABLE journals ADD COLUMN reminds_me_of TEXT")
    if "is_favorite" not in existing_columns:
        c.execute("ALTER TABLE journals ADD COLUMN is_favorite INTEGER DEFAULT 0")
        if "is_faviorite" in existing_columns:
            c.execute("UPDATE journals SET is_favorite = COALESCE(is_faviorite, 0)")
    conn.commit()
    conn.close()

def add_entry(song, artist, opinion, mood, note, reminds_me_of, is_favorite):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''
        INSERT INTO journals (song, artist, opinion, mood, note, reminds_me_of, is_favorite, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (song, artist, opinion, mood, note, reminds_me_of, is_favorite, sqlite3.datetime.datetime.now()))
    conn.commit()
    conn.close()

def get_entries():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''
        SELECT id, song, artist, opinion, mood, note, reminds_me_of, is_favorite, created_at
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

def edit_entry(entry_id, song, artist, opinion, mood, note, reminds_me_of, is_favorite):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(
        '''
        UPDATE journals
        SET song = ?, artist = ?, opinion = ?, mood = ?, note = ?, reminds_me_of = ?, is_favorite = ?
        WHERE id = ?
        ''',
        (song, artist, opinion, mood, note, reminds_me_of, is_favorite, entry_id)
    )
    conn.commit()
    conn.close()
