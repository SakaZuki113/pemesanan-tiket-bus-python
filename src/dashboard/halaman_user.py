from src.auth.login import login
from time import sleep

def dashboard(isiData = {}):
    if not isiData:
        print("Kamu belum login! silahkan login dulu dong...")
        print("Redirect 3 seconds...")
        sleep(3)
        login()
    else:
        email = isiData[0]['email']
        name = isiData[0]['nama']
        role = isiData[0]['role']
        data = []
        data.append({
            'email': email,
            'nama': name,
            'role': role
        })
        if role == "Admin":
            print("Kamu Role Admin, akan di redirect ke halaman Admin dalam 2 detik..")
            sleep(2)
            import src.dashboard.halaman_admin as admin
            admin.dashboard_admin(data)
        else:
            print(f"Selamat datang {name}!")
            print("\nSilahkan pilih menu ini: ")
            print("1. Menu Ticket")
            print("2. Menu Bus")
            print("3. Menu Rute")
            print("4. Logout")
            pil = int(input("Masukkan angka untuk memilih menu: "))

            if pil == 1:
                import src.hal_tiket.tiket as tiket
                tiket.main_tiket(data)
            elif pil == 2:
                pass
            elif pil == 3:
                pass
            elif pil == 4:
                print("Kamu akan logout")
                print("Menghapus data query dan lainnya...")
                data.clear()
                sleep(10)
                print("Selamat tinggal.. Terima kasih ~")
                exit()