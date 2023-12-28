import datetime
import sqlite3
from tkinter import *

#query za kreiranje tablice admin
create_table_query = """CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    lastname TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);"""

#query za dohvaćanje usera, jednoga, admina
select_query = """SELECT  username, password FROM Users
WHERE username = ?;"""


#query za prikazivanje podataka u profilu
select_query_profile = """SELECT name, lastname, username, password FROM Users
WHERE username = ?;"""

#query za dodavanje usera s
insert_query = """INSERT INTO Users (name,lastname, username, password)
VALUES (?, ?, ?,?);"""


#query za promjenu podataka u profilu 
update_query_profile = """UPDATE Users SET name = ?, lastname = ?, password = ?
WHERE username = ?;"""

# Nikola: Koristi ovo kao primjer za Herbs
create_containers_query = """CREATE TABLE IF NOT EXISTS Containers(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    herb_id INTEGER,
    FOREIGN KEY (herb_id) REFERENCES Herbs(id)
);"""

add_new_containers_query = """INSERT INTO Containers (name, herb_id) VALUES (?, ?);"""
select_all_containers_sorted_query = """
    SELECT * FROM Containers
    ORDER BY 
        CASE
            WHEN herb_id IS NULL THEN 2
            ELSE 1
        END,
        herb_id
"""
select_container_query = """SELECT * FROM Containers WHERE id = ?;"""
delete_container_query = """DELETE FROM Containers WHERE id = ?;"""
update_container_query = """UPDATE Containers SET name = ?, herb_id = ? WHERE id = ?;"""


create_herbs_query = """CREATE TABLE IF NOT EXISTS Herbs(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    soil_moisture FLOAT NOT NULL,
    luminosity FLOAT NOT NULL,
    air_temperature FLOAT NOT NULL,
    ph_value FLOAT NOT NULL,
    features TEXT NOT NULL,
    herb_height INTEGER NOT NULL,
    herb_width INTEGER NOT NULL,
    image TEXT NOT NULL
);"""

add_new_herbs_query = """INSERT INTO Herbs (name, soil_moisture, luminosity, air_temperature,ph_value,
                                            features, herb_height, herb_width, image)
VALUES (?,?,?,?,?,?,?,?,?);"""


select_herb_query = """SELECT * FROM Herbs WHERE id = ?;"""
select_herb_by_name_query = """SELECT * FROM Herbs WHERE name = ?;"""
select_all_herbs_query = """SELECT * FROM Herbs"""
delete_herb_query = """DELETE FROM Herbs WHERE id = ?;"""
update_herb_query = """UPDATE Herbs SET name = ?, soil_moisture = ?, luminosity = ?, air_temperature = ?, ph_value = ?, features = ?, herb_height = ?, herb_width = ?, image = ?
WHERE id = ?;"""

create_temperature_table_query = """CREATE TABLE IF NOT EXISTS temperature (
    id INTEGER PRIMARY KEY,
    read_time DATETIME NOT NULL,
    value FLOAT NOT NULL
)"""
# query za ph value
create_ph_value_table_query = """CREATE TABLE IF NOT EXISTS ph_value (
    id INTEGER PRIMARY KEY,
    read_time DATETIME NOT NULL,
    value FLOAT NOT NULL
)"""
# query za tablicu za humidity, istakao i prethdne
create_humidity_table_query = """CREATE TABLE IF NOT EXISTS humidity (
    id INTEGER PRIMARY KEY,
    read_time DATETIME NOT NULL,
    value INTEGER NOT NULL
)"""

create_luminosity_table_query = """CREATE TABLE IF NOT EXISTS luminosity (
id INTEGER PRIMARY KEY,
read_time DATETIME NOT NULL,
value INTEGER NOT NULL
)"""


