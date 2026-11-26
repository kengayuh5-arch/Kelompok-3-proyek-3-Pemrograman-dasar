from models.alat import Alat
from models.kategori_alat import KategoriAlat


class AlatRepository:
    def __init__(self, database):
        self.database = database

    def _row_to_obj(self, row):
        if not row:
            return None
        kategori = KategoriAlat(
            id_kategori=row['id_kategori'],
            nama=row['nama_kategori'],
            deskripsi=row['deskripsi_kategori'] if row['deskripsi_kategori'] else ""
        )
        
        return Alat(
            kode=row['kode_alat'],
            nama=row['nama'],
            kategori=kategori,
            stok_baik=row['stok_baik'],
            stok_rusak_ringan=row['stok_rusak_ringan'],
            stok_rusak_berat=row['stok_rusak_berat'],
            id_alat=row['id_alat']
        )


    def tambah(self, alat):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO alat 
                    (kode_alat, nama, id_kategori, stok_baik, stok_rusak_ringan, stok_rusak_berat) 
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (alat.getKode(), alat.getNama(), alat.getIdKategori(), 
                     alat.getStokBaik(), alat.getStokRusakRingan(), alat.getStokRusakBerat())
                )
                id_baru = cur.lastrowid
                conn.commit()
                return id_baru
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


    def tampilkan_semua(self):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("""SELECT a.*, k.nama AS nama_kategori, k.deskripsi AS deskripsi_kategori
                    FROM alat a
                    JOIN kategori_alat k ON a.id_kategori = k.id_kategori
                    ORDER BY a.id_alat""")
                rows = cur.fetchall()
                return [self._row_to_obj(row) for row in rows]
        finally:
            conn.close()


    def ubah(self, alat, conn=None):
        own_conn = conn is None
        if own_conn:
            conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """UPDATE alat 
                    SET nama=%s, id_kategori=%s, stok_baik=%s, stok_rusak_ringan=%s, stok_rusak_berat=%s 
                    WHERE id_alat=%s""",
                    (alat.getNama(), alat.getIdKategori(), alat.getStokBaik(), 
                     alat.getStokRusakRingan(), alat.getStokRusakBerat(), alat.id_alat)
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


    def hapus(self, id_alat):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM alat WHERE id_alat=%s", (id_alat,))
                changed = cur.rowcount
                conn.commit()
                return changed > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


    def cari(self, keyword):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                search_query = f"%{keyword}%"
                cur.execute("""SELECT a.*, k.nama AS nama_kategori, k.deskripsi AS deskripsi_kategori
                    FROM alat a
                    JOIN kategori_alat k ON a.id_kategori = k.id_kategori
                    WHERE a.kode_alat LIKE %s OR a.nama LIKE %s OR k.nama LIKE %s
                    ORDER BY a.id_alat""",
                    (search_query, search_query, search_query)
                )
                rows = cur.fetchall()
                return [self._row_to_obj(row) for row in rows]
        finally:
            conn.close()


    def cari_by_kode(self, kode_alat):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("""SELECT a.*, k.nama AS nama_kategori, k.deskripsi AS deskripsi_kategori
                    FROM alat a
                    JOIN kategori_alat k ON a.id_kategori = k.id_kategori
                    WHERE a.kode_alat = %s""", (kode_alat,))
                row = cur.fetchone()
                return self._row_to_obj(row)
        finally:
            conn.close()
