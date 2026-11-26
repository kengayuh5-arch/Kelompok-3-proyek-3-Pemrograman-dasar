from datetime import date
from models.alat import Alat, KONDISI_VALID


class DetailPeminjaman:
    def __init__(self, id_transaksi, alat, jumlah=1, sudah_kembali=False, kondisi_kembali=None, tanggal_kembali=None, id_detail=None):
        if type(alat) != Alat:
            raise ValueError("Alat harus berupa objek Alat!")
        if type(jumlah) != int or jumlah <= 0:
            raise ValueError("Jumlah harus integer > 0!")
        
        self.id_detail = id_detail
        self.id_transaksi = id_transaksi
        self.alat = alat
        self.jumlah = jumlah
        
        # Terima nilai dari database
        self.sudahKembali = sudah_kembali
        self.tanggalKembali = tanggal_kembali
        self.kondisiKembali = kondisi_kembali

    
    def getAlat(self): return self.alat

    def getJumlah(self): return self.jumlah
    
    def kembalikan(self, tgl, kondisi):
        if self.sudahKembali:
            raise ValueError(f"Alat {self.alat.getNama()} sudah dikembalikan!")
        if type(tgl) != date:
            raise ValueError("Tanggal harus date!")
        if kondisi not in KONDISI_VALID:
            raise ValueError("Kondisi tidak valid!")
        
        self.sudahKembali = True
        self.tanggalKembali = tgl
        self.kondisiKembali = kondisi
        self.alat.kembali(kondisi, self.jumlah)

    
    def isKembali(self): return self.sudahKembali
    
    def getDetail(self):
        if self.sudahKembali:
            status = f"Kembali {self.tanggalKembali:%d-%m-%Y} (kondisi: {self.kondisiKembali})"
        else:
            status = "Belum kembali"
        return f"{self.alat.getNama()} x {self.jumlah} [{self.alat.getKode()}] - {status}"

    def getIdAlat(self):
        return self.alat.id_alat