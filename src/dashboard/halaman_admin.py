from src.auth.login import login
from time import sleep

def dashboard_admin(data = {}):
    if not data:
        print("Kamu belum login! silahkan login dulu dong...")
        print("Redirect 3 seconds...")
        sleep(3)
        login()
    else:
        name = data[0]['nama']
        role = data[0]['role']

        print(f"Selamat datang {name}!")
