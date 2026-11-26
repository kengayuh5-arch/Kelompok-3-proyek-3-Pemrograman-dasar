import os
from services.sistem_lab import SistemLab
from reports.laporan import Laporan

class MenuApp:
    def __init__(self, sistem, laporan):
        if type(sistem) != SistemLab:
            raise ValueError("sistem harus objek SistemLab")
        if type(laporan) != Laporan:
            raise ValueError("laporan harus objek Laporan")
        
        self.sistem = sistem
        self.laporan = laporan
    
    def inputValid(self, prompt):
        nilai = input(prompt).strip()
        if not nilai:
            raise ValueError("Input tidak boleh kosong")
        return nilai
    
    def inputAngka(self, prompt):
        nilai = input(prompt).strip()
        try:
            return int(nilai)
        except ValueError:
            raise ValueError(f"'{nilai}' bukan angka yang valid")
    
    def pause(self):
        input("\n(Tekan Enter untuk lanjut)")
    
    def jalankan(self):
        print("\n" + "=" * 40)
        print("  Sistem pengelolaan peminjaman alat")
        print("=" * 40)
        
        while True:
            try:
                self.tampilkanMenu()
                pilihan = input("Silahkan pilih menu program (0-7): ").strip()
                
                if pilihan == "1": self.menuMahasiswa()
                elif pilihan == "2": self.menuAlat()
                elif pilihan == "3": self.menuTransaksi()
                elif pilihan == "4": self.menuPengembalian()
                elif pilihan == "5": self.menuLaporan()
                elif pilihan == "6": self.menuLog()
                elif pilihan == "7": self.menuEksporLaporan()
                elif pilihan == "0":
                    print("\nProgram selesai. Terima kasih")
                    break
                else:
                    print("\nPilihan tidak valid. Silahkan pilih kembali")
            
            except Exception as e:
                print(f"\nError tak terduga: {e}")
                self.pause()
    
    def tampilkanMenu(self):
        print("\n" + "=" * 40)
        print("===== Menu Utama =====")
        print("=" * 40)
        print("1. Kelola data mahasiswa")
        print("2. Kelola data alat")
        print("3. Buat transaksi peminjaman")
        print("4. Proses pengembalian alat")
        print("5. Laporan dan statistik")
        print("6. Lihat log aktivitas")
        print("7. Ekspor Laporan ke File")
        print("0. Keluar")
        print("-" * 40)

    def menuMahasiswa(self):
        while True:
            print("\n===== Kelola Mahasiswa =====")
            print("1. Tambah mahasiswa")
            print("2. Tampilkan semua mahasiswa")
            print("3. Cari mahasiswa")
            print("4. Edit mahasiswa")
            print("5. Hapus mahasiswa")
            print("6. Lihat riwayat mahasiswa")
            print("0. Kembali ke menu utama")
            
            pilih = input("Silahkan pilih menu (0-6): ").strip()
            
            if pilih == "1": self.tambahMahasiswa()
            elif pilih == "2": self.tampilkanSemuaMahasiswa()
            elif pilih == "3": self.cariMahasiswa()
            elif pilih == "4": self.editMahasiswa()
            elif pilih == "5": self.hapusMahasiswa()
            elif pilih == "6": self.lihatRiwayatMahasiswa()
            elif pilih == "0": break
            else: print("Pilihan tidak valid. silahkan pilih kembali")
    
    def tambahMahasiswa(self):
        print("\n=== Tambah Mahasiswa ===")
        try:
            nim = self.inputValid("NIM: ")
            nama = self.inputValid("Nama: ")
            no_hp = self.inputValid("No HP: ")
            
            mhs = self.sistem.tambahMahasiswa(nim, nama, no_hp)
            print(f"\nMahasiswa {mhs.getNama()} berhasil ditambahkan")
        except ValueError as e:
            print(f"\nError: {e}")
        self.pause()
    
    def tampilkanSemuaMahasiswa(self):
        print("\n===== Daftar Mahasiswa =====")
        daftar_mhs = self.sistem.ambil_semua_mahasiswa()
        
        if len(daftar_mhs) == 0:
            print("(Belum ada mahasiswa)")
            self.pause()
            return
        
        print(f"{'NIM':<12} | {'NAMA':<20} | {'NO HP':<15}")
        print("-" * 55)
        for mhs in daftar_mhs:
            print(
                f"{mhs.getNim():<12} | "
                f"{mhs.getNama():<20} | "
                f"{mhs.getNoHp():<15}"
            )
        print(f"Total: {len(daftar_mhs)} mahasiswa")
        self.pause()
    
    def cariMahasiswa(self):
        print("\n=== Cari Mahasiswa ===")
        try:
            keyword = self.inputValid("Masukkan NIM/nama: ")
            hasil = self.sistem.cariMahasiswa(keyword)
            
            if len(hasil) == 0:
                print(f"Tidak ada mahasiswa yang cocok dengan '{keyword}'")
            else:
                print(f"\nDitemukan {len(hasil)} mahasiswa:")
                for mhs in hasil:
                    print(f"  {mhs.getDetail()}")
        except ValueError as e:
            print(f"Error: {e}")
        self.pause()
    
    def editMahasiswa(self):
        print("\n=== Edit Mahasiswa ===")
        try:
            nim = self.inputValid("NIM yang mau diedit: ")
            mhs = self.sistem.getMahasiswa(nim)
            
            if not mhs:
                raise ValueError(f"Mahasiswa dengan NIM {nim} tidak ditemukan")
                
            print(f"Data saat ini: {mhs.getDetail()}")
            print("(Kosongkan kalau tidak mau ubah)")
            
            nama = input("Nama baru: ").strip()
            no_hp = input("No HP baru: ").strip()
            
            self.sistem.editMahasiswa(nim, nama, no_hp)
            print("Data mahasiswa berhasil diperbarui")
        except ValueError as e:
            print(f"Error: {e}")
        self.pause()
    
    def hapusMahasiswa(self):
        print("\n=== Hapus Mahasiswa ===")
        try:
            nim = self.inputValid("NIM yang mau dihapus: ")
            mhs = self.sistem.getMahasiswa(nim)
            
            if not mhs:
                raise ValueError(f"Mahasiswa dengan NIM {nim} tidak ditemukan")
                
            konfirmasi = input(f"Yakin hapus {mhs.getNama()}? (y/n): ").strip().lower()
            if konfirmasi == "y":
                self.sistem.hapusMahasiswa(nim)
                print("Mahasiswa berhasil dihapus")
            else:
                print("(Batal)")
        except ValueError as e:
            print(f"Error: {e}")
        self.pause()
    
    def lihatRiwayatMahasiswa(self):
        try:
            nim = self.inputValid("NIM mahasiswa: ")
            self.laporan.cetakRiwayatMahasiswa(nim)
        except ValueError as e:
            print(f"Error: {e}")
        self.pause()

    def menuAlat(self):
        while True:
            print("\n===== Kelola Alat =====")
            print("1. Tambah alat")
            print("2. Tampilkan semua alat")
            print("3. Cari alat")
            print("4. Edit alat")
            print("5. Hapus alat")
            print("6. Lihat alat tersedia")
            print("7. Lihat alat dipinjam")
            print("8. Lihat alat rusak")
            print("9. Kelola kategori")
            print("0. Kembali ke menu utama")
            
            pilih = input("Silahkan piilih menu (0-9): ").strip()
            
            if pilih == "1": self.tambahAlat()
            elif pilih == "2": self.tampilkanSemuaAlat()
            elif pilih == "3": self.cariAlat()
            elif pilih == "4": self.editAlat()
            elif pilih == "5": self.hapusAlat()
            elif pilih == "6": self.laporan.cetakAlatTersedia(); self.pause()
            elif pilih == "7": self.laporan.cetakAlatDipinjam(); self.pause()
            elif pilih == "8": self.laporan.cetakAlatRusak(); self.pause()
            elif pilih == "9": self.menuKategori()
            elif pilih == "0": break
            else: print("Pilihan tidak valid. Silahkan pilih kembali")
    
    def tampilkanSemuaAlat(self):
        print("\n===== Daftar semua alat =====")
        daftar_alat = self.sistem.ambil_semua_alat()
        
        if len(daftar_alat) == 0:
            print("(Belum ada alat)")
            self.pause()
            return
        
        print(f"{'KODE':<8} | {'NAMA':<15} | {'KATEGORI':<15} | {'BAIK':<4} | {'R.RINGAN':<8} | {'R.BERAT':<7}")
        print("-" * 75)
        for a in daftar_alat:
            print(
                f"{a.getKode():<8} | {a.getNama():<15} | {a.getKategori().getNama():<15} | "
                f"{a.getStokBaik():<4} | {a.getStokRusakRingan():<8} | {a.getStokRusakBerat():<7}"
            )
        print(f"Total: {len(daftar_alat)} alat")
        self.pause()
    
    def tambahAlat(self):
        print("\n=== Tambah Alat ===")
        try:
            daftar_ktg = self.sistem.ambil_semua_kategori()
            if len(daftar_ktg) == 0:
                print("Belum ada kategori. Tambah kategori dulu (menu utama 2 -> tambahkan kategori 9).")
                self.pause()
                return
            
            kode = self.inputValid("Kode alat: ")
            nama = self.inputValid("Nama alat: ")
            
            print("\nKategori yang tersedia:")
            for ktg in daftar_ktg:
                print(f"  {ktg.getId()} - {ktg.getNama()}")
            
            id_ktg = self.inputValid("ID kategori: ")
            stok = self.inputAngka("Stok: ")
            
            alat = self.sistem.tambahAlat(kode, nama, id_ktg, stok)
            print(f"\nAlat {alat.getNama()} berhasil ditambahkan")
        except ValueError as e:
            print(f"\nError: {e}")
        self.pause()
    
    def cariAlat(self):
        print("\n=== Cari Alat ===")
        try:
            keyword = self.inputValid("Kata kunci (kode/nama/kategori): ")
            hasil = self.sistem.cariAlat(keyword)
            
            if len(hasil) == 0:
                print(f"Tidak ada alat cocok dengan '{keyword}'")
            else:
                print(f"\nDitemukan {len(hasil)} alat:")
                for a in hasil:
                    print(f"  {a.getDetail()}")
        except ValueError as e:
            print(f"Error: {e}")
        self.pause()
    
    def editAlat(self):
        print("\n=== Edit Alat ===")
        try:
            kode = self.inputValid("Kode alat yang mau diedit: ")
            alat = self.sistem.getAlat(kode)
            
            if not alat:
                raise ValueError(f"Alat dengan kode {kode} tidak ditemukan")
                
            print(f"\nData saat ini: {alat.getDetail()}")
            print("(Kosongkan jika tidak ada perubahan, isi angka jika ada)")
            
            nama = input("Nama baru: ").strip()
            
            id_ktg = None
            daftar_ktg = self.sistem.ambil_semua_kategori()
            print("\nKategori yang tersedia:")
            for ktg in daftar_ktg:
                print(f"  {ktg.getId()} - {ktg.getNama()}")
            id_ktg_input = input("ID kategori baru: ").strip()
            if id_ktg_input:
                id_ktg = id_ktg_input
                
            print("\n--- Aksi Stok dan Perbaikan ---")
            tambah_input = input("Tambah stok baru       : ").strip()
            tambah_stok = int(tambah_input) if tambah_input else 0
            
            ringan_input = input("Perbaikan Rusak Ringan : ").strip()
            perbaikan_ringan = int(ringan_input) if ringan_input else 0
            
            berat_input = input("Perbaikan Rusak Berat  : ").strip()
            perbaikan_berat = int(berat_input) if berat_input else 0
            
            self.sistem.editAlat(kode, nama, id_ktg, tambah_stok, perbaikan_ringan, perbaikan_berat)
            print("\nData alat berhasil diperbarui!")
        except ValueError as e:
            print(f"\nError: {e}")
        self.pause()
    
    def hapusAlat(self):
        print("\n=== Hapus Alat ===")
        try:
            kode = self.inputValid("Kode alat yang mau dihapus: ")
            alat = self.sistem.getAlat(kode)
            
            if not alat:
                raise ValueError(f"Alat dengan kode {kode} tidak ditemukan")
                
            konfirmasi = input(f"Yakin hapus {alat.getNama()}? (y/n): ").strip().lower()
            if konfirmasi == "y":
                self.sistem.hapusAlat(kode)
                print("Alat berhasil dihapus")
            else:
                print("(Batal)")
        except ValueError as e:
            print(f"Error: {e}")
        self.pause()

    def menuKategori(self):
        while True:
            print("\n===== Kelola Kategori =====")
            print("1. Tambah kategori")
            print("2. Tampilkan semua kategori")
            print("0. Kembali")
            
            pilih = input("Silahkan pilih menu (0-2): ").strip()
            
            if pilih == "1": self.tambahKategori()
            elif pilih == "2": self.tampilkanSemuaKategori()
            elif pilih == "0": break
            else: print("Pilihan tidak valid. silahkan pilih kembali")
    
    def tambahKategori(self):
        print("\n=== Tambah Kategori ===")
        try:
            id_ktg = self.inputValid("ID kategori: ")
            nama = self.inputValid("Nama kategori: ")
            deskripsi = input("Deskripsi (opsional): ").strip()
            
            self.sistem.tambahKategori(id_ktg, nama, deskripsi)
            print(f"\nKategori {nama} berhasil ditambahkan")
        except ValueError as e:
            print(f"\nError: {e}")
        self.pause()
    
    def tampilkanSemuaKategori(self):
        print("\n===== Daftar Kategori =====")
        daftar_ktg = self.sistem.ambil_semua_kategori()
        
        if len(daftar_ktg) == 0:
            print("(Belum ada kategori)")
            self.pause()
            return
        
        for ktg in daftar_ktg:
            desk = f" - {ktg.deskripsi}" if ktg.deskripsi else ""
            print(f"  [{ktg.getId()}] {ktg.getNama()}{desk}")
        print(f"Total: {len(daftar_ktg)} kategori")
        self.pause()

    def menuTransaksi(self):
        while True:
            print("\n===== Kelola Transaksi =====")
            print("1. Buat transaksi baru")
            print("2. Tampilkan semua transaksi")
            print("3. Cari transaksi by mahasiswa")
            print("4. Lihat detail transaksi")
            print("0. Kembali ke menu utama")
            
            pilih = input("Silahkan pilih menu (0-4): ").strip()
            
            if pilih == "1": self.buatTransaksi()
            elif pilih == "2": self.tampilkanSemuaTransaksi()
            elif pilih == "3": self.cariTransaksiByMahasiswa()
            elif pilih == "4": self.lihatDetailTransaksi()
            elif pilih == "0": break
            else: print("Pilihan tidak valid. silahkan pilih kembali")
    
    def buatTransaksi(self):
        print("\n=== Buat Transaksi Baru ===")
        try:
            nim = self.inputValid("NIM mahasiswa: ")
            mhs = self.sistem.getMahasiswa(nim)
            
            if not mhs:
                raise ValueError(f"Mahasiswa dengan NIM {nim} tidak ditemukan")
            
            self.sistem.validasiBatasTransaksi(nim)
            print(f"Mahasiswa: {mhs.getNama()}")
            
            print("\nMasukkan alat yang dipinjam (ketik 'selesai' untuk mengakhirinya): ")
            daftar_item = []
            
            while True:
                kode = input("Kode alat: ").strip()
                if kode.lower() == "selesai": break
                if not kode: continue
                
                try:
                    alat = self.sistem.getAlat(kode)
                    if not alat:
                        raise ValueError(f"Alat {kode} tidak ditemukan")
                    print(f"  -> {alat.getNama()} (stok: {alat.getStokBaik()})")
                    jumlah = self.inputAngka("  Jumlah: ")
                    daftar_item.append((kode, jumlah))
                except ValueError as e:
                    print(f"  {e}")
            
            if len(daftar_item) == 0:
                print("Tidak ada alat yang dipilih. Transaksi batal.")
                self.pause()
                return
            
            print("\nRingkasan:")
            for kode, jumlah in daftar_item:
                alat = self.sistem.getAlat(kode)
                print(f"  - {alat.getNama()} x {jumlah}")
            
            konfirmasi = input("\nKonfirmasi buat transaksi? (y/n): ").strip().lower()
            if konfirmasi != "y":
                print("(Batal)")
                self.pause()
                return
            
            trx = self.sistem.buatTransaksi(nim, daftar_item)
            print(f"\nTransaksi {trx.getIdTransaksi()} berhasil dibuat")
        except ValueError as e:
            print(f"\nError: {e}")
        self.pause()
    
    def tampilkanSemuaTransaksi(self):
        print("\n===== Daftar Semua Transaksi =====")
        daftar_trx = self.sistem.ambil_semua_transaksi()
        
        if len(daftar_trx) == 0:
            print("(Belum ada transaksi)")
            self.pause()
            return
        
        print(f"{'ID':<10} | {'PEMINJAM':<20} | {'TANGGAL':<12} | STATUS")
        print("-" * 75)
        for trx in daftar_trx:
            print(
                f"{trx.getIdTransaksi():<10} | "
                f"{trx.getMahasiswa().getNama():<20} | "
                f"{trx.getTanggalPinjam():%d-%m-%Y} | "
                f"{trx.getStatus()}"
            )
        print(f"Total: {len(daftar_trx)} transaksi")
        self.pause()
    
    def cariTransaksiByMahasiswa(self):
        print("\n=== Cari Transaksi by Mahasiswa ===")
        try:
            nim = self.inputValid("NIM mahasiswa: ")
            mhs = self.sistem.getMahasiswa(nim)
            if not mhs:
                raise ValueError(f"Mahasiswa dengan NIM {nim} tidak ditemukan")
                
            hasil = self.sistem.cariTransaksiByMahasiswa(nim)
            if len(hasil) == 0:
                print(f"Tidak ada transaksi untuk NIM {nim}")
            else:
                print(f"\nTransaksi milik {mhs.getNama()}:")
                for trx in hasil:
                    print(f"  {trx.getDetail()}")
        except ValueError as e:
            print(f"Error: {e}")
        self.pause()
    
    def lihatDetailTransaksi(self):
        try:
            id_trx = self.inputValid("ID transaksi: ")
            trx = self.sistem.getTransaksi(id_trx)
            if not trx:
                raise ValueError(f"Transaksi {id_trx} tidak ditemukan")
            print()
            print(trx.getDetail())
        except ValueError as e:
            print(f"Error: {e}")
        self.pause()

    def menuPengembalian(self):
        print("\n=== Proses Pengembalian Alat ===")
        try:
            id_trx = self.inputValid("ID transaksi: ")
            trx = self.sistem.getTransaksi(id_trx)
            if not trx:
                raise ValueError(f"Transaksi {id_trx} tidak ditemukan")
            
            print(f"\nDetail transaksi saat ini:")
            print(trx.getDetail())
            
            belum = trx.detailBelumKembali()
            if len(belum) == 0:
                print("\nSemua alat di transaksi ini sudah dikembalikan")
                self.pause()
                return
            
            print("\nAlat yang belum kembali:")
            for d in belum:
                print(f"  - {d.getAlat().getKode()} | {d.getAlat().getNama()} x {d.getJumlah()}")
            
            kode_alat = self.inputValid("\nKode alat yang dikembalikan: ")
            
            print("\nKondisi saat dikembalikan:")
            print("1. baik")
            print("2. rusak ringan")
            print("3. rusak berat")
            pilih_kondisi = input("Pilih (1-3): ").strip()
            
            if pilih_kondisi == "1": kondisi = "baik"
            elif pilih_kondisi == "2": kondisi = "rusak ringan"
            elif pilih_kondisi == "3": kondisi = "rusak berat"
            else:
                print("Pilihan kondisi tidak valid")
                self.pause()
                return
            
            self.sistem.prosesPengembalian(id_trx, kode_alat, kondisi)
            print(f"\nAlat {kode_alat} berhasil dikembalikan (kondisi: {kondisi})")
            
            if kondisi != "baik":
                print(f"  Alat dengan kondisi '{kondisi}' TIDAK masuk kembali ke stok.")
        except ValueError as e:
            print(f"\nError: {e}")
        self.pause()

    def menuLaporan(self):
        while True:
            print("\n===== Laporan dan Statistik =====")
            print("1. Alat tersedia")
            print("2. Alat dipinjam")
            print("3. Alat rusak")
            print("4. Statistik peminjaman")
            print("5. Ringkasan hari Ini")
            print("0. Kembali")
            
            pilih = input("Silahkan pilih menu (0-5): ").strip()
            
            if pilih == "1": self.laporan.cetakAlatTersedia(); self.pause()
            elif pilih == "2": self.laporan.cetakAlatDipinjam(); self.pause()
            elif pilih == "3": self.laporan.cetakAlatRusak(); self.pause()
            elif pilih == "4": self.laporan.cetakStatistik(); self.pause()
            elif pilih == "5": self.ringkasanHariIni()
            elif pilih == "0": break
            else: print("Pilihan tidak valid. Silahkan pilih kembali")
    
    def ringkasanHariIni(self):
        print("\n===== RINGKASAN HARI INI =====")
        r = self.laporan.ringkasanHariIni()
        print(f"Tanggal              : {r['tanggal']:%d-%m-%Y}")
        print(f"Jumlah transaksi     : {r['jumlah_transaksi']}")
        print(f"Jumlah alat dipinjam : {r['jumlah_alat_dipinjam']}")
        self.pause()
    
    def menuLog(self):
        print("\n===== Log Aktivitas =====")
        logs = self.sistem.ambil_log_terakhir(20)
        
        if len(logs) == 0:
            print("(Belum ada log)")
            self.pause()
            return
        
        for log in logs:
            print(log.format())
        
        print(f"\nMenampilkan {len(logs)} log terakhir.")
        self.pause()

    def menuEksporLaporan(self):
        print("\n=== Ekspor Laporan ===")
        teks_laporan = self.laporan.buat_teks_laporan()
        nama_file = input("Masukkan nama file (contoh: laporan_lab.txt): ").strip()
        
        if not nama_file.endswith(".txt"):
            nama_file += ".txt"
            
        if not os.path.exists("laporan"):
            os.makedirs("laporan")
            
        path = os.path.join("laporan", nama_file)
        with open(path, "w") as file:
            file.write(teks_laporan)
            
        print(f"\nLaporan berhasil disimpan di folder 'laporan/{nama_file}'")
        self.pause()