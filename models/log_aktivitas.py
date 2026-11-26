from datetime import datetime

class LogAktivitas:
    def __init__(self, pesan, waktu=None, id_log=None):
        if not pesan or type(pesan) != str:
            raise ValueError("Pesan log tidak boleh kosong!")
        
        self.id_log = id_log 
        self.pesan = pesan
        self.waktu = waktu if waktu else datetime.now()

    
    def format(self):
        waktu_str = self.waktu.strftime("%Y-%m-%d %H:%M")
        return f"[{waktu_str}] {self.pesan}"