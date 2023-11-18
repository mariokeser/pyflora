import sqlite3 
import datetime 


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


class DbClient:
    def __init__(self, db_name):
        self.conn = self.get_connection(db_name)

    def get_connection(self, db_name):
        try:
            conn = sqlite3.connect(db_name) 

            cursor = conn.cursor() 

            cursor.execute(create_temperature_table_query)
            cursor.execute(create_humidity_table_query)
            cursor.execute(create_ph_value_table_query) 
            cursor.execute(create_luminosity_table_query)

            conn.commit() 
            return conn
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
        finally: 
            cursor.close()


    def save_temperature_reading(self, value):
        try:
            cursor = self.conn.cursor() 

            cursor.execute(insert_temperature_query, 
                           (datetime.datetime.now(), value))

            self.conn.commit() 
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
        finally:
            cursor.close()

    def save_ph_value_reading(self, value): 
        try:
            cursor = self.conn.cursor()

            cursor.execute(insert_ph_value_query,
                           (datetime.datetime.now(), value))

            self.conn.commit()
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
        finally:
            cursor.close()
    
    def save_humidity_reading(self, value):
        try:
            cursor = self.conn.cursor()

            cursor.execute(insert_humidity_query,
                           (datetime.datetime.now(), value))

            self.conn.commit()
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
        finally:
            cursor.close()
    
    def save_luminosity_reading(self, value):
        try:
            cursor = self.conn.cursor()

            cursor.execute(insert_luminosity_query,
                           (datetime.datetime.now(), value))

            self.conn.commit()
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
        finally:
            cursor.close()


    def get_temperature(self): 
        try:
            cursor = self.conn.cursor()

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

    def get_ph_value(self):
        try:
            cursor = self.conn.cursor()

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

    def get_humidity(self):
        try:
            cursor = self.conn.cursor()

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

    def get_luminosity(self):
        try:
            cursor = self.conn.cursor()

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


