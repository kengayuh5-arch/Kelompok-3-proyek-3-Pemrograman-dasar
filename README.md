# Sistem Pengelolaan Peminjaman Peralatan Laboratorium

Aplikasi berbasis Command-Line Interface (CLI) untuk mengelola inventaris peralatan laboratorium, data mahasiswa, serta transaksi peminjaman dan pengembalian alat. Proyek ini dikembangkan menggunakan **Python** dengan paradigma **Object-Oriented Programming (OOP)**, arsitektur berlapis (*Layered Architecture*), dan penyimpanan database relasional **MariaDB / MySQL**.

---

## Fitur Utama

* **Manajemen Data Master (CRUD):**
  * **Kategori Alat:** Menambah, mencari, dan menampilkan daftar kategori peralatan.
  * **Data Mahasiswa:** Mendaftarkan, mengubah, menghapus, mencari (berdasarkan NIM/nama), dan menampilkan daftar mahasiswa peminjam.
  * **Inventaris Alat:** Mengelola data peralatan beserta kondisi stok (*Stok Baik*, *Rusak Ringan*, dan *Rusak Berat*), penambahan stok baru, serta pencatatan perbaikan alat rusak.
* **Transaksi Peminjaman Multi-Item:**
  * Mendukung peminjaman beberapa jenis alat dalam satu kode transaksi (`TRX001`, `TRX002`, dst.) dengan batas maksimal **2 transaksi aktif** per mahasiswa dan masa pinjam standar **7 hari**.
  * Menggunakan mekanisme transaksi database atomik (`COMMIT` dan `ROLLBACK`) sehingga perubahan pada tabel `transaksi`, `detail_peminjaman`, dan pengurangan stok di tabel `alat` berjalan serentak.
* **Pengembalian Parsial & Penuh:**
  * Mendukung pengembalian alat per item beserta pencatatan kondisi pengembalian (`baik`, `rusak ringan`, `rusak berat`) yang otomatis memperbarui rincian stok alat terkait.
* **Laporan & Statistik Laboratorium:**
  * Ringkasan total inventaris dan kondisi stok.
  * Daftar peralatan yang sedang dipinjam.
  * Deteksi transaksi yang melewati batas waktu pengembalian (keterlambatan).
  * Statistik peminjaman dan peringkat alat paling sering dipinjam.
  * Riwayat peminjaman per mahasiswa.
* **Audit Trail (Log Aktivitas):**
  * Mencatat setiap aktivitas penting sistem secara otomatis beserta stempel waktu ke dalam database.

---

## Arsitektur & Struktur Folder

```text
├── database.py                  # Konfigurasi & pabrik koneksi MariaDB (PyMySQL + DictCursor)
├── db_lab.sql                   # Skema struktur tabel & relasi database db_lab
├── main.py                      # Entry point utama & perakitan Dependency Injection
├── README.md                    # Dokumentasi proyek
├── models/                      # Lapisan Entitas Domain (OOP)
│   ├── alat.py
│   ├── detail_peminjaman.py
│   ├── kategori_alat.py
│   ├── log_aktivitas.py
│   ├── mahasiswa.py
│   └── transaksi.py
├── repositories/                # Lapisan Akses Data (Query SQL & Mapping Objek)
│   ├── alat_repo.py
│   ├── detail_repo.py
│   ├── kategori_repo.py
│   ├── log_repo.py
│   ├── mahasiswa_repo.py
│   └── transaksi_repo.py
├── services/                    # Lapisan Logika Bisnis & Pelaporan
│   ├── laporan.py
│   └── sistem_lab.py
└── ui/                          # Lapisan Antarmuka Pengguna (CLI)
    └── menu_app.py
```

---

## Prasyarat & Instalasi

1. **Perangkat Lunak yang Dibutuhkan:**
   * Python 3.8 atau lebih baru
   * XAMPP (Apache & MySQL / MariaDB)
   * Library Python `pymysql`

2. **Instalasi Library Python:**
   Jalankan perintah berikut pada terminal:
   ```bash
   pip install pymysql
   ```

3. **Pengaturan Database (XAMPP & phpMyAdmin):**
   * Jalankan modul **Apache** dan **MySQL** pada XAMPP Control Panel.
   * Buka `http://localhost/phpmyadmin`, lalu buat database baru dengan nama **`db_lab`**.
   * Pilih database `db_lab`, buka tab **Import**, lalu pilih file `db_lab.sql` (atau file dump SQL proyek) dan klik **Import / Go**.

4. **Konfigurasi Koneksi di `database.py`:**
   Pastikan parameter koneksi pada atribut `self.config` di dalam file `database.py` sudah sesuai dengan pengaturan MySQL/MariaDB di XAMPP lokal Anda:
   ```python
   self.config = {
       "host": "127.0.0.1",
       "port": 3307,  # Sesuaikan dengan laptop masing-masing
       "user": "root",
       "password": "",
       "database": "db_lab"
   }
   ```

5. **Menjalankan Aplikasi:**
   ```bash
   python main.py
   ```

---

## Pembagian Tugas Kelompok

| Nama Anggota | File yang Dikerjakan |
| :--- | :--- |
| **Bintang Fajar Khoiru Rizal** | `sistem_lab.py`, `transaksi.py`, `detail_peminjaman.py`, `alat_repository.py`, `log_repository.py`, `transaksi_repository.py` |
| **Afrizal Affandi Ahmad** | `alat.py`, `kategori_alat.py`, `mahasiswa.py`, `log_aktivitas.py`, `detail_repository.py`, `mahasiswa_repository.py` |
| **Ken Gayuh Nusa Islami** | `menu_app.py`, `laporan.py`, `main.py`, `database.py`, `kategori_repository.py`, `README.md` |