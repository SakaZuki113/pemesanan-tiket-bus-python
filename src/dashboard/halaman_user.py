from src.auth.login import login
from time import sleep

def dashboard(isiData = {}):
    if not isiData:
        print("Kamu belum login! silahkan login dulu dong...")
        print("Redirect 3 seconds...")
        sleep(3)
        login()
    else:
        name = isiData[0]['nama']
        print(f"Selamat datang {name}!")
