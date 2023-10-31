import sqlite3 # služi za  stvaranje konekcije na bazu, stvaranje baza 
import datetime # importali smo za dodavanje modula u querye
#moramo stvarati tablice za bazu, tablice radimo preko query-a, za svaki rad sa bazom trebamo neki query koji sa cursorom execute u 
#metodama nad klasom/funkcijama

#pravimo query za tablicu za spremanje u bazu vrijednosti temperature, pravimo tablicu imena temperature
# napravljene su kolone s njihovim obilježjima,read_time će biti neko vrijeme zapisa,da možemo sortirat kojim redom želim dohvatiti temperature
#kad ću ih dohvaćati(DATETIME-tip u sql-u za sortirat stvari po vremenu u obliku datum pa vrijeme,mogli smo to spremati i kao string, vjerojatno bi 
#se onda umjesto DATETIME upisalo STRING? ),  value će biti vrijednost dohvaćene temperature
create_temperature_table_query = """CREATE TABLE IF NOT EXISTS temperature (
    id INTEGER PRIMARY KEY,
    read_time DATETIME NOT NULL,
    value FLOAT NOT NULL
)"""
# ovdje dodajemo tlakove u query, stvar je ista kao za create_temperature_table_query
create_pressure_table_query = """CREATE TABLE IF NOT EXISTS pressure (
    id INTEGER PRIMARY KEY,
    read_time DATETIME NOT NULL,
    value INTEGER NOT NULL
)"""
# query za tablicu za humidity, istakao i prethdne
create_humidity_table_query = """CREATE TABLE IF NOT EXISTS humidity (
    id INTEGER PRIMARY KEY,
    read_time DATETIME NOT NULL,
    value INTEGER NOT NULL
)"""
#pravimo query kako da insertam tempearturu, za to služi INSERT INTO,  insertamo u tablicu koju smo stvorili u get_connection
#insertamo u read_time, value kolone(tim redom se mora insertati), sa VALUES se insertaju te vrijednosti preko placeholdera (?, ?) pa te
#upitnike popunjavamo u funkciji kojoj predamo query
insert_temperature_query = """INSERT INTO temperature (read_time, value)
VALUES (?, ?)"""
#query za insert tlakova, isti način kao za insert_temperature_query
insert_pressure_query = """INSERT INTO pressure (read_time, value)
VALUES (?, ?)"""
#query za insert humidity, isto kao ovo prije
insert_humidity_query = """INSERT INTO humidity (read_time, value)
VALUES (?, ?)"""

# ove naredbe smo napravili u pythonu kako bi ih mogli preko funkcija u client.py dohvaćati u terminalu
#query za izbor temperature,u query samo prepisali naredbu iz sqla, ide sve pod trostruke navodnike, SELECT value-dohvati vrijednost FROM
#temperature(tablica za temperaturu),znači dohvati vrijednost od temperature,ORDER BY(posloži po) read_time(vrijeme čitanja temperature)
#DESC(descending- znači od najnovijeg očitanja),LIMIT 1, znači samo jednu vrijednost da prikaže. Sql naredbama smo prošli po kolonama
#tablice temperature- da dohvati vrijednost iz temperature, posloženu po vremenu čitanja, od najnovijeg/zadnjeg očitanja, samo jednu.
select_temperature_query = """SELECT  value FROM temperature
ORDER BY read_time DESC
LIMIT 1"""
# isto vrijedi i za ova druga 2 querya
select_pressure_query = """SELECT value FROM pressure
ORDER BY read_time DESC
LIMIT 1"""

select_humidity_query = """SELECT value FROM humidity
ORDER BY read_time DESC
LIMIT 1"""

