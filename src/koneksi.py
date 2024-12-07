import sqlite3

def koneksi_db():
    db = sqlite3.connect("Booking_Bus.db")
    cursor = db.cursor()
    return db, cursor

def create_tables():
    db, cursor = koneksi_db()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama VARCHAR(255),
        email VARCHAR(255) UNIQUE,
        password VARCHAR(255),
        status_logged INTEGER DEFAULT 0 CHECK (status_logged IN (0, 1))
    )
    ''')
    db.commit()
    # CATATAN BUAT YANG KEBAGIAN DATABASE, BUAT CURSOR EXECUTE SETELAH COMMENT INI !
    
create_tables()