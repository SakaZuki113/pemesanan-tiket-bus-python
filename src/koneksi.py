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
        role VARCHAR(10) DEFAULT 'Member' CHECK (role IN ('Member', 'Admin'))
    )
    ''')
    # CATATAN BUAT YANG KEBAGIAN DATABASE, BUAT CURSOR EXECUTE SETELAH COMMENT INI !

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kapasitas INTEGER,
        plat_bus VARCHAR(20) UNIQUE NOT NULL,
        merek VARCHAR(50),
        warna VARCHAR(30),
        fasilitas TEXT,
        bahan_bakar TEXT
    )                        
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rute (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bus_id INTEGER,
        "from" TEXT,
        "to" TEXT,
        bill REAL,
        FOREIGN KEY(bus_id) REFERENCES bus(id)
    )
    ''')

    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS keberangkatan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bus_id INTEGER,
        rute_id INTEGER,
        waktu_awal DATETIME,
        waktu_akhir DATETIME,
        keterlambatan INTEGER DEFAULT 0,
        status VARCHAR(50) DEFAULT 'Dijadwalkan',
        FOREIGN KEY(bus_id) REFERENCES bus(id),
        FOREIGN KEY(rute_id) REFERENCES rute(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keberangkatan_id INTEGER,
        tanggal DATE,
        jam DATETIME,
        total_seat INTEGER,
        seat_available INTEGER,
        FOREIGN KEY(keberangkatan_id) REFERENCES keberangkatan(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tiket (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        schedule_id INTEGER,
        metode_pembayaran VARCHAR(20) CHECK (metode_pembayaran IN ('Cash', 'Transfer Bank')),
        jumlah_tiket INTEGER,
        total_harga REAL,
        tanggal_pemesanan DATETIME DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(20) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Dibayar')),
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(schedule_id) REFERENCES schedule(id)
    )
    ''')

    db.commit()
create_tables()
