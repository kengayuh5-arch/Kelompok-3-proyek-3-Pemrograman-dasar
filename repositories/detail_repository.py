from models.detail_peminjaman import DetailPeminjaman
from models.alat import Alat
from models.kategori_alat import KategoriAlat


class DetailRepository:
    def __init__(self, database):
        self.database = database

    def _row_to_obj(self, row):
        if not row:
            return None
        ktg = KategoriAlat(
            id_kategori=row['id_kategori'],
            nama=row['nama_kategori'],
            deskripsi=row['deskripsi_kategori'] if row['deskripsi_kategori'] else ""
        )
        alat = Alat(
            kode=row['kode_alat'],
            nama=row['nama_alat'],
            kategori=ktg,
            stok_baik=row['stok_baik'],
            stok_rusak_ringan=row['stok_rusak_ringan'],
            stok_rusak_berat=row['stok_rusak_berat'],
            id_alat=row['id_alat']
        )

        return DetailPeminjaman(
            id_transaksi=row['id_transaksi'],
            alat=alat,
            jumlah=row['jumlah'],
            sudah_kembali=bool(row['sudah_kembali']),
            kondisi_kembali=row['kondisi_kembali'],
            tanggal_kembali=row['tanggal_kembali'],
            id_detail=row['id_detail']
        )


    def tambah(self, detail, conn=None):
        own_conn = conn is None
        
        if own_conn:
            conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                tgl = detail.tanggalKembali
                cur.execute(
                    """INSERT INTO detail_peminjaman 
                    (id_transaksi, id_alat, jumlah, sudah_kembali, kondisi_kembali, tanggal_kembali) 
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (detail.id_transaksi, detail.getIdAlat(), detail.getJumlah(), 
                     1 if detail.sudahKembali else 0, detail.kondisiKembali, tgl)
                )
                id_baru = cur.lastrowid
            if own_conn:
                conn.commit()
            return id_baru
        except Exception:
            
            if own_conn:
                conn.rollback()
            raise
        
        finally:
            if own_conn:
                conn.close()


    def tampilkan_by_transaksi(self, id_transaksi, conn=None):
        own_conn = conn is None
        if own_conn:
            conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("""SELECT d.*, a.kode_alat, a.nama AS nama_alat, a.id_kategori,
                    a.stok_baik, a.stok_rusak_ringan, a.stok_rusak_berat, 
                    k.nama AS nama_kategori, k.deskripsi AS deskripsi_kategori
                    FROM detail_peminjaman d
                    JOIN alat a ON d.id_alat = a.id_alat
                    JOIN kategori_alat k ON a.id_kategori = k.id_kategori
                    WHERE d.id_transaksi = %s
                    ORDER BY d.id_detail""", (id_transaksi,))
                rows = cur.fetchall()
                return [self._row_to_obj(row) for row in rows]
        finally:
            if own_conn:
                conn.close()

    def proses_pengembalian(self, id_detail, kondisi, tanggal_kembali, conn=None):
        own_conn = conn is None
        if own_conn:
            conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """UPDATE detail_peminjaman 
                    SET sudah_kembali=1, kondisi_kembali=%s, tanggal_kembali=%s 
                    WHERE id_detail=%s""",
                    (kondisi, tanggal_kembali, id_detail)
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

    def get_id_alat_dipinjam(self):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT DISTINCT id_alat FROM detail_peminjaman WHERE sudah_kembali = 0")
                rows = cur.fetchall()
                return [row['id_alat'] for row in rows]
        finally:
            conn.close()