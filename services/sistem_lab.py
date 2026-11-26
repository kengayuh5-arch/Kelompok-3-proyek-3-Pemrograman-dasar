from datetime import date
from models.mahasiswa import Mahasiswa, MAKS_TRANSAKSI_AKTIF
from models.alat import Alat
from models.kategori_alat import KategoriAlat
from models.transaksi import Transaksi
from models.detail_peminjaman import DetailPeminjaman
from models.log_aktivitas import LogAktivitas

from repositories.mahasiswa_repository import MahasiswaRepository
from repositories.kategori_repository import KategoriRepository
from repositories.alat_repository import AlatRepository
from repositories.transaksi_repository import TransaksiRepository
from repositories.detail_repository import DetailRepository
from repositories.log_repository import LogRepository

class SistemLab:
    def __init__(self, database):
        self.database = database
        self.mhs_repo = MahasiswaRepository(database)
        self.kat_repo = KategoriRepository(database)
        self.alat_repo = AlatRepository(database)
        self.trx_repo = TransaksiRepository(database)
        self.detail_repo = DetailRepository(database)
        self.log_repo = LogRepository(database)
        
        self.counter_transaksi = 0
        self._init_counter()

    def _init_counter(self):
        last_id = self.trx_repo.get_last_id()
        if last_id:
            self.counter_transaksi = int(last_id.replace("TRX", ""))
        else:
            self.counter_transaksi = 0

    def catatLog(self, pesan):
        log_baru = LogAktivitas(pesan)
        self.log_repo.tambah(log_baru)

    def generateIdTransaksi(self):
        self.counter_transaksi += 1
        angka_str = str(self.counter_transaksi)
        while len(angka_str) < 3:
            angka_str = "0" + angka_str
        return "TRX" + angka_str

    def validasiBatasTransaksi(self, nim):
        mhs = self.getMahasiswa(nim)
        if not mhs:
            raise ValueError(f"Mahasiswa {nim} tidak ditemukan!")
            
        trx_aktif = self.trx_repo.hitung_transaksi_aktif(mhs.id_mahasiswa)
        if trx_aktif >= MAKS_TRANSAKSI_AKTIF:
            raise ValueError(f"Mahasiswa {nim} sudah mencapai batas maksimal {MAKS_TRANSAKSI_AKTIF} transaksi aktif!")
        return True

    # ================= KELOLA MAHASISWA =================
    def tambahMahasiswa(self, nim, nama, no_hp):
        if self.getMahasiswa(nim):
            raise ValueError(f"Mahasiswa dengan NIM {nim} sudah terdaftar")
        mhs = Mahasiswa(nim, nama, no_hp)
        self.mhs_repo.tambah(mhs)
        self.catatLog(f"Mahasiswa {nim} ({nama}) ditambahkan")
        return mhs
    
    def editMahasiswa(self, nim, nama="", no_hp=""):
        mhs = self.getMahasiswa(nim)
        if not mhs:
            raise ValueError(f"Mahasiswa dengan NIM {nim} tidak ditemukan")
        
        nama_baru = nama if nama else mhs.getNama()
        no_hp_baru = no_hp if no_hp else mhs.getNoHp()
            
        self.mhs_repo.ubah(mhs.id_mahasiswa, nama_baru, no_hp_baru)
        self.catatLog(f"Data mahasiswa {nim} diperbarui")
    
    def hapusMahasiswa(self, nim):
        mhs = self.getMahasiswa(nim)
        if not mhs:
            raise ValueError(f"Mahasiswa dengan NIM {nim} tidak ditemukan")
        
        if self.trx_repo.hitung_transaksi_aktif(mhs.id_mahasiswa) > 0:
            raise ValueError(f"Mahasiswa {mhs.getNama()} masih punya transaksi aktif!")
        
        try:
            self.mhs_repo.hapus(mhs.id_mahasiswa)
            self.catatLog(f"Mahasiswa {nim} ({mhs.getNama()}) dihapus")
        except Exception as e:
            if "foreign key constraint fails" in str(e).lower():
                raise ValueError(f"Gagal menghapus! Mahasiswa {mhs.getNama()} memiliki riwayat transaksi di database.")
            raise e

    # ================= KELOLA KATEGORI =================
    def tambahKategori(self, id_kategori, nama, deskripsi=""):
        if self.kat_repo.cari_by_id(id_kategori):
            raise ValueError(f"Kategori {id_kategori} sudah ada!")
        ktg = KategoriAlat(id_kategori, nama, deskripsi)
        self.kat_repo.tambah(ktg)
        self.catatLog(f"Kategori {id_kategori} ({nama}) ditambahkan")
        return ktg

    # ================= KELOLA ALAT =================
    def tambahAlat(self, kode, nama, id_kategori, stok=1):
        if self.getAlat(kode):
            raise ValueError(f"Alat dengan kode {kode} sudah ada!")
        if type(stok) != int or stok <= 0:
            raise ValueError("Stok awal alat harus lebih dari 0!")
        
        ktg = self.kat_repo.cari_by_id(id_kategori)
        if not ktg:
            raise ValueError(f"Kategori {id_kategori} tidak ditemukan!")
        
        alat = Alat(kode, nama, ktg, stok_baik=stok)
        self.alat_repo.tambah(alat)
        self.catatLog(f"Alat {kode} ({nama}) ditambahkan")
        return alat
    
    def editAlat(self, kode, nama="", id_kategori=None, tambah_stok=0, perbaikan_ringan=0, perbaikan_berat=0):
        alat = self.getAlat(kode)
        if not alat:
            raise ValueError(f"Alat dengan kode {kode} tidak ditemukan")
        
        ktg = None
        if id_kategori is not None:
            ktg = self.kat_repo.cari_by_id(id_kategori)
            if not ktg:
                raise ValueError(f"Kategori {id_kategori} tidak ditemukan")
            
        alat.ubahData(nama, ktg, tambah_stok, perbaikan_ringan, perbaikan_berat)
        
        self.alat_repo.ubah(alat)
        self.catatLog(f"Data alat {kode} diperbarui")
    
    def hapusAlat(self, kode):
        alat = self.getAlat(kode)
        if not alat:
            raise ValueError(f"Alat dengan kode {kode} tidak ditemukan")
        
        if alat.id_alat in self.detail_repo.get_id_alat_dipinjam():
            raise ValueError(f"Alat {kode} ({alat.getNama()}) masih tercatat dalam transaksi peminjaman aktif!")
        
        try:
            self.alat_repo.hapus(alat.id_alat)
            self.catatLog(f"Alat {kode} ({alat.getNama()}) dihapus")
        except Exception as e:
            if "foreign key constraint fails" in str(e).lower():
                raise ValueError(f"Gagal menghapus! Alat {kode} memiliki riwayat di transaksi.")
            raise e

    # ================= TRANSAKSI & PENGEMBALIAN =================
    def buatTransaksi(self, nim, daftar_item):
        mhs = self.getMahasiswa(nim)
        if not mhs:
            raise ValueError(f"Mahasiswa dengan NIM {nim} tidak ditemukan")
        
        self.validasiBatasTransaksi(nim)
        
        if not daftar_item or len(daftar_item) == 0:
            raise ValueError("Transaksi harus punya minimal 1 alat")
        
        item_digabung = {}
        for kode, jumlah in daftar_item:
            item_digabung[kode] = item_digabung.get(kode, 0) + jumlah
        
        alat_valid = {}
        for kode, total_jumlah in item_digabung.items():
            if type(total_jumlah) != int or total_jumlah <= 0:
                raise ValueError(f"Jumlah pinjam untuk {kode} harus lebih dari 0!")
            alat = self.getAlat(kode)
            if not alat:
                raise ValueError(f"Alat {kode} tidak ditemukan!")
            if not alat.isTersedia():
                raise ValueError(f"Alat {alat.getNama()} tidak tersedia (Stok Baik habis).")
            if total_jumlah > alat.getStokBaik():
                raise ValueError(f"Stok {alat.getNama()} tidak cukup! Tersedia: {alat.getStokBaik()}")
            alat_valid[kode] = alat
        
        conn = self.database.connect()
        try:
            id_trx = self.generateIdTransaksi()
            trx = Transaksi(id_trx, mhs)
            self.trx_repo.tambah(trx, conn=conn)
            
            for kode, total_jumlah in item_digabung.items():
                alat = alat_valid[kode]
                alat.pinjam(total_jumlah)
                self.alat_repo.ubah(alat, conn=conn)
                
                detail = DetailPeminjaman(id_trx, alat, total_jumlah)
                self.detail_repo.tambah(detail, conn=conn)
                trx.daftar_detail.append(detail)
                
            conn.commit()
        except Exception:
            conn.rollback()
            self._init_counter()
            raise
        finally:
            conn.close()
        
        ringkasan = ", ".join([f"{kode} x {jml}" for kode, jml in item_digabung.items()])
        self.catatLog(f"Transaksi {id_trx} dibuat oleh {mhs.getNama()}: {ringkasan}")
        
        return trx

    def prosesPengembalian(self, id_trx, kode_alat, kondisi):
        trx = self.getTransaksi(id_trx)
        if not trx:
            raise ValueError(f"Transaksi {id_trx} tidak ditemukan")
        if not trx.isAktif():
            raise ValueError(f"Transaksi {id_trx} sudah selesai")
        
        conn = self.database.connect()
        try:
            detail_list = self.detail_repo.tampilkan_by_transaksi(id_trx, conn=conn)
            detail_target = None
            for d in detail_list:
                if d.getAlat().getKode() == kode_alat and not d.isKembali():
                    detail_target = d
                    break
                    
            if not detail_target:
                raise ValueError(f"Alat {kode_alat} tidak ditemukan/sudah kembali.")
                
            tgl_kembali = date.today()
            detail_target.kembalikan(tgl_kembali, kondisi)
            
            self.detail_repo.proses_pengembalian(detail_target.id_detail, kondisi, tgl_kembali, conn=conn)
            
            alat = detail_target.getAlat()
            self.alat_repo.ubah(alat, conn=conn)
            
            detail_list_baru = self.detail_repo.tampilkan_by_transaksi(id_trx, conn=conn)
            if all(d.isKembali() for d in detail_list_baru):
                self.trx_repo.update_status(id_trx, "selesai", conn=conn)
                
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
            
        self.catatLog(f"{trx.getMahasiswa().getNama()} mengembalikan {kode_alat} (kondisi: {kondisi}) di transaksi {id_trx}")

    # ================= GETTERS & PENCARIAN =================
    def getMahasiswa(self, nim):
        return self.mhs_repo.cari_by_nim(nim)

    def cariMahasiswa(self, keyword):
        return self.mhs_repo.cari(keyword)

    def getKategori(self, id_kategori):
        return self.kat_repo.cari_by_id(id_kategori)

    def getAlat(self, kode):
        return self.alat_repo.cari_by_kode(kode)

    def cariAlat(self, keyword):
        return self.alat_repo.cari(keyword)

    def getTransaksi(self, id_trx):
        trx = self.trx_repo.cari_by_id(id_trx)
        if trx:
            trx.daftar_detail = self.detail_repo.tampilkan_by_transaksi(id_trx)
        return trx

    def cariTransaksiByMahasiswa(self, nim):
        daftar_trx = self.trx_repo.cari_by_nim(nim)
        for trx in daftar_trx:
            trx.daftar_detail = self.detail_repo.tampilkan_by_transaksi(trx.getIdTransaksi())
        return daftar_trx

    def getAlatTersedia(self):
        semua_alat = self.alat_repo.tampilkan_semua()
        return [a for a in semua_alat if a.isTersedia()]

    def getAlatDipinjam(self):
        semua_alat = self.alat_repo.tampilkan_semua()
        id_alat_dipinjam = self.detail_repo.get_id_alat_dipinjam()
        return [a for a in semua_alat if a.id_alat in id_alat_dipinjam]

    def getAlatRusak(self):
        semua_alat = self.alat_repo.tampilkan_semua()
        return [a for a in semua_alat if a.getStokRusakRingan() > 0 or a.getStokRusakBerat() > 0]

    def ambil_semua_mahasiswa(self):
        return self.mhs_repo.tampilkan_semua()
        
    def ambil_semua_alat(self):
        return self.alat_repo.tampilkan_semua()
        
    def ambil_semua_kategori(self):
        return self.kat_repo.tampilkan_semua()
        
    def ambil_semua_transaksi(self):
        daftar_trx = self.trx_repo.tampilkan_semua()
        for trx in daftar_trx:
            trx.daftar_detail = self.detail_repo.tampilkan_by_transaksi(trx.getIdTransaksi())
        return daftar_trx
        
    def ambil_log_terakhir(self, batas=20):
        return self.log_repo.tampilkan_terakhir(batas)