# klasa za bazu, database, za stvaranje konekcije na bazu
"""
class DbClient: 
    def __init__(self, db_name): # njezin konstruktor, predali smo joj parametar db_name koji će služiti za  ime baze na koju će se ići
        self.db_name= db_name #napravio na početku,predao njezin parametar u varijablu self.db_name,self. znači da je db_name postavljen u klasu
        self.conn = self.get_connection()# nakon try blocka gdje smo stvorili i returnali konekciju u metodi get_connection, onda smo ovdje
#sa self.conn postavili u konstruktor novu varijablu conn kojoj smo predali metodu za dohvaćanje konekcije nad bazom get_connection() i njoj smo
#morali dati self.- sve što se postavlja u konstruktor  klase mora imati self. self.conn je sad konekcija koja je spremljena u atribut klase i služiti
#će za dohvaćanje get, save temperature idr, bez da gui i main() znaju za to, gui samo zna da ima klijenta(db_client) gdje može zvati 
#get, save temperature idr., main() samo zna može stvoriti klijenta i dati mu ime baze db_client=repo.DbClient("data/readings.db"), a klijent-
#db_client će odraditi stvaranje konekcije i save-anje svega što treba
        
#metoda nad klasom za dohvaćanje konekcije nad bazom,nazvali smo ju get_connection,ona samo dohvaća konekciju i spremljena je u konstruktoru gore
    def get_connection(self): #postavljena na self da bi vrijedila u ovo klasi,ali zato druge stvari u metodi da bi vrijedile u metodi ne moraju
        #imati self, kao što je ovaj conn, imamo self.db_name jer je tako postavljen u konstruktor klase kao self.db_name
        try:   # ovo je try, except block, pravimo sa conn= konekciju
            conn = sqlite3.connect(self.db_name) #na conn dajemo modul za bazu.connect(njegova funkcija za konekciju) i ime varijable za bazu
#koju smo postavili u klasu DbClient- self.db_name

            return conn # returnamo dobivenu konkeciju, kako bi se ova metoda mogla koristiti u self.conn gore u klasi
        except sqlite3.Error as err:  # ako nije uspjela konekcija nek pod exceptom javi kao err sqlite3.Error
            print(f"ERROR: {err}")

# nakon ovoga gore, onda je napravio promjene u DbClient, zato što ne moramo spremiti u konstrukt klase parametardb_name-jer je potreban samo za 
# konekciju pa je izbacio db_name iz konstrukta klase i napravio slijedeće promjene

class DbClient:
    def __init__(self, db_name):# predan je parametar db_name koji će služiti za ime baze na koju ćemo dati konekciju
        self.conn = self.get_connection(db_name)# nakon return conn u get_connction postavili smo ovu metodu za konekciju nad bazom sa
#self. jer se postavlja u konstrut, predali smo joj db_name iz inita klase DbClient i predali na novu varijablu conn sa self. jer se predaje
#u konstrukt baze, tako samo argument klase iz inita db_name iskoristili da napravimo preko ove klase konekciju na bazu, bez da spremamo taj
#argument kao atribut u konstrukt klase, jer je potreban samo za konekciju, ali nije potreban za ništa drugo u samoj klasi.
# primjenjujemo metodu nad klasom u klasi jer smo ju predali u konstruktor klase

    def get_connection(self, db_name): # prvo smo napravili metodu za konekciju, dali smo ime za konekciju nad bazom -db_name
        
            try:   
                conn = sqlite3.connect(db_name)# tu pravimo konekciju na bazu i predajemo argument db_name iz get_connection metode

                return conn # returnamo konkeciju da ovu metodu za konekciju možemo postaviti u konstrukt klase i to je idući korak 
            except sqlite3.Error as err: 
                print(f"ERROR: {err}")
"""
class DbClient:
    def __init__(self, db_name):
        self.conn = self.get_connection(db_name)
#query za tablicu baze podataka se uvijek stavlja u get_connection
    def get_connection(self, db_name):
        try:
            conn = sqlite3.connect(db_name) # conn bez selfa jer je samo u metodi

            cursor = conn.cursor() # pokrenili smo cursor nad konekcijom za stvaranje baze

            cursor.execute(create_temperature_table_query)# na cursor.execute poziva se query
            cursor.execute(create_pressure_table_query) # dodali smo i ovaj query za tablicu tlaka if not exists
            cursor.execute(create_humidity_table_query)# stvorili tablicu

            conn.commit() # na konekciji se mora napraviti .commit() da se na konekciju napravi tablica baze 
