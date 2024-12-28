from src.koneksi import koneksi_db
from tabulate import tabulate
from time import sleep
from datetime import datetime
import random

db, cursor = koneksi_db()

def dashboard_admin(data = {}):
    print("\nMenu Admin:")
    print("1. Menu Tiket")
    print("2. Menu Bus")
    print("3. Menu Rute")
    print("4. Logout")
    pilih = int(input("Masukkan menu 1-4: "))

    if pilih == 1:
        while True:
            print("\nMenu Tiket:")
            print("1. Lihat Informasi Tiket")
            print("2. Edit Informasi Tiket")
            print("3. Hapus Informasi Tiket")
            print("4. Kembali ke menu Admin")

            pil = int(input("Masukkan menu Tiket: "))

            if pil == 1:
                cursor.execute('''
                SELECT 
                    tiket.id AS tiket_id,
                    users.nama AS nama_user,
                    tiket.jumlah_tiket,
                    tiket.metode_pembayaran,
                    tiket.tanggal_pemesanan,
                    tiket.total_harga,
                    tiket.status
                FROM tiket
                JOIN users ON tiket.user_id = users.id
                ''')
                hasil = cursor.fetchall()

                if hasil:
                    print("History Tiket:")
                    # for row in hasil:
                    #     print(f'''
                    #     Tiket ID         : {row[0]}
                    #     Nama User        : {row[1]}
                    #     Jumlah Tiket     : {row[2]}
                    #     Metode Pembayaran: {row[3]}
                    #     Tanggal Pemesanan: {row[4]}
                    #     Total Harga      : {row[5]}
                    #     ''')
                    print(tabulate(hasil, headers=["Tiket ID", "Nama User", "Jumlah Tiket", "Metode Pembayaran", "Tanggal Pemesanan", "Total Harga", "Status"], tablefmt="github", numalign="center", stralign="center"))
                    
            elif pil == 2:
                cursor.execute('''
                SELECT 
                    tiket.id AS tiket_id, 
                    users.nama AS nama_user,
                    tiket.total_harga,
                    tiket.status
                FROM tiket
                JOIN users ON tiket.user_id = users.id
                ''')
                hasil = cursor.fetchall()

                if hasil:
                    print("\nTiket Sebelum Diperbarui:")
                    # for row in hasil:
                    #     print(f'''
                    #     Tiket ID         : {row[0]}
                    #     Nama User        : {row[1]}
                    #     Status           : {row[2]}
                    #     ''')
                    print(tabulate(hasil, headers=["Tiket ID", "Nama User", "Total Harga", "Status"], tablefmt="github", numalign="center", stralign="center"))

                else:
                    print("Tidak ada data tiket ditemukan.")
                    continue

                tiket_id = int(input("\nMasukkan ID tiket yang ingin diubah statusnya: "))

                status_baru = input("Masukkan status baru (Pending / Dibayar): ").capitalize()

                if status_baru not in ['Pending', 'Dibayar']:
                    print("Status tidak valid. Pilih 'Pending' atau 'Dibayar'.")
                    continue

                cursor.execute('''
                UPDATE tiket
                SET status = ?
                WHERE id = ?
                ''', (status_baru, tiket_id))

                db.commit()

                print(f"\nTiket dengan ID {tiket_id} telah diperbarui. Statusnya menjadi {status_baru}.")
            elif pil == 3:
                cursor.execute('''
                SELECT 
                    tiket.id AS tiket_id, 
                    users.nama AS nama_user, 
                    tiket.status, 
                    tiket.jumlah_tiket, 
                    tiket.total_harga, 
                    tiket.tanggal_pemesanan
                FROM tiket
                JOIN users ON tiket.user_id = users.id
                ''')
                hasil = cursor.fetchall()

                if hasil:
                    print("\nTiket Sebelum Dihapus:")
                    # for row in hasil:
                    #     print(f'''
                    #     Tiket ID         : {row[0]}
                    #     Nama User        : {row[1]}
                    #     Status           : {row[2]}
                    #     Jumlah Tiket     : {row[3]}
                    #     Total Harga      : {row[4]}
                    #     Tanggal Pemesanan: {row[5]}
                    #     ''')
                    print(tabulate(hasil, headers=["Tiket ID", "Nama User", "Status", "Jumlah Tiket", "Total Harga", "Tanggal Pemesanan"], tablefmt="github", numalign="center", stralign="center"))

                else:
                    print("Tidak ada data tiket ditemukan.")
                    continue

                tiket_id = int(input("\nMasukkan ID tiket yang ingin dihapus: "))

                cursor.execute('''
                DELETE FROM tiket
                WHERE id = ?
                ''', (tiket_id,))

                db.commit()

                print(f"\nTiket dengan ID {tiket_id} telah berhasil dihapus.")
            elif pil == 4:
                dashboard_admin(data)
    elif pilih == 2:
        while True:
            print("\nMenu Konfigurasi Bus:")
            print("1. Lihat Informasi Bus")
            print("2. Tambah Informasi Bus")
            print("3. Edit Informasi Bus")
            print("4. Hapus Informasi Bus")
            print("5. Kembali ke menu Admin")

            pil = int(input("Masukkan menu Konfigurasi: "))

            if pil == 1:
                cursor.execute("SELECT * FROM bus")
                hasil = cursor.fetchall()

                if hasil:
                    print(tabulate(hasil, headers=["ID", "Kapasitas", "Plat Bus", "Merek", "Warna Bus", "Fasilitas", "Bahan Bakar Bus"], tablefmt="github", numalign="center", stralign="center"))
            elif pil == 2:
                print("\nKamu memilih untuk menambahkan data Bus. Silahkan masukkan Informasi yang dibutuhkan dibawah ini.")
                while True:
                    kapasitas = int(input("Masukkan Kapasitas dari Bus yang akan dibuat: "))
                    # plat_bus = input("Masukkan Plat Bus yang ingin didaftarkan: ")
                    merek = input("Masukkan Merek Bus: ")
                    warna = input("Masukkan detail warna Bus: ")
                    fasilitas = input("Masukkan fasilitas apa saja yang dimiliki Bus: ")
                    bahan_bakar = input("Masukkan tipe bahan bakar Bus: ")

                    while not kapasitas or not merek or not warna or not fasilitas or not bahan_bakar:
                        print("Semua input wajib diisi!")
                        break
                    tanggal = f"{datetime.now().day}"
                    text = "NUSANTARA"
                    random_num = str(random.randint(000,999))
                    plat_bus = f"{random_num} - {text} - {tanggal}"
                    # print(plat_bus)
                    cursor.execute("SELECT plat_bus FROM bus WHERE plat_bus = ?", (plat_bus,))
                    rows = cursor.fetchall()
                    if rows:
                        print(f"Mohon maaf, plat bus sudah tersedia. Masukkan ulang data bus agar di re-generate")
                    else:
                        # print("Tidak ada data")
                        print("Kami ingin konfirmasi data berikut ini: ")
                        print("="*20)
                        print(f"Kapasitas Penumpang: {kapasitas}")
                        print(f"Nomor Plat Bus [HASIL GENERATE]: {plat_bus}")
                        print(f"Merek Bus: {merek}")
                        print(f"Warna Bus: {warna}")
                        print(f"Fasilitas Bus: {fasilitas}")
                        print(f"Bahan Bakar Bus: {bahan_bakar}")
                        print("="*20)
                        konfirm = input("Apakah data ini sudah sesuai? (Y/T): ")

                        if konfirm == "y".lower():
                            print("Baiklah data akan kami masukkan ke database")
                            sleep(3)
                            cursor.execute("INSERT INTO bus VALUES (null, ?, ?, ?, ?, ?, ?)", (kapasitas, plat_bus, merek, warna, fasilitas, bahan_bakar))
                            db.commit()
                            print("Sukses. Data telah ditambahkan ke database, untuk mengeceknya silahkan ke menu 1")
                            break
                        elif konfirm == "t".lower():
                            print("\nSilahkan masukkan data lagi dibawah ini: ")
                        
                    # print("Semua text terisi")
                    # break
            elif pil == 3:
                cursor.execute("SELECT * FROM bus")
                hasil = cursor.fetchall()

                if hasil:
                    print("Berikut ini adalah data sebelum di update: ")
                    print(tabulate(hasil, headers=["ID", "Kapasitas", "Plat Bus", "Merek", "Warna Bus", "Fasilitas", "Bahan Bakar Bus"], tablefmt="github", numalign="center", stralign="center"))
                    update = int(input("Masukkan ID Bus untuk mengupdate data: "))
                    bus_dipilih = next((buses for buses in hasil if buses[0] == update), None)
                    if bus_dipilih:
                        # print("Data sama")
                        while True:
                            print("="*15)
                            print(f"Kamu akan update data dari ID Bus: {bus_dipilih[0]}")
                            print(f"Kapasitas: {bus_dipilih[1]}")
                            print(f"Plat Bus: {bus_dipilih[2]}")
                            print(f"Merek: {bus_dipilih[3]}")
                            print(f"Warna Bus: {bus_dipilih[4]}")
                            print(f"Fasilitas Bus: {bus_dipilih[5]}")
                            print(f"Bahan Bakar Bus: {bus_dipilih[6]}")
                            print("="*15)
                            pilih_update = input("Pilih mau data apa yang diubah? (All/Kapasitas/Plat): ").capitalize()

                            if pilih_update not in ['All', 'Kapasitas', 'Plat']:
                                print("Input tidak valid, hanya tersedia All, Kapasitas, dan Plat")
                                continue
                            elif pilih_update == "All":
                                kapasitas_baru = int(input("Masukkan Kapasitas dari Bus yang akan dibuat: "))
                                merek_baru = input("Masukkan Merek Bus: ")
                                warna_baru = input("Masukkan detail warna Bus: ")
                                fasilitas_baru = input("Masukkan fasilitas apa saja yang dimiliki Bus: ")
                                bahan_bakar_baru = input("Masukkan tipe bahan bakar Bus: ")
                                while not kapasitas_baru or not merek_baru or not warna_baru or not fasilitas_baru or not bahan_bakar_baru:
                                    print("Semua input wajib diisi!")
                                    break
                                cursor.execute('''
                                                UPDATE bus
                                                SET kapasitas = ?, merek = ?, warna = ?, fasilitas = ?, bahan_bakar = ?
                                               WHERE id = ?
                                               ''', (kapasitas_baru, merek_baru, warna_baru, fasilitas_baru, bahan_bakar_baru, bus_dipilih[0]))
                                db.commit()
                                print(f"Berhasil terupdate semua data bus ID : {bus_dipilih[0]}")
                                break
                            elif pilih_update == "Kapasitas":
                                kapasitas_baru = int(input("Masukkan Kapasitas Penumpang Maximal di dalam Bus: "))
                                if kapasitas_baru == bus_dipilih[1]:
                                    print("Kapasitas masih sama seperti sebelumnya, tidak ada perubahan. Masukkan ulang (Jika tidak ada perubahan, ketik cancel).")
                                else:
                                    cursor.execute('''
                                                    UPDATE bus
                                                   SET kapasitas = ?
                                                   WHERE id = ?
                                                   ''', (kapasitas_baru, bus_dipilih[0]))
                                    db.commit()
                                    print("Berhasil mengubah kapasitas penumpang, cek ke menu 1 untuk detailnya.")
                                    break
                            elif pilih_update == "Plat":
                                while True:
                                    tanggal = f"{datetime.now().day}"
                                    text = "NUSANTARA"
                                    random_num = str(random.randint(000,999))
                                    plat_bus = f"{random_num} - {text} - {tanggal}"
                                    cursor.execute("SELECT plat_bus FROM bus WHERE plat_bus = ?", (plat_bus,))
                                    rows = cursor.fetchall()
                                    if rows:
                                        print(f"Mohon maaf, plat bus sudah tersedia. Akan di re-generate ulang")
                                        break
                                    else:
                                        print("="*15)
                                        print(f"Nomor Plat Bus [HASIL GENERATE]: {plat_bus}")
                                        print("="*15)
                                        cursor.execute("UPDATE bus SET plat_bus = ? WHERE id = ?", (plat_bus, bus_dipilih[0]))
                                        db.commit()
                                        print(f"Berhasil mengubah plat bus menjadi [{plat_bus}] untuk bus ID [{bus_dipilih[0]}]")
                                        break
                            elif pilih_update == "Cancel":
                                print("Kamu memilih kembali ke menu konfigurasi bus..")
                                sleep(5)
                                break

            elif pil == 4:
                cursor.execute("SELECT * FROM bus")
                hasil = cursor.fetchall()

                if hasil:
                    print("Data yang tersedia untuk dihapus: ")
                    print(tabulate(hasil, headers=["ID", "Kapasitas", "Plat Bus", "Merek", "Warna Bus", "Fasilitas", "Bahan Bakar Bus"], tablefmt="github", numalign="center", stralign="center"))
                    deleted = int(input("Masukkan ID Bus untuk menghapus data bus: "))
                    deleted_bus = next((bus_hapus for bus_hapus in hasil if bus_hapus[0] == deleted), None)
                    if deleted_bus:
                        cursor.execute("DELETE FROM bus WHERE id = ?", (deleted_bus[0],))
                        db.commit()
                        print(f"Berhasil menghapus data bus dengan ID {deleted}")
            elif pil == 5:
                dashboard_admin(data)
    elif pilih == 3:
        while True:
            print("\nMenu Rute: ")
            print("1. Tambahkan Rute")
            print("2. Lihat Informasi Rute")
            print("3. Tambahkan Schedules")
            print("4. Kembali ke menu Admin")
            pil = int(input("Masukkan Konfigurasi Rute: "))
            if pil == 1:
                cursor.execute("SELECT id FROM bus")
                found = cursor.fetchall()

                if found:
                    bus_id = int(input("Masukkan ID Bus: "))
                    bus_id = bus_id

                    from_loc = input("Masukkan Lokasi awal: ")
                    last_loc = input("Masukkan lokasi terakhir: ")
                    bill = float(input("Masukkan Harga Rute ini: "))

                    cursor.execute("INSERT INTO rute VALUES (null, ?, ?, ?, ?)", (bus_id, from_loc, last_loc, bill))
                    db.commit()
                    print("Rute berhasil ditambahkan.")
            elif pil == 2:
                cursor.execute("SELECT rute.id, bus.id, rute.'from', rute.'to', bill FROM rute JOIN bus ON bus.id = rute.bus_id")
                hasil = cursor.fetchall()

                if hasil:
                    print(tabulate(hasil, headers=["ID", "Bus ID", "Tujuan Awal", "Tujuan Akhir", "Harga Rute"], tablefmt="github", numalign="center", stralign="center"))
            elif pil == 3:
                # cursor.execute("SELECT id FROM bus")
                cursor.execute("SELECT rute.id, bus.id FROM rute JOIN bus ON bus.id = rute.bus_id")
                found_them = cursor.fetchall()

                if found_them:
                    bus_id = int(input("Pilih Bus ID: "))
                    rute_id = int(input("Pilih Rute ID: "))
                    print("Pastikan cek informasi Bus, dan Rute nya dimasing-masing menu!")

                    waktu_awal = input("Masukkan tanggal dan waktu Awal: (format: DD-MM-YYYY HH:MM:SS): ")
                    waktu_akhir = input("Masukkan tanggal dan waktu Akhir: (format: DD-MM-YYYY HH:MM:SS): ")
                    convert = datetime.strptime(waktu_awal, "%d-%m-%Y %H:%M:%S")
                    convert2 = datetime.strptime(waktu_akhir, "%d-%m-%Y %H:%M:%S")

                    raw_hasil = cursor.execute("INSERT INTO keberangkatan (bus_id, rute_id, waktu_awal, waktu_akhir) VALUES (?, ?, ?, ?)", (bus_id, rute_id, convert, convert2))
                    db.commit()
                    if raw_hasil:
                        cursor.execute("SELECT id, bus_id, rute_id, waktu_awal, waktu_akhir FROM keberangkatan")
                        hasil = cursor.fetchall()
                        if hasil:
                            print(tabulate(hasil, headers=["ID Keberangkatan", "Bus ID", "Rute ID", "Waktu Awal", "Waktu Akhir"], tablefmt="github", numalign="center", stralign="center"))
                            keberangkatan_id = int(input("Masukkan ID Keberangkatan: "))
                            tgl = input("Masukkan tanggal: (format: DD-MM-YYYY): ")
                            jam = input("Masukkan tanggal dan waktu Akhir: (format: HH:MM:SS): ")
                            conv = datetime.strptime(tgl, "%d-%m-%Y")
                            conv2 = datetime.strptime(jam, "%H:%M:%S")
                            total_seat = int(input("Masukkan Total Penumpang: "))

                            cursor.execute("INSERT INTO schedule (keberangkatan_id, tanggal, jam, total_seat, seat_available) VALUES (?, ?, ?, ?, ?)", (keberangkatan_id, conv, conv2, total_seat, total_seat))
                            db.commit()
                            print("Berhasil tersimpan kedalam database schedule.")
            elif pil == 4:
                dashboard_admin(data)
    elif pilih == 4:
        print("Kamu akan logout")
        print("Menghapus data query dan lainnya...")
        data.clear()
        sleep(10)
        print("Selamat tinggal.. Terima kasih ~")
        exit()       