import pymysql

class Database:
    def __init__(self):
        self.config = {
            "host": "localhost",
            "port": 3307,               # Sesuai dengan port
            "user": "root",
            "password": "",
            "database": "db_lab",       # Nama database
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor,
            "autocommit": False
        }

    def connect(self):
        return pymysql.connect(**self.config)

# Test
if __name__ == "__main__":
    print("Mencoba menghubungkan ke database db_lab...")
    db = Database()
    try:
        conn = db.connect()
        if conn:
            print("KONEKSI KE DB_LAB BERHASIL!")
            conn.close()
    except Exception as e:
        print("KONEKSI GAGAL. Pesan Error:")
        print(e)