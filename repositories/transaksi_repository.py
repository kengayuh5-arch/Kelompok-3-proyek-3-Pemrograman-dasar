from models.transaksi import Transaksi
from models.mahasiswa import Mahasiswa

class TransaksiRepository:
    def __init__(self, database):
        self.database = database


    def _row_to_obj(self, row):
        if not row:
            return None
        mhs = Mahasiswa(
            nim=row['nim'],
            nama=row['nama'],
            no_hp=row['no_hp'],
            id_mahasiswa=row['id_mahasiswa']
        )
        return Transaksi(
            id_transaksi=row['id_transaksi'],
            mahasiswa=mhs,
            tanggal_pinjam=row['tanggal_pinjam'],
            batas_kembali=row['batas_kembali'],
            status=row['status']
        )


    def tambah(self, transaksi, conn=None):
        own_conn = conn is None
        if own_conn:
            conn = self.database.connect()
        
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO transaksi (id_transaksi, id_mahasiswa, tanggal_pinjam, batas_kembali, status) 
                    VALUES (%s, %s, %s, %s, %s)""",
                    (transaksi.getIdTransaksi(), transaksi.getIdMahasiswa(), 
                     transaksi.getTanggalPinjam(), transaksi.getBatasKembali(), transaksi.getStatus())
                )
            if own_conn:
                conn.commit()
            return True
        except Exception:
            if own_conn:
                conn.rollback()
            raise
        finally:
            if own_conn:
                conn.close()

    def tampilkan_semua(self):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("""SELECT t.*, m.nim, m.nama, m.no_hp 
                    FROM transaksi t
                    JOIN mahasiswa m ON t.id_mahasiswa = m.id_mahasiswa
                    ORDER BY t.id_transaksi DESC""")
                rows = cur.fetchall()
                return [self._row_to_obj(row) for row in rows]
        finally:
            conn.close()

    def cari_by_id(self, id_transaksi):
        conn = self.database.connect()
        
        try:
            with conn.cursor() as cur:
                cur.execute("""SELECT t.*, m.nim, m.nama, m.no_hp 
                    FROM transaksi t
                    JOIN mahasiswa m ON t.id_mahasiswa = m.id_mahasiswa
                    WHERE t.id_transaksi = %s""", (id_transaksi,))
                row = cur.fetchone()
                
                return self._row_to_obj(row)
        finally:
            conn.close()

    def cari_by_nim(self, nim):
        conn = self.database.connect()
        
        try:
            with conn.cursor() as cur:
                cur.execute("""SELECT t.*, m.nim, m.nama, m.no_hp 
                    FROM transaksi t
                    JOIN mahasiswa m ON t.id_mahasiswa = m.id_mahasiswa
                    WHERE m.nim = %s
                    ORDER BY t.id_transaksi DESC""", (nim,))
                rows = cur.fetchall()
                return [self._row_to_obj(row) for row in rows]
        finally:
            conn.close()

    def update_status(self, id_transaksi, status_baru, conn=None):
        own_conn = conn is None
        if own_conn:
            conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE transaksi SET status=%s WHERE id_transaksi=%s", 
                    (status_baru, id_transaksi)
                )
                changed = cur.rowcount
            if own_conn:
                conn.commit()
            return changed > 0
        except Exception:
            if own_conn:
                conn.rollback()
            raise
        
        finally:
            if own_conn:
                conn.close()
            
    def hitung_transaksi_aktif(self, id_mahasiswa):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT COUNT(*) AS total FROM transaksi WHERE id_mahasiswa = %s AND status != 'selesai'",
                    (id_mahasiswa,)
                )
                row = cur.fetchone()
                return row['total'] if row else 0
        
        finally:
            conn.close()

            
    def get_last_id(self):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id_transaksi FROM transaksi ORDER BY id_transaksi DESC LIMIT 1")
                row = cur.fetchone()
                return row['id_transaksi'] if row else None
        finally:
            conn.close()