# sad kad smo vraćali konekciju na bazu da se može koristiti u konstruktoru klase App, kad vraćamo konekciju inicijalizirati ću i bazu, odnosno
#ako ne postoji stvoriti ću tu bazu, to se radi preko cursora
            return conn
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
        finally: # u finally ćemo zatvoriti cursor, i ako se dogodio error nek se closa cursor, tome služi finally
            cursor.close()

#nakon što smo napravili get_connection na bazu,kad imamo bazu, pravimo u klasi metodu  za spremanje vrijednosti (value)tempa u bazu
    def save_temperature_reading(self, value):# value je temp koji želimo spremiti, trebamo query za insertanje tempa u bazu
        try:
            cursor = self.conn.cursor() # sa cursorom pokrećemo konekciju, to je sad self.conn jer je sad conn spremljen u konstruktor
#executamo query sa cursorom, u query predajemo vrijednosti koje smo naveli u query: read_time, value, predaju se na mjesto VALUES(?,?)
            cursor.execute(insert_temperature_query, # gdje umjesto ?, sada popunjavamo sa konkretnim VALUES
                           (datetime.datetime.now(), value))# na mjesto prvog ?(read_time) dali smo modul za vrijeme(učili smo te module prije-
#datum,vrijeme)na mjesto drugog ? u query(value),dali smo parametar value iz ove funkcije-koja je napravljena za spremanje vrijednosti tempa u bazu
            self.conn.commit() #self.conn se mora -commit() za izvršenje
        except sqlite3.Error as err: #except i finally standardno
            print(f"ERROR: {err}")
        finally:
            cursor.close()
# funkcija za save_pressure je ista kao za save_temperature_reading.
# kad otvorim bazu u dbeaver i otiđem na tablicu za temperaturu i otvorim sql editor i tamo na automatski postavljeni SELECT na temperature
#umjesto temperature upišem pressure,pokaže mi tablicu od tlaka
    def save_pressure_reading(self, value): 
        try:
            cursor = self.conn.cursor()

            cursor.execute(insert_pressure_query,
                           (datetime.datetime.now(), value))

            self.conn.commit()
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
        finally:
            cursor.close()
#save_humidity ista kao prethodne funkcije
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
# sad pravimo metode u DbClient-koji ima bazu svih podataka za dohvaćanje querya koji služe za dohvaćanje vrijednosti iz baze
    def get_temperature(self): # ovdje ne treba value, jer ga imamo preko metoda gore, ovdje ih sad samo dohvaćamo
        try:
            cursor = self.conn.cursor()#otvorimo cursor na konekciju

            cursor.execute(select_temperature_query) # executamo cursor na query za select temperature, ovdje ne commitamo na bazu,jer već imamo
#podatke u njoj, već sad moramo fećati/dohvaćati sa baze, zato smo stvorili varijablu record i njoj preko cursora dali metodu .fetchone()
            record = cursor.fetchone() # fetchone je metoda od cursora-koji nam je potreban za izvršavanje akcija na bazi, sa fetchone dohvaća
            #se samo jedna vrijednost/to nam i treba,fetchone daje vrijednosti u obliku tuple
# teoretski se može dogoditi da fetchone ne dohvati ništa/ne postoji ni jedna vrijednost, zato pitamo
            if record != None: # ako je record različit od None/nešto je dohvatio
                return record[0] #onda vrati record na 0, imati će samo jednu vrijednost u tuple i to je ta na nultom indeksu
            else: 
                return None # inače neka return/vrati None, znači da nema ništa
        except sqlite3.Error as err:
            print(f"ERROR: {err}")
        finally:
            cursor.close()
#isto je za dohvaćanje tlaka i vlažnosti
    def get_pressure(self):
        try:
            cursor = self.conn.cursor()

            cursor.execute(select_pressure_query)

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


