from koneksi import koneksi_db

def login(email, password):

    db, cursor = koneksi_db()  # Mendapatkan koneksi dan cursor

    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))

    user = cursor.fetchone()

    db.close()  # Menutup koneksi setelah selesai


    if user:

        print("Login berhasil!")

        return True

    else:

        print("Email atau password salah.")

        return False


if __name__ == "__main__":

    # Contoh penggunaan fungsi login

    email_input = input("Masukkan email: ")

    password_input = input("Masukkan password: ")

    login(email_input, password_input)
# def loginOrRegister():
#     print("Selamat datang, silahkan pilih register/login pada form dibawah ini.")
#     pil = int(input("Opsi tersedia\n1. Login\n2. Register"))

#     if pil == 1:
#         print("="*16)
#         email = input("Masukkan Email: ")
#         password = input("Masukkan Password: ")
#         print("="*16)
#         # Validation
#         cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
#         query = cursor.fetchone()
#         if query:
#             print("Berhasil login, akan dialihkan ke Home.")
#             cursor.execute("UPDATE users SET status_logged = 1 WHERE email = ?", (email, ))
#             db.commit()
#             return query[1]
#         else:
#             print("Email atau password salah.")
#             return None
#     elif pil == 2:
#         while True:
#             print("="*16)
#             nama = input("Masukkan Nama Lengkap: ")
#             email = input("Masukkan Email: ")
#             # password = input("Masukkan Password: ")
#             print("="*16)

#             cursor.execute("SELECT * FROM users WHERE email = ?", (email, ))
#             query = cursor.fetchone()
#             if query:
#                 print("Email sudah terdaftar. Gunakan email lain.")
#                 continue
#             else:
#                 password = input("Masukkan Password: ")
#                 cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (nama, email, password))
#                 db.commit()
#                 print("Akun berhasil dibuat.")
#                 loggedIn()
#                 break

# name = loginOrRegister()
# if name:
#     loggedIn(name)
# db.close()