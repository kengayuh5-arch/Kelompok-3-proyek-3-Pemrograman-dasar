from models.mahasiswa import Mahasiswa

class MahasiswaRepository:
    def __init__(self, database):
        self.database = database


    def _row_to_obj(self, row):
        if not row: return None
        return Mahasiswa(
            nim=row['nim'],
            nama=row['nama'],
            no_hp=row['no_hp'],
            id_mahasiswa=row['id_mahasiswa']
        )
    def tambah(self, mahasiswa):
        conn = self.database.connect()
        
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO mahasiswa (nim, nama, no_hp) VALUES (%s, %s, %s)",
                    (mahasiswa.getNim(), mahasiswa.getNama(), mahasiswa.getNoHp())
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
                cur.execute("SELECT * FROM mahasiswa ORDER BY id_mahasiswa")
                rows = cur.fetchall()
                return [self._row_to_obj(row) for row in rows]
        finally:
            conn.close()


    def ubah(self, id_mahasiswa, nama, no_hp):
        conn = self.database.connect()
        
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE mahasiswa SET nama=%s, no_hp=%s WHERE id_mahasiswa=%s",
                    (nama, no_hp, id_mahasiswa)
                )
                changed = cur.rowcount
                conn.commit()
                return changed > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


    def hapus(self, id_mahasiswa):
        conn = self.database.connect()
        
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM mahasiswa WHERE id_mahasiswa=%s", (id_mahasiswa,))
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
                cur.execute(
                    "SELECT * FROM mahasiswa WHERE nim LIKE %s OR nama LIKE %s ORDER BY id_mahasiswa",
                    (search_query, search_query)
                )
                rows = cur.fetchall()
                return [self._row_to_obj(row) for row in rows]
        finally:
            conn.close()

    def cari_by_nim(self, nim):
        conn = self.database.connect()
        
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM mahasiswa WHERE nim = %s", (nim,))
                row = cur.fetchone()
                return self._row_to_obj(row)
        finally:
            conn.close()