from src.auth.login import loginOrRegister
from src.hal_tiket.tiket import buy_ticket
def loggedIn(name):

    print(f"Selamat datang {name}! silahkan pilih menu dibawah ini")

    print("Silahkan pilih menu yang tersedia: ")
    print("1. Beli Tiket")
    print("2. Cek Jadwal Bus")
    print("3. Cek Tipe Bus")

    pil = int(input("Silahkan Pilih Menu dengan angka: "))

    if pil == 1:
        buy_ticket()

    