MAKS_TRANSAKSI_AKTIF = 2

class Mahasiswa:
    def __init__(self, nim, nama, no_hp, id_mahasiswa=None):
        if not nim or type(nim) != str:
            raise ValueError("NIM tidak boleh kosong!")
        if not nama or type(nama) != str:
            raise ValueError("Nama tidak boleh kosong!")
        if not no_hp or type(no_hp) != str:
            raise ValueError("Nomor HP tidak boleh kosong!")
            
        self.id_mahasiswa = id_mahasiswa
        self.nim = nim
        self.nama = nama
        self.no_hp = no_hp
    
    def getNim(self):
        return self.nim
    
    def getNama(self):
        return self.nama
    
    def getNoHp(self):
        return self.no_hp
    
    def ubahData(self, nama="", no_hp=""):
        if nama:
            self.nama = nama
        if no_hp:
            self.no_hp = no_hp

    def getDetail(self):
        return f"[{self.nim}] {self.nama} | HP: {self.no_hp}"