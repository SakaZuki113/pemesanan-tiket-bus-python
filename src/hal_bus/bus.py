import src.dashboard.halaman_user as user
from time import sleep
from src.auth.login import login
from src.koneksi import koneksi_db
from tabulate import tabulate

def main_bus(data_login={}):
    if not data_login:
        print("Kamu belum login! Silahkan login dulu.")
        print("Redirect 3 seconds...")
        sleep(3)
        login()
    else:
        id_user = data_login[0]['id']
        name = data_login[0]['nama']
        role = data_login[0]['role']
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
            print("Tiket berhasil dipesan!")
            print("Redirecting to dashboard...")
            sleep(3)
            from src.dashboard.halaman_user import dashboard
            dashboard(data_login)



# import src.dashboard.halaman_user as user
# from time import sleep
# from src.auth.login import login
# from src.koneksi import koneksi_db
# from tabulate import tabulate

# def main_bus(data_login = {}):
#     if not data_login:
#         print("Kamu belum login! silahkan login dulu dong...")
#         print("Redirect 3 seconds...")
#         sleep(3)
#         login()
#     else:
#         id = data_login[0]['id']
#         email = data_login[0]['email']
#         name = data_login[0]['nama']
#         role = data_login[0]['role']
#         rute_id = data_login[0]['rute_id']
#         data = []
#         data.append({
#             'id': id,
#             'email': email,
#             'nama': name,
#             'role': role
#         })
#         if not rute_id:
#             print("Rute belum dipilih. Kembali ke menu Rute..")
#             sleep(3)
#             from src.hal_rute.rute import main_rute
#             main_rute(data)
#         elif rute_id:
#             print("\nMenu pilihan:")
#             print("1. Pesan Bus")
#             print("2. Kembali ke halaman user")

#             pil = int(input("Masukkan menu angka: "))

#             if pil == 1:
#                 cursor = koneksi_db()
#                 cursor.execute('''
#                                 SELECT * FROM bus
#                                 ''')
#                 row = cursor.fetchall()
#                 if row:
#                     print(tabulate(row, headers=["ID", "Kapasitas", "Plat Bus", "Merek Bus", "Warna Bus", "Fasilitas Bus", "Tipe Bahan Bakar Bus"], tablefmt="github", numalign="center", stralign="center"))
#                     pilihan = int(input("Ingin memesan ID Bus berapa? "))
#                     bus_pilihan = next((buses for buses in row if buses[0] == pilihan), None)

#                     if bus_pilihan:

#                         # print(f"Kamu telah memilih bus {bus_pilihan}")
                        
#             elif pil == 2:
#                 print("Kamu memilih untuk kembali ke dashboard")
#                 sleep(5)
#                 print("Redirect success")
#                 user.dashboard(data)
#         else:
#             print("Ada yang aneh... Kami logout-kan dulu ya")
#             data.clear()
#             sleep(3)
#             exit()