import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector

# ==========================
# KONEKSI DATABASE
# ==========================
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="parkir",
            port=3306
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error Koneksi", f"Gagal terhubung ke database: {err}")
        return None

# ==========================
# PARKIR MASUK
# ==========================
def parkir_masuk():
    plat = entry_plat.get().strip().upper()
    jenis = combo_jenis.get().strip()

    if plat == "" or jenis == "":
        messagebox.showwarning("Input Error", "Plat dan Jenis Kendaraan harus diisi!")
        return

    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            sql = "INSERT INTO parkir (plat_nomor, jenis_kendaraan) VALUES (%s, %s)"
            cursor.execute(sql, (plat, jenis))
            db.commit()
            messagebox.showinfo("Sukses", f"Kendaraan {plat} berhasil diparkir!")
            
            entry_plat.delete(0, tk.END)
            entry_plat.focus()
            tampilkan_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Gagal menyimpan: {err}")
        finally:
            cursor.close()
            db.close()

# ==========================
# PARKIR KELUAR - FITUR LENGKAP
# ==========================
def parkir_keluar():
    selected = tabel.focus()
    if not selected:
        messagebox.showwarning("Pilih Data", "Silakan pilih kendaraan dari tabel yang akan keluar!")
        return

    values = tabel.item(selected, 'values')
    id_parkir = values[0]
    plat_nomor = values[1]
    jenis = values[2]
    waktu_masuk = values[3]
    
    # Hitung tarif berdasarkan jenis dan durasi
    tarif = hitung_tarif(jenis, waktu_masuk)
    
    # Konfirmasi parkir keluar
    confirm = messagebox.askyesno(
        "Konfirmasi Parkir Keluar",
        f"Plat Nomor: {plat_nomor}\n"
        f"Jenis: {jenis}\n"
        f"Waktu Masuk: {waktu_masuk}\n"
        f"Tarif: Rp {tarif:,}\n\n"
        f"Apakah yakin proses parkir keluar?"
    )
    
    if not confirm:
        return
    
    waktu_keluar = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            sql = "UPDATE parkir SET waktu_keluar=%s, tarif=%s, status='Selesai' WHERE id=%s AND status='Parkir'"
            cursor.execute(sql, (waktu_keluar, tarif, id_parkir))
            db.commit()
            
            if cursor.rowcount > 0:
                messagebox.showinfo(
                    "Sukses", 
                    f"✅ Parkir keluar berhasil!\n\n"
                    f"Plat: {plat_nomor}\n"
                    f"Jenis: {jenis}\n"
                    f"Waktu Masuk: {waktu_masuk}\n"
                    f"Waktu Keluar: {waktu_keluar.split()[1]}\n"
                    f"Total Tarif: Rp {tarif:,}"
                )
            else:
                messagebox.showwarning("Peringatan", "Kendaraan sudah keluar atau data tidak ditemukan!")
            
            tampilkan_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Gagal update: {err}")
        finally:
            cursor.close()
            db.close()

