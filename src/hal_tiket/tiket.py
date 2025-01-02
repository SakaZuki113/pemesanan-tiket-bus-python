from src.koneksi import koneksi_db
import src.dashboard.halaman_user as user
from time import sleep
from src.auth.login import login
from tabulate import tabulate

def main_tiket(data_login = {}):
    if not data_login:
        print("Kamu belum login! silahkan login dulu dong...")
        print("Redirect 3 seconds...")
        sleep(3)
        login()
    else:
        id = data_login[0]['id']
        email = data_login[0]['email']
        name = data_login[0]['nama']
        role = data_login[0]['role']
        data = []
        data.append({
            'id': id,
            'email': email,
            'nama': name,
            'role': role
        })
        db, cursor = koneksi_db()
        while True:
            print("\nMenu pilihan:")
            print("1. Pesan Tiket")
            print("2. Lihat Informasi Tiket")
            print("3. Kembali ke halaman user")

            pil = int(input("Masukkan menu angka: "))

            if pil == 1:
                from src.hal_rute.rute import main_rute
                main_rute(data)
            elif pil == 2:
                try:
                    cursor.execute('''
                    SELECT 
                        tiket.id AS tiket_id,
                        users.nama AS nama_user,
                        tiket.jumlah_tiket,
                        tiket.metode_pembayaran,
                        tiket.tanggal_pemesanan,
                        tiket.total_harga,
                        tiket.status
                    FROM tiket
                    JOIN users ON tiket.user_id = users.id
                    WHERE tiket.user_id = ?
                    ''', (id, ))
                    hasil = cursor.fetchall()

                    if hasil:
                        print(tabulate(hasil, headers=["Tiket ID", "Nama User", "Jumlah Tiket", "Metode Pembayaran", "Tanggal Pemesanan", "Total Harga", "Status"], tablefmt="github", numalign="center", stralign="center"))
                        
                except Exception as err:
                    print(f"[WARNING - DANGER] ADA MASALAH NIH: {err}")
            elif pil == 3:
                user.dashboard(data)
                break