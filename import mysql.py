import mysql.connector
import random
import string

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_parkir_uas"
)
cursor = db.cursor()


def generate_ticket():
    random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"TKT-{random_code}"


def check_in(id_kategori):
    id_tiket = generate_ticket()
    sql = "INSERT INTO Transaksi (id_tiket, id_kategori, waktu_masuk) VALUES (%s, %s, NOW())"
    val = (id_tiket, id_kategori)
    
    cursor.execute(sql, val)
    db.commit()
    print(f"--- KENDARAAN MASUK ---")
    print(f"ID Tiket : {id_tiket}")
    print(f"Kategori : {id_kategori} (1: Motor, 2: Mobil)")


def tampilkan_parkir():
    cursor.execute("SELECT id_tiket, waktu_masuk FROM Transaksi WHERE waktu_keluar IS NULL")
    hasil = cursor.fetchall()
    print("\n--- DAFTAR KENDARAAN DI LOKASI ---")
    for row in hasil:
        print(f"Tiket: {row[0]} | Masuk: {row[1]}")

def check_out(id_tiket):

    query_info = """
    SELECT t.waktu_masuk, k.tarif_per_jam 
    FROM Transaksi t 
    JOIN Kategori k ON t.id_kategori = k.id_kategori 
    WHERE t.id_tiket = %s
    """
    cursor.execute(query_info, (id_tiket,))
    data = cursor.fetchone()

    if data:
        waktu_masuk, tarif = data
        

        sql_update = """
        UPDATE Transaksi t
        JOIN Kategori k ON t.id_kategori = k.id_kategori
        SET t.waktu_keluar = NOW(),
            t.total_biaya = GREATEST(k.tarif_per_jam, CEIL(TIMESTAMPDIFF(SECOND, t.waktu_masuk, NOW()) / 3600) * k.tarif_per_jam)
        WHERE t.id_tiket = %s
        """
        cursor.execute(sql_update, (id_tiket,))
        db.commit()
        

        cursor.execute("SELECT total_biaya FROM Transaksi WHERE id_tiket = %s", (id_tiket,))
        biaya = cursor.fetchone()[0]
        
        print(f"--- KENDARAAN KELUAR ---")
        print(f"ID Tiket    : {id_tiket}")
        print(f"Total Biaya : Rp {biaya}")
    else:
        print("ID Tiket tidak ditemukan!")


check_in(2) 
tampilkan_parkir()
check_out('TKT-8U03E')