# ==========================
# HITUNG TARIF BERDASARKAN DURASI
# ==========================
def hitung_tarif(jenis, waktu_masuk_str):
    try:
        # Konversi string waktu_masuk ke datetime
        waktu_masuk = datetime.strptime(waktu_masuk_str, '%Y-%m-%d %H:%M:%S')
        waktu_sekarang = datetime.now()
        
        # Hitung selisih jam
        selisih = waktu_sekarang - waktu_masuk
        total_jam = max(1, selisih.seconds // 3600)  # Minimal 1 jam
        
        # Tarif per jam
        if jenis == "Mobil":
            tarif_per_jam = 5000
            tarif_minimum = 5000
        else:  # Motor
            tarif_per_jam = 2000
            tarif_minimum = 2000
        
        # Hitung total tarif
        tarif_total = tarif_per_jam * total_jam
        return max(tarif_total, tarif_minimum)
        
    except:
        # Jika error dalam perhitungan, gunakan tarif flat
        return 5000 if jenis == "Mobil" else 2000

# ==========================
# LAPORAN / SUMMARY
# ==========================
def tampilkan_laporan():
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            
            # Hitung total kendaraan hari ini
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_kendaraan,
                    SUM(CASE WHEN jenis_kendaraan='Mobil' THEN 1 ELSE 0 END) as total_mobil,
                    SUM(CASE WHEN jenis_kendaraan='Motor' THEN 1 ELSE 0 END) as total_motor,
                    SUM(CASE WHEN status='Parkir' THEN 1 ELSE 0 END) as masih_parkir,
                    SUM(CASE WHEN status='Selesai' THEN 1 ELSE 0 END) as sudah_keluar,
                    COALESCE(SUM(tarif), 0) as total_pendapatan
                FROM parkir 
                WHERE DATE(waktu_masuk) = CURDATE()
            """)
            
            result = cursor.fetchone()
            
            # Tampilkan dalam window terpisah
            laporan_window = tk.Toplevel(root)
            laporan_window.title("Laporan Harian")
            laporan_window.geometry("400x300")
            laporan_window.configure(bg='#f0f0f0')
            
            tk.Label(laporan_window, text="📊 LAPORAN PARKIR HARI INI", 
                    font=("Arial", 14, "bold"), bg='#f0f0f0').pack(pady=10)
            
            frame_laporan = tk.Frame(laporan_window, bg='#f0f0f0')
            frame_laporan.pack(pady=10, padx=20, fill='both')
            
            data_laporan = [
                ("Total Kendaraan", f"{result[0]:,}"),
                ("Mobil", f"{result[1]:,}"),
                ("Motor", f"{result[2]:,}"),
                ("Masih Parkir", f"{result[3]:,}"),
                ("Sudah Keluar", f"{result[4]:,}"),
                ("Total Pendapatan", f"Rp {result[5]:,}")
            ]
            
            for i, (label, value) in enumerate(data_laporan):
                tk.Label(frame_laporan, text=label, font=("Arial", 10), 
                        bg='#f0f0f0', width=20, anchor='w').grid(row=i, column=0, pady=5, sticky='w')
                tk.Label(frame_laporan, text=value, font=("Arial", 10, "bold"), 
                        bg='#f0f0f0', width=15, anchor='e').grid(row=i, column=1, pady=5, sticky='e')
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Gagal mengambil laporan: {err}")
        finally:
            cursor.close()
            db.close()

# ==========================
# TAMPILKAN DATA
# ==========================
def tampilkan_data():
    for row in tabel.get_children():
        tabel.delete(row)

    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT 
                    id,
                    plat_nomor,
                    jenis_kendaraan,
                    DATE_FORMAT(waktu_masuk, '%Y-%m-%d %H:%i:%S') as waktu_masuk,
                    COALESCE(DATE_FORMAT(waktu_keluar, '%Y-%m-%d %H:%i:%S'), '-') as waktu_keluar,
                    CASE 
                        WHEN tarif = 0 THEN '-'
                        ELSE CONCAT('Rp ', FORMAT(tarif, 0))
                    END as tarif,
                    status
                FROM parkir 
                ORDER BY waktu_masuk DESC
                LIMIT 100
            """)
            
            rows = cursor.fetchall()
            
            # Warna berdasarkan status
            for row in rows:
                item_id = tabel.insert("", "end", values=row)
                if row[6] == 'Parkir':
                    tabel.item(item_id, tags=('parkir',))
                else:
                    tabel.item(item_id, tags=('selesai',))
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

# ==========================
# GUI SETUP
# ==========================
root = tk.Tk()
root.title("Sistem Parkir Modern")
root.geometry("1000x650")
root.configure(bg='#2c3e50')

# Header
header_frame = tk.Frame(root, bg='#34495e', height=80)
header_frame.pack(fill='x')
header_frame.pack_propagate(False)

tk.Label(header_frame, text="SISTEM PARKIR MODERN", 
        font=("Arial", 24, "bold"), bg='#34495e', fg='white').pack(pady=20)

# Main Container
main_frame = tk.Frame(root, bg='#ecf0f1', padx=20, pady=20)
main_frame.pack(fill='both', expand=True)

# Left Frame - Input
left_frame = tk.Frame(main_frame, bg='#ecf0f1')
left_frame.grid(row=0, column=0, sticky='n', padx=(0, 20))

input_frame = tk.LabelFrame(left_frame, text="Input Kendaraan Masuk", 
                           font=("Arial", 12, "bold"), bg='white', padx=20, pady=20)
