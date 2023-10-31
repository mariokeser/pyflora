import sqlite3

class DbClient:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = self.get_connection

    def get_connection(self):
        try:
            conn = sqlite3.connect(self.db_name)
            return conn #imamo return jer moramo konekciju ove metode postaviti u konstrukt klase
        except sqlite3.Error as err:
            print(f"ERROR: {err}")

# Ovo dvoje radi isto za konekciju na bazu,samo što smo dolje conn stavili odmah u konstrukt klase,a gore smo napravili metodu u klasi
# i onda nju stavili u konstrukt klase, napravili smo odvojenu metodu u klasi za dohvaćanje baze, u oba slučaja imamo self.conn 
class DbClient:
    def __init__(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name) #self.conn jer se postavlja u klasu, a db_name, nema self. jer je samo parametar klase, ali nije
            #postavljen kao varijabla u klasu, ovdje nema returna jer je kon direktno u konstruktoru
        except sqlite3.Error as err:
            print(f"ERROR: {err}")