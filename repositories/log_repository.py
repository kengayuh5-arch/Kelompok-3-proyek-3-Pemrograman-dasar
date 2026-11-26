from models.log_aktivitas import LogAktivitas


class LogRepository:
    def __init__(self, database):
        self.database = database

    def _row_to_obj(self, row):
        if not row: return None
        return LogAktivitas(
            pesan=row['pesan'],
            waktu=row['waktu'],
            id_log=row['id_log']
        )


    def tambah(self, log):
        conn = self.database.connect()

        try:
            with conn.cursor() as cur:
                waktu_str = log.waktu.strftime("%Y-%m-%d %H:%M:%S")
                cur.execute(
                    "INSERT INTO log_aktivitas (waktu, pesan) VALUES (%s, %s)",
                    (waktu_str, log.pesan)
                )
                
                conn.commit()
                return cur.lastrowid
        except Exception:
            conn.rollback()
            raise
        
        finally:
            conn.close()


    def tampilkan_terakhir(self, batas=20):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM log_aktivitas ORDER BY id_log DESC LIMIT %s", (batas,))
                rows = cur.fetchall()

                
                hasil = [self._row_to_obj(row) for row in rows]
                hasil.reverse() 
                return hasil
        finally:
            conn.close()



        