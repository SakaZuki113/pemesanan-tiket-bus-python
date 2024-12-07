from src.koneksi import koneksi_db
from time import sleep

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
        password = input("Masukkan Password: ")

        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        query = cursor.fetchone()

        if query:
            print("Berhasil login, dialihkan ke halaman dashboard.")
            db.close()
            return query
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
            print("Registrasi sukses, akan dialihkan ke halaman login!")
            db.close()
            return login()

def main():
    hasil_query = None
    while True:
        pil = login_menu()

        if pil == 1:
            if hasil_query is None:
                hasil_query = login()
                if hasil_query:
                    print("Redirect to Dashboard user")
                    sleep(5)
                else:
                    print("Login gagal, silahkan coba lagi.")
            else:
                print("Anda sudah login, redirect ke Dashboard user.")
                sleep(5)

            from src.dashboard.halaman_user import dashboard
            dashboard(hasil_query)
            break

        elif pil == 2:
            print("Redirect to Register page")
            sleep(5)
            register()
        else:
            print("Not valid, cek pilihan yang tersedia.")