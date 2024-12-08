from src.auth.login import login
from time import sleep

def dashboard(isiData = None):
    if not isiData:
        print("Kamu belum login! silahkan login dulu dong...")
        print("Redirect 3 seconds...")
        sleep(3)
        login()
    else:
        name = isiData[1]
        print(f"Selamat datang {name}!")


# if __name__ == "__main__":
#     print("Tidak bisa menjalankan function ini. Silahkan langsung ke file main.py")