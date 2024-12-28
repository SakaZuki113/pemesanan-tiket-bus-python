import src.dashboard.halaman_user as user
from time import sleep
from src.auth.login import login
from src.koneksi import koneksi_db
from tabulate import tabulate

def main_rute(data_login = {}):
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
            print("1. Lihat Informasi Rute")
            print("2. Kembali kehalaman user")

            pil = int(input("Masukkan menu angka: "))

            if pil == 1:
                try:
                    cursor.execute('''
                                    SELECT id, "from", "to", bill FROM rute
                                ''')
                    row = cursor.fetchall()
                    if row:
                        print(tabulate(row, headers=["ID", "Dari", "Tujuan", "Harga"], tablefmt="github", numalign="center", stralign="center"))
                        pilihan = int(input("Ingin memesan pada rute ID Berapa? "))
                        rute_dipilih = next((rute for rute in row if rute[0] == pilihan), None)

                        if rute_dipilih:
                            import src.hal_bus.bus as bus
                            print(f"Kamu memilih rute {rute_dipilih[1]} - {rute_dipilih[2]} - Rp {rute_dipilih[3]}")
                            print("Redirect ke halaman bus")
                            sleep(3)
                            data.append({
                                'rute_id': rute_dipilih
                            })
                            bus.main_bus(data)
                        else:
                            print("Not found")
                    else:
                        print("Tidak ada data rute yang tersedia.")
                except Exception as err:
                    print(f"WE HAVE ERROR JENDRAL, Error Message: {err}")

            elif pil == 2:
                print("Kamu memilih untuk kembali ke dashboard")
                sleep(5)
                print("Redirect success")
                user.dashboard(data)
                break