input_frame.pack(pady=(0, 20))

tk.Label(input_frame, text="Plat Nomor:", font=("Arial", 11), 
        bg='white').grid(row=0, column=0, pady=10, sticky='w')
entry_plat = tk.Entry(input_frame, font=("Arial", 11), width=20)
entry_plat.grid(row=0, column=1, pady=10, padx=(10, 0))
entry_plat.focus()

tk.Label(input_frame, text="Jenis Kendaraan:", font=("Arial", 11), 
        bg='white').grid(row=1, column=0, pady=10, sticky='w')
combo_jenis = ttk.Combobox(input_frame, values=["Motor", "Mobil"], 
                          font=("Arial", 11), width=18, state="readonly")
combo_jenis.grid(row=1, column=1, pady=10, padx=(10, 0))
combo_jenis.current(1)

btn_masuk = tk.Button(input_frame, text="PARKIR MASUK", command=parkir_masuk,
                     bg='#27ae60', fg='white', font=("Arial", 11, "bold"),
                     width=20, height=2, bd=0, cursor='hand2')
btn_masuk.grid(row=2, column=0, columnspan=2, pady=20)

# Tombol Aksi
action_frame = tk.Frame(left_frame, bg='#ecf0f1')
action_frame.pack()

btn_keluar = tk.Button(action_frame, text="PARKIR KELUAR", command=parkir_keluar,
                      bg='#e74c3c', fg='white', font=("Arial", 11, "bold"),
                      width=15, height=2, bd=0, cursor='hand2')
btn_keluar.pack(side='left', padx=(0, 10))

btn_laporan = tk.Button(action_frame, text="LAPORAN", command=tampilkan_laporan,
                       bg='#3498db', fg='white', font=("Arial", 11, "bold"),
                       width=15, height=2, bd=0, cursor='hand2')
btn_laporan.pack(side='left')

# Right Frame - Tabel
right_frame = tk.Frame(main_frame, bg='#ecf0f1')
right_frame.grid(row=0, column=1, sticky='nsew')
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(0, weight=1)

# Frame untuk tabel dengan judul
tabel_frame = tk.LabelFrame(right_frame, text="Data Parkir", 
                           font=("Arial", 12, "bold"), bg='white')
tabel_frame.pack(fill='both', expand=True)

# Tabel
kolom = ("ID", "Plat Nomor", "Jenis", "Waktu Masuk", "Waktu Keluar", "Tarif", "Status")
tabel = ttk.Treeview(tabel_frame, columns=kolom, show="headings", height=20)

# Style untuk tabel
style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview", 
                background="white",
                foreground="black",
                rowheight=25,
                fieldbackground="white")
style.map('Treeview', background=[('selected', '#3498db')])

# Konfigurasi kolom
column_widths = [50, 120, 80, 150, 150, 100, 80]
for i, col in enumerate(kolom):
    tabel.heading(col, text=col)
    tabel.column(col, width=column_widths[i], anchor="center")

# Tag untuk warna baris
tabel.tag_configure('parkir', background='#d5f4e6')  # Hijau muda untuk parkir
tabel.tag_configure('selesai', background='#f4d5d5')  # Merah muda untuk selesai

# Scrollbar
scrollbar = ttk.Scrollbar(tabel_frame, orient="vertical", command=tabel.yview)
tabel.configure(yscrollcommand=scrollbar.set)
tabel.pack(side='left', fill='both', expand=True)
scrollbar.pack(side='right', fill='y')

# Footer
footer_frame = tk.Frame(root, bg='#34495e', height=40)
footer_frame.pack(fill='x', side='bottom')
footer_frame.pack_propagate(False)

tk.Label(footer_frame, text="© 2024 Sistem Parkir Modern - Developed with Python & MySQL", 
        font=("Arial", 9), bg='#34495e', fg='white').pack(pady=10)

# Hotkey
root.bind('<Return>', lambda event: parkir_masuk())
root.bind('<F5>', lambda event: tampilkan_data())
root.bind('<F1>', lambda event: tampilkan_laporan())

# Load data awal
tampilkan_data()

# Jalankan aplikasi
root.mainloop()