insert_temperature_query = """INSERT INTO temperature (read_time, value)
VALUES (?, ?)"""
#query za insert ph value
insert_ph_value_query = """INSERT INTO ph_value (read_time, value)
VALUES (?, ?)"""
#query za insert humidity, isto kao ovo prije
insert_humidity_query = """INSERT INTO humidity (read_time, value)
VALUES (?, ?)"""
insert_luminosity_query = """INSERT INTO luminosity (read_time, value)
VALUES (?, ?)"""


select_temperature_query = """SELECT  value FROM temperature
ORDER BY read_time DESC
LIMIT 1"""
# select za ph value
select_ph_value_query = """SELECT value FROM ph_value
ORDER BY read_time DESC
LIMIT 1"""

select_humidity_query = """SELECT value FROM humidity
ORDER BY read_time DESC
LIMIT 1"""
select_luminosity_query = """SELECT value FROM luminosity
ORDER BY read_time DESC
LIMIT 1"""

#konekcija na bazu 

def get_connection(db_name):
        try:
            conn = sqlite3.connect(db_name) 

            cursor = conn.cursor() 

            cursor.execute(create_table_query)
            cursor.execute(create_containers_query)
            cursor.execute(create_herbs_query)
            cursor.execute(create_temperature_table_query)
            cursor.execute(create_humidity_table_query)
            cursor.execute(create_ph_value_table_query) 
            cursor.execute(create_luminosity_table_query)
            conn.commit() 

            if login(conn, "admin") == None: 
               add_user(conn,"Mario", "Keser", "admin", "admin")

            cursor.close() 

            return conn 
        except sqlite3.Error as err:
            print(f"ERROR: {err}")

    #za dohvaćanje usera - preimenuj u login i promjeni sve u ovom fileu
def login(conn, username): 
        try:  
            cursor = conn.cursor()

            cursor.execute(select_query, (username, ))

            record = cursor.fetchone()

            if record != None: 
                return (record[0], record[1]) 
            else:                    
                return None 
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
        finally: 
            cursor.close()

    #dodavanje usera
def add_user(conn, name, lastname, username, password):
        try:
            cursor = conn.cursor() 

            if get_user(conn, username) != None:
                return False  

            cursor.execute(insert_query, (name, lastname, username, password)) 
            conn.commit() 

            return True
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
            
        finally:
            cursor.close()
    #za dohvaćanje usera  u edit profile- 
def get_user(conn, username): 
        try:  
            cursor = conn.cursor()

            cursor.execute(select_query_profile, (username, ))

            record = cursor.fetchone()

            if record != None: 
                return (record[0], record[2], record[2], record[3])
            else:
                cursor.close()
        except sqlite3.Error as err: 
            print(f"ERROR: {err}")

    # za promjenu podataka usera, stari user stavljen u old username
def update_user(conn, name, lastname,password, username):
        try:
            cursor = conn.cursor()
            
            # if get_user(conn, username) != None:
            #     return False

            cursor.execute(update_query_profile, (name, lastname, password, username))
    
            conn.commit()  
            #return True
        
        except sqlite3.Error as err: 
            print(f"ERROR: {err}")
            
        finally:
            cursor.close() 

    #dodavanje posude
def add_containers(conn, name, herb_id = None):
        try:
            cursor = conn.cursor()  
            cursor.execute(add_new_containers_query, (name, herb_id,)) 
            conn.commit()
            return True
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
            
        finally:
            cursor.close()

def get_all_containers(conn):
        try:
            cursor = conn.cursor()
            cursor.execute(select_all_containers_sorted_query)
            record = cursor.fetchall()
            result = []
            
            if record != None:
                for item in record:
                    result.append({"id": item[0], "name": item[1], "herb_id": item[2]})
                return result     
            else:
                cursor.close()
        except sqlite3.Error as err: 
            print(f"ERROR: {err}")

def get_container(conn, id):
        try:
            cursor = conn.cursor()
            cursor.execute(select_container_query, (id,))
            record = cursor.fetchone()
            
            if record != None:
                return (record[0], record[1],record[2]) 
            else:
                cursor.close()
        except sqlite3.Error as err: 
            print(f"ERROR: {err}")

