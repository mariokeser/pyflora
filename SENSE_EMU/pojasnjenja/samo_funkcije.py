import sqlite3
# ovdje imamo samo funkcije bez klase, metode nad klasom su zaprave funkcije

def get_connection(db_name):
        try:
            conn = sqlite3.connect(db_name)
            return conn 
        except sqlite3.Error as err:
            print(f"ERROR: {err}")

def get_temperature(conn): # za čuvanje temperature u bazi nam treba konekcija na bazu u ovoj funkciji koju smo dobili u gornjoj funkciji
     cursor = conn.cursor() # pozivamo cursor nad konekcijom, itd

# to bi bio rad samo sa funkcijama bez klasa, može se raditi i bez klasa, samo s funkcijama, sve klase jesu funkcije, ali imaju self.