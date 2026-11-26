from datetime import date, timedelta
from models.mahasiswa import Mahasiswa
from models.detail_peminjaman import DetailPeminjaman


MAKS_HARI = 7
STATUS_DIPINJAM = "dipinjam"
STATUS_SELESAI = "selesai"

class Transaksi:
    def __init__(self, id_transaksi, mahasiswa, tanggal_pinjam=None, batas_kembali=None, status=STATUS_DIPINJAM):
        if not id_transaksi or type(id_transaksi) != str:
            raise ValueError("ID transaksi tidak boleh kosong!")
        if type(mahasiswa) != Mahasiswa:
            raise ValueError("Mahasiswa harus objek Mahasiswa!")
        self.id_transaksi = id_transaksi
        self.mahasiswa = mahasiswa
        self.daftar_detail = []
        
        if tanggal_pinjam is None:
            self.tanggal_pinjam = date.today()
        else:
            self.tanggal_pinjam = tanggal_pinjam
        if batas_kembali is None:
            self.batas_kembali = self.tanggal_pinjam + timedelta(days=MAKS_HARI)
        else:
            self.batas_kembali = batas_kembali
            
        self.status = status
    
    def getIdTransaksi(self):
        return self.id_transaksi
    
    def getMahasiswa(self):
        return self.mahasiswa
    
    def getTanggalPinjam(self):
        return self.tanggal_pinjam
    
    def getBatasKembali(self):
        return self.batas_kembali
    
    def getStatus(self):
        return self.status
    
    def getDaftarDetail(self):
        return self.daftar_detail
    
    def tambahDetail(self, alat, jumlah=1):
        detail = DetailPeminjaman(self.id_transaksi, alat, jumlah)
        alat.pinjam(jumlah)
        self.daftar_detail.append(detail)
    
    def kembalikanAlat(self, kode_alat, kondisi, tgl_kembali=None):
        if tgl_kembali is None: tgl_kembali = date.today()
        
        for detail in self.daftar_detail:
            if detail.getAlat().getKode() == kode_alat and not detail.isKembali():
                detail.kembalikan(tgl_kembali, kondisi)
                self.perbaruiStatus()
                return
        raise ValueError(f"Alat {kode_alat} tidak ditemukan/sudah kembali.")
    
    def perbaruiStatus(self):
        if self.cekSemuaKembali():
            self.status = STATUS_SELESAI
        else:
            self.status = STATUS_DIPINJAM

    
    def cekSemuaKembali(self):
        if not self.daftar_detail: return False
        return all(d.isKembali() for d in self.daftar_detail)
    
    def detailBelumKembali(self):
        return [d for d in self.daftar_detail if not d.isKembali()]
    def isAktif(self): return self.status != STATUS_SELESAI
    
    def getDetail(self):
        baris = [f"Transaksi {self.id_transaksi}",
                 f"  Peminjam : {self.mahasiswa.getNama()} ({self.mahasiswa.getNim()})",
                 f"  Tanggal  : {self.tanggal_pinjam:%d-%m-%Y}",
                 f"  Batas    : {self.batas_kembali:%d-%m-%Y}",
                 f"  Status   : {self.status}",
                 f"  Alat     :"]
        if not self.daftar_detail:
            baris.append("    (Belum ada alat)")
        else:
            for d in self.daftar_detail:
                baris.append(f"    - {d.getDetail()}")
        return "\n".join(baris)


    def getIdMahasiswa(self):
        return self.mahasiswa.id_mahasiswa