def delete_container(conn, id): 
        try:
            cursor = conn.cursor() 

            if get_container(conn,id) == None:
                return False 

            cursor.execute(delete_container_query, (id,)) 

            conn.commit() 

            return True 
        except sqlite3.Error as err:
            print(f"ERROR: {err}")

def update_container(conn, name, container_id, herb_id=None):
        try:
            cursor = conn.cursor()

            cursor.execute(update_container_query, (name, herb_id, container_id))
    
            conn.commit()  
        
        except sqlite3.Error as err: 
            print(f"ERROR: {err}")
            
        finally:
            cursor.close() 

    #dodavanje bilja
def add_herbs(conn, name, soil_moisture, luminosity, air_temperature, ph_value, features, herb_hight, herb_width, image):
        try:
            cursor = conn.cursor()  

            cursor.execute(add_new_herbs_query, (name,soil_moisture, luminosity, air_temperature, ph_value, features, herb_hight, herb_width, image)) 
            conn.commit() 
            return True
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
            
        finally:
            cursor.close()
    #Brisanje biljke
def delete_herb(conn, id): 
        try:
            cursor = conn.cursor() 

            if get_herb(conn,id) == None:
                return False 

            cursor.execute(delete_herb_query, (id,)) 

            conn.commit() 

            return True 
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
        

    # za dohvaćanje herba u varijable i image
def get_herb(conn, id):
        try:
            cursor = conn.cursor()
            cursor.execute(select_herb_query, (id,))
            record = cursor.fetchone()
            
            if record != None:
                return (record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9])
            else:
                cursor.close()
        except sqlite3.Error as err: 
            print(f"ERROR: {err}")

def get_all_herbs(conn):
        try:
            cursor = conn.cursor()
            cursor.execute(select_all_herbs_query)
            record = cursor.fetchall()
            result = []
            
            if record != None:
                for item in record:
                    result.append({"id": item[0], "name": item[1], "soil_moisture": item[2], "luminosity": item[3], "air_temperature": item[4], "ph_value": item[5],
                                "features": item[6], "herb_height": item[7], "herb_width": item[8], "image": item[9]})
                return result     
            else:
                cursor.close()
        except sqlite3.Error as err: 
            print(f"ERROR: {err}")
    
    #za promjenu podataka herba
def update_herb(conn, name, soil_moisture, luminosity, air_temperature, ph_value, features, herb_height, herb_width, image, herb_id):
        try:
            cursor = conn.cursor()

            cursor.execute(update_herb_query, (name, soil_moisture, luminosity, air_temperature, ph_value, features, herb_height, herb_width, image, herb_id))
    
            conn.commit()  
        
        except sqlite3.Error as err: 
            print(f"ERROR: {err}")
            
        finally:
            cursor.close()

def get_herb_id_by_name(conn, name):
        try:
            cursor = conn.cursor()
            cursor.execute(select_herb_by_name_query, (name,))
            record = cursor.fetchone()
            
            if record != None:
                return record[0] 
            else:
                cursor.close()
        except sqlite3.Error as err: 
            print(f"ERROR: {err}")


def save_temperature_reading(conn, value):
            try:
                cursor = conn.cursor() 

                cursor.execute(insert_temperature_query, 
                            (datetime.datetime.now(), value))

                conn.commit() 
            except sqlite3.Error as err:
                print(f"ERROR: {err}")
            finally:
                cursor.close()

def save_ph_value_reading(conn, value): 
        try:
            cursor = conn.cursor()

            cursor.execute(insert_ph_value_query,
                            (datetime.datetime.now(), value))

            conn.commit()
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
        finally:
            cursor.close()

def save_humidity_reading(conn, value):
        try:
            cursor = conn.cursor()

            cursor.execute(insert_humidity_query,
                            (datetime.datetime.now(), value))

            conn.commit()
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
        finally:
            cursor.close()

def save_luminosity_reading(conn, value):
        try:
            cursor = conn.cursor()

            cursor.execute(insert_luminosity_query,
                            (datetime.datetime.now(), value))

            conn.commit()
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
        finally:
            cursor.close()


