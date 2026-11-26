from database import Database
from services.sistem_lab import SistemLab
from reports.laporan import Laporan
from ui.menu_app import MenuApp

def main():
    db = Database()
    sistem = SistemLab(db)
    
    
    laporan = Laporan(sistem)
    ui = MenuApp(sistem, laporan)
    
    try:
        ui.jalankan()
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan paksa oleh pengguna.")
    
if __name__ == "__main__":
    main()