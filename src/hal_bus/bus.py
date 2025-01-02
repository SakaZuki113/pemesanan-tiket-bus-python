from time import sleep
from src.auth.login import login
from src.koneksi import koneksi_db
from tabulate import tabulate
from src.dashboard.halaman_user import dashboard

def main_bus(data_login={}):
    if not data_login:
        print("Kamu belum login! Silahkan login dulu.")
        print("Redirect 3 seconds...")
        sleep(3)
        login()
    else:
        id_user = data_login[0]['id']
        rute_id = data_login[1]['rute_id'][0]

        if not rute_id:
            print("Rute belum dipilih. Kembali ke menu Rute...")
            sleep(3)
            from src.hal_rute.rute import main_rute
            main_rute(data_login)
        else:
            db, cursor = koneksi_db()
            cursor.execute('''
                SELECT s.id, k.waktu_awal, k.waktu_akhir, s.tanggal, s.jam, 
                       s.total_seat, s.seat_available, b.plat_bus, b.merek, b.warna,
                       r.bill
                FROM schedule s
                JOIN keberangkatan k ON s.keberangkatan_id = k.id
                JOIN bus b ON k.bus_id = b.id
                JOIN rute r ON k.rute_id = r.id
                WHERE k.rute_id = ? AND s.seat_available > 0
            ''', (rute_id,))
            jadwal = cursor.fetchall()

            if not jadwal:
                print("Tidak ada jadwal yang tersedia untuk rute ini.")
                sleep(3)
                return

            print(tabulate(jadwal, headers=["ID", "Waktu Awal", "Waktu Akhir", "Tanggal", "Jam", 
                                            "Total Seat", "Seat Available", "Plat Bus", "Merek", "Warna", "Harga per Kursi"], 
                           tablefmt="github", numalign="center", stralign="center"))
            pilihan_jadwal = int(input("Pilih ID Jadwal yang ingin dipesan: "))
            jadwal_pilihan = next((j for j in jadwal if j[0] == pilihan_jadwal), None)

            if not jadwal_pilihan:
                print("Jadwal yang dipilih tidak valid.")
                sleep(3)
                return

            jumlah_tiket = int(input("Masukkan jumlah tiket yang ingin dipesan: "))
            if jumlah_tiket > jadwal_pilihan[6]:
                print("Jumlah tiket melebihi ketersediaan. Pemesanan dibatalkan.")
                sleep(3)
                return

            metode_pembayaran = input("Pilih metode pembayaran (Cash/Transfer Bank): ")
            if metode_pembayaran not in ['Cash', 'Transfer Bank']:
                print("Metode pembayaran tidak valid. Pemesanan dibatalkan.")
                sleep(3)
                return
            
            total_harga = jadwal_pilihan[10] * jumlah_tiket

            if metode_pembayaran == 'Transfer Bank':
                print("Silahkan transfer ke 0000221 bank BTCSA a.n Tiket Bus")
                upload = input("Silahkan upload bukti tf: ")

                if not upload:
                    cursor.execute('''
                        INSERT INTO tiket (user_id, schedule_id, metode_pembayaran, jumlah_tiket, total_harga)
                        VALUES (?, ?, ?, ?, ?)
                        ''', (id_user, pilihan_jadwal, metode_pembayaran, jumlah_tiket, total_harga))
                    cursor.execute('''
                        UPDATE schedule
                        SET seat_available = seat_available - ?
                        WHERE id = ?
                    ''', (jumlah_tiket, pilihan_jadwal))
                    db.commit()
                    print("Tiket berhasil dipesan, dan pembayaran masih pending. Jangan lupa untuk dibayar.")
                    print("Redirecting to dashboard...")
                    sleep(3)
                    dashboard(data_login)
                else:
                    cursor.execute('''
                        INSERT INTO tiket (user_id, schedule_id, metode_pembayaran, jumlah_tiket, total_harga, status)
                        VALUES (?, ?, ?, ?, ?)
                        ''', (id_user, pilihan_jadwal, metode_pembayaran, jumlah_tiket, total_harga, 'Dibayar'))
                    cursor.execute('''
                        UPDATE schedule
                        SET seat_available = seat_available - ?
                        WHERE id = ?
                    ''', (jumlah_tiket, pilihan_jadwal))
                    db.commit()
                    print("Tiket berhasil dipesan dan pembayaran sukses!")
                    print("Redirecting to dashboard...")
                    sleep(3)
                    dashboard(data_login)
            else:
                cursor.execute('''
                    INSERT INTO tiket (user_id, schedule_id, metode_pembayaran, jumlah_tiket, total_harga)
                    VALUES (?, ?, ?, ?, ?)
                ''', (id_user, pilihan_jadwal, metode_pembayaran, jumlah_tiket, total_harga))

                cursor.execute('''
                    UPDATE schedule
                    SET seat_available = seat_available - ?
                    WHERE id = ?
                ''', (jumlah_tiket, pilihan_jadwal))

                db.commit()
                print("Tiket berhasil dipesan dan jangan lupa dibayar melalui loket.")
                print("Redirecting to dashboard...")
                sleep(3)
                dashboard(data_login)