def get_temperature(conn): 
        try:
            cursor = conn.cursor()

            cursor.execute(select_temperature_query) 
            record = cursor.fetchone() 
            
            if record != None: 
                return record[0] 
            else: 
                return None 
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
        finally:
            cursor.close()

def get_ph_value(conn):
        try:
            cursor = conn.cursor()

            cursor.execute(select_ph_value_query)

            record = cursor.fetchone()

            if record != None:
                return record[0]
            else:
                return None
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
        finally:
            cursor.close()

def get_humidity(conn):
        try:
            cursor = conn.cursor()

            cursor.execute(select_humidity_query)

            record = cursor.fetchone()

            if record != None:
                return record[0]
            else:
                return None
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
        finally:
            cursor.close()

def get_luminosity(conn):
        try:
            cursor = conn.cursor()

            cursor.execute(select_luminosity_query)

            record = cursor.fetchone()

            if record != None:
                return record[0]
            else:
                return None
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
        finally:
            cursor.close()


class App(Tk):
    def __init__(self, db_client):
        super().__init__()

        self.db_client = db_client

        self.title("Pyflora Simulator")
        self.geometry("500x300")              
 
        self.var_temp = DoubleVar(self, 20) 
        self.sld_temp = Slider(self, 
                               "Temperature (°C)", 
                               -30, 
                               105, 
                               0.5, 
                               250, 
                               self.var_temp) 
        
        self.sld_temp.grid(column=0, row=0) 
        self.sld_temp.after(1000, self.save_temperature)
        

        self.var_ph_value = DoubleVar(self, 7) 
        self.sld_ph_value = Slider(self,
                                "pH_value (pH)",
                                1, 
                                14,
                                0.5, 
                                length=250, 
                                variable=self.var_ph_value) 
        self.sld_ph_value.grid(column=1, row=0) 
        self.sld_ph_value.after(1000, self.save_ph_value) 
        self.var_hum = IntVar(self, 50) 
        self.sld_hum = Slider(self,
                              "Humidity (%)",
                              0, #from_
                              100, #to
                              length=250,
                              variable=self.var_hum) 
        self.sld_hum.grid(column=2, row=0)
        self.sld_hum.after(1000, self.save_humidity)
        
        self.var_lum = IntVar(self, 7000)
        self.sld_lum = Slider (self,
                              "Luminosity (pH)",
                              from_ = 0,
                              to = 10500,
                              resolution=500,
                              length=250,
                              variable=self.var_lum)
        self.sld_lum.grid(column=3, row=0)
        self.sld_lum.after(1000, self.save_luminosity)

    def save_temperature(self): 
        self.db_client.save_temperature_reading(self.var_temp.get())
        self.sld_temp.after(1000, self.save_temperature)

    def save_ph_value(self):
        self.db_client.save_ph_value_reading(self.var_ph_value.get())
        self.sld_ph_value.after(1000, self.save_ph_value)

    def save_humidity(self):
        self.db_client.save_humidity_reading(self.var_hum.get())
        self.sld_hum.after(1000, self.save_humidity)
    
    def save_luminosity(self):
        self.db_client.save_luminosity_reading(self.var_lum.get())
        self.sld_lum.after(1000, self.save_luminosity)



class Slider(Frame): 
    def __init__(self, 
                 master,
                 title, 
                 from_,
                 to,
                 resolution=1, 
                 length=None, 
                 variable=None,
                 orientation=VERTICAL):
        super().__init__(master) 
       

        if orientation == VERTICAL: 
            from_, to = to, from_ 


        Label(self, text=title).grid(column=0, row=0)

        self.scale = Scale(self, 
                              from_=from_, 
                              to=to,  
                              resolution=resolution,
                              tickinterval=abs(to-from_),

                              length=length,
                              variable=variable, 
                              orient=orientation) 
        self.scale.grid(column=0, row=1) 