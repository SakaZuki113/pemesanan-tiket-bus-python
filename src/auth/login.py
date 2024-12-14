from src.koneksi import koneksi_db
from time import sleep
import getpass

data = {} #Initilisasi array
data['hasil'] = [] #Buat menyimpan array dalem bentuk object

def login_menu():
    print("="*10)
    print("Silahkan dipilih menu ini.")
    print("1. Login")
    print("2. Register")
    print("3. Keluar dari Aplikasi")
    pil = int(input("Silahkan pilih (1/2/3): "))
    return pil

def login():
    db, cursor = koneksi_db()

    while True:
        email = input("Masukkan Email terdaftar: ")
        password = getpass.getpass("Masukkan Password: ")

        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        query = cursor.fetchone()

        if query:
            print("Berhasil login, dialihkan ke halaman dashboard.")
            db.close()
            data['hasil'].append({
                'id': query[0],
                'nama': query[1],
                'email': query[2],
                'role': query[4]
            })
            from src.dashboard.halaman_user import dashboard
            dashboard(data['hasil'])
            return data['hasil']
        else:
            print("Email atau password salah, silahkan coba kembali!")

def register():
    db, cursor = koneksi_db()
    while True:
        nama = input("Masukkan nama lengkap: ")
        email = input("Masukkan Email: ")

        cursor.execute("SELECT * FROM users WHERE email = ?", (email, ))
        query = cursor.fetchone()

        if query:
            print("Email sudah ada, silahkan daftarkan email lain!")
        else:
            cursor.execute("INSERT INTO users (nama, email) VALUES (?, ?)", (nama, email))
            db.commit()
            password = input("Masukkan Password: ")
            cursor.execute("UPDATE users SET password = ? WHERE email = ?", (password, email))
            db.commit()
            print("Registrasi sukses!")
            db.close()
            return

def main():
    from src.dashboard.halaman_user import dashboard
    # hasil_query = None
    while True:
        pil = login_menu()

        if pil == 1:
            if login():
                pass
            else:
                login()
                print("Login gagal, silahkan coba lagi.")
            
            break

        elif pil == 2:
            print("Redirect to Register page")
            sleep(5)
            register()
            print("Silahkan login setelah registrasi")
            login()
            sleep(5)
            break
        elif pil == 3:
            print("Sayonara ~")
            sleep(2)
            exit()
        else:
            print("Not valid, cek pilihan yang tersedia.")

        break