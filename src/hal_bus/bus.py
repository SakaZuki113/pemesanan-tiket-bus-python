from src.koneksi import koneksi_db
import random as rand
import datetime
import uuid
from time import sleep
from src.auth.login import login
import src.dashboard.halaman_user as user

def main_bus(data_login = {}):
    db, cursor = koneksi_db()
    if not data_login:
        print("Kamu belum login! silahkan login dulu dong...")
        print("Redirect 3 seconds...")
        sleep(3)
        login()
    else:
        print("\nMenu pilihan: ")
        print("1. Pesan Sekarang")
        print("2. Lihat history pemesanan")
        print("3. Kembali ke halaman user")

        pil = int(input("Masukkan menu pilihan: "))
        id = data_login[0]['id']
        email = data_login[0]['email']
        nama = data_login[0]['nama']
        role = data_login[0]['role']
        print(id)
        data = []
        data.append({
            'id': id,
            'email': email,
            'nama': nama,
            'role': role
        })

        if pil == 1:
            pass
        elif pil == 2: 
            cursor.execute('''
                SELECT * FROM pemesanan WHERE user_id = ?
            ''', (id, ))
            row = cursor.fetchone()
            print(row)
            db.close()
        elif pil == 3:
            print("Kamu memilih untuk kembali ke dashboard")
            sleep(5)
            print("Redirect Success\n")
            user.dashboard(data)

# from src.koneksi import koneksi_db
# import random as rand
# import datetime
# import uuid

# def pemesanan(UID, schedule_id, jumlah_kursi):
#     db, cursor = koneksi_db()
#     # Cek jadwal bus
#     cursor.execute("""
#         SELECT total_seat, seat_available, keberangkatan_id 
#         FROM schedule 
#         WHERE id = ?
#     """, (schedule_id,))
#     schedule = cursor.fetchone()

#     if not schedule:
#         print("Tidak ada schedules yang tersedia")

#     total_seat, seat_available, keberangkatan_id = schedule

#     # Validasi ketersediaan kursi
#     if jumlah_kursi > seat_available:
#         print(f"Kursi tidak cukup, Tersedia: {seat_available}")

#         # Ambil detail keberangkatan
#     cursor.execute("""
#         SELECT rute_id, bus_id, waktu_awal, waktu_akhir 
#         FROM keberangkatan 
#         WHERE id = ?
#     """, (keberangkatan_id,))
#     keberangkatan = cursor.fetchone()

#     if not keberangkatan:
#         print("Detail keberangkatan tidak ditemukan")

#     rute_id, bus_id, waktu_awal, waktu_akhir = keberangkatan

#     # Buat nomor pemesanan unik
#     uniq_oid = uuid.uuid4
#     nomor_pemesanan = rand.randrange(1,999)+uniq_oid

#     # Simpan pemesanan
#     cursor.execute("""
#         INSERT INTO pemesanan (
#             user_id, 
#             schedule_id, 
#             rute_id, 
#             bus_id, 
#             jumlah_kursi, 
#             status, 
#             nomor_pemesanan, 
#             tanggal_pemesanan,
#             total_harga,
#             metode_pembayaran
#         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, (
#         UID, 
#         schedule_id, 
#         rute_id, 
#         bus_id, 
#         jumlah_kursi, 
#         'Dikonfirmasi', 
#         nomor_pemesanan,
#         datetime.now()
#     ))

#         # Update ketersediaan kursi
#     cursor.execute("""
#         UPDATE schedule 
#         SET seat_available = seat_available - ? 
#         WHERE id = ?
#     """, (jumlah_kursi, schedule_id))

#         # Commit transaksi
#     db.commit()
#     db.close()
#     print(f"Pemesanan berhasil: {nomor_pemesanan}")

# def buat_tabel_pemesanan():
#     """Membuat tabel pemesanan jika belum ada"""
#     db, cursor = koneksi_db()
#     if not db or not cursor:
#         return

#     try:
#         cursor.execute('''
#         CREATE TABLE IF NOT EXISTS pemesanan (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER,
#             schedule_id INTEGER,
#             rute_id INTEGER,
#             bus_id INTEGER,
#             jumlah_kursi INTEGER,
#             status VARCHAR(50) DEFAULT 'Dikonfirmasi',
#             nomor_pemesanan VARCHAR(50) UNIQUE,
#             tanggal_pemesanan DATETIME,
#             FOREIGN KEY(user_id) REFERENCES users(id),
#             FOREIGN KEY(schedule_id) REFERENCES schedule(id),
#             FOREIGN KEY(rute_id) REFERENCES rute(id),
#             FOREIGN KEY(bus_id) REFERENCES bus(id)
#         )
#         ''')
#         db.commit()
#     except sqlite3.Error as e:
#         print(f"Error membuat tabel pemesanan: {e}")
#     finally:
#         if db:
#             db.close()
