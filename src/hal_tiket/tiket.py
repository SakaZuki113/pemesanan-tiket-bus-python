import src.dashboard.halaman_user as user
from time import sleep
from src.auth.login import login

def main_tiket(data_login = {}):
    if not data_login:
        print("Kamu belum login! silahkan login dulu dong...")
        print("Redirect 3 seconds...")
        sleep(3)
        login()
    else:
        print("\nMenu pilihan:")
        print("1. Lihat Informasi Tiket")
        print("2. Lihat Informasi Pembayaran")
        print("3. Kembali kehalaman user")

        pil = int(input("Masukkan menu angka: "))

        if pil == 1:
            pass
        elif pil == 2:
            pass
        elif pil == 3:
            email = data_login[0]['email']
            name = data_login[0]['nama']
            role = data_login[0]['role']
            data = []
            data.append({
                'email': email,
                'nama': name,
                'role': role
            })
            print("Kamu memilih untuk kembali ke dashboard")
            sleep(5)
            print("Redirect success")
            user.dashboard(data)