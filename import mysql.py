import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",      
        password="",      
        database="sistem_parkir"
    )

def parkir_masuk():
    plat = entry_plat.get()
    jenis = combo_jenis.get()
    waktu_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if plat == "" or jenis == "":
        messagebox.showwarning("Input Error", "Isi plat dan jenis kendaraan!")
        return

    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "INSERT INTO riwayat_parkir (plat_nomor, jenis_kendaraan, waktu_masuk) VALUES (%s, %s, %s)"
        cursor.execute(sql, (plat, jenis, waktu_masuk))
        db.commit()
        db.close()
        
        tampilkan_data()
        entry_plat.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Gagal simpan data: {e}")

def parkir_keluar():
    selected = tabel.focus()
    if not selected:
        messagebox.showwarning("Pilih Data", "Pilih kendaraan yang akan keluar!")
        return


    item = tabel.item(selected)
    record_id = item['values'][0]
    waktu_keluar = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

    tarif = 5000 

    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "UPDATE riwayat_parkir SET waktu_keluar = %s, tarif = %s WHERE id = %s"
        cursor.execute(sql, (waktu_keluar, tarif, record_id))
        db.commit()
        db.close()
        
        tampilkan_data()
    except Exception as e:
        messagebox.showerror("Error", f"Gagal update data: {e}")

def tampilkan_data():
    for row in tabel.get_children():
        tabel.delete(row)

    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM riwayat_parkir ORDER BY id DESC")
        res = cursor.fetchall()
        
        for row in res:
            tabel.insert("", "end", values=row)
        db.close()
    except Exception as e:
        print(f"Error loading data: {e}")


root = tk.Tk()
root.title("Sistem Parkir MariaDB")
root.geometry("700x450")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Plat Nomor").grid(row=0, column=0)
entry_plat = tk.Entry(frame)
entry_plat.grid(row=0, column=1)

tk.Label(frame, text="Jenis Kendaraan").grid(row=1, column=0)
combo_jenis = ttk.Combobox(frame, values=["Motor", "Mobil"])
combo_jenis.grid(row=1, column=1)

tk.Button(frame, text="Parkir Masuk", command=parkir_masuk).grid(row=2, column=0, columnspan=2, pady=5)

kolom = ("ID", "Plat", "Jenis", "Masuk", "Keluar", "Tarif")
tabel = ttk.Treeview(root, columns=kolom, show="headings")

for k in kolom:
    tabel.heading(k, text=k)
    tabel.column(k, width=100)

tabel.pack(pady=10)

tk.Button(root, text="Parkir Keluar (Selesai)", command=parkir_keluar).pack(pady=5)


tampilkan_data()

root.mainloop()