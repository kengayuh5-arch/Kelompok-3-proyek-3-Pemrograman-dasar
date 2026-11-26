from models.kategori_alat import KategoriAlat

class KategoriRepository:
    def __init__(self, database):
        self.database = database

    def _row_to_obj(self, row):
        if not row: return None
        return KategoriAlat(
            id_kategori=row['id_kategori'],
            nama=row['nama'],
            deskripsi=row['deskripsi'] if row['deskripsi'] else ""
        )

    def tambah(self, kategori):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO kategori_alat (id_kategori, nama, deskripsi) VALUES (%s, %s, %s)",
                    (kategori.getId(), kategori.getNama(), kategori.deskripsi)
                )
                conn.commit()
                return True
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def tampilkan_semua(self):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM kategori_alat ORDER BY id_kategori")
                rows = cur.fetchall()
                return [self._row_to_obj(row) for row in rows]
        finally:
            conn.close()

    def cari_by_id(self, id_kategori):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM kategori_alat WHERE id_kategori = %s", (id_kategori,))
                row = cur.fetchone()
                return self._row_to_obj(row)
        finally:
            conn.close()

            