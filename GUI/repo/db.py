import sqlite3

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

select_all_containers_query = """SELECT * FROM Containers"""
select_container_query = """SELECT * FROM Containers WHERE id = ?;"""
delete_container_query = """DELETE FROM Containers WHERE id = ?;"""
update_container_query = """UPDATE Containers SET name = ?
WHERE id = ?;"""


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
select_all_herbs_query = """SELECT * FROM Herbs"""
delete_herb_query = """DELETE FROM Herbs WHERE id = ?;"""
update_herb_query = """UPDATE Herbs SET name = ?, soil_moisture = ?, luminosity = ?, air_temperature = ?, ph_value = ?, features = ?, herb_height = ?, herb_width = ?, image = ?
WHERE id = ?;"""



#konekcija na bazu 
def get_connection(db_name):
    try:
        conn = sqlite3.connect(db_name) 

        cursor = conn.cursor() 

        cursor.execute(create_table_query)
        cursor.execute(create_containers_query)
        cursor.execute(create_herbs_query)
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
        cursor.execute(select_all_containers_query)
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

def update_container(conn, name, container_id):
    try:
        cursor = conn.cursor()

        cursor.execute(update_container_query, (name, container_id))
   
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
            return (record[0], record[1],record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]) 
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