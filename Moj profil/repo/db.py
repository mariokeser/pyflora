# Nakon što smo ovo napravili u my_profile.py, napravili smo podfolder repo, potrebni __init__.py i spremili u poseban file ovu funkciju
import sqlite3 

#spremi  u bazu podataka,za bazu prvo moramo dohvatiti konekciju na bazu zato smo funkciju nazvali get_connection
# s parametrom db_name dali smo funkciji putanju, mogli smo dati i neko ime na neko ime na nekom drugom serveru
def get_connection(db_name): 
    try:
        conn = sqlite3.connect(db_name) # spojili smo se na bazu podataka sqlite3 sa .connect(i predamo putanju), spojili smo se na bazu db_name

        cursor = conn.cursor()# pomoću .cursor() na conn-konekciji, postavimo cursor na bazu, dolje ide daljnji redoslijed kreiranja
        # napravili smo kolone u tablici unutar funkcije(pokazano prije kako se kreira) s potrebnim podacima koji su navedeni u funkciji save_db
        # cursor se executa da se napravi tablica
        # stvori tablicu ako ne postoji
        cursor.execute(""" CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY,                      
        name TEXT NOT NULL,
        photo_filename TEXT NOT NULL,
        skills TEXT NOT NULL);""")
     
        conn.commit() # nad konekcijom napravimo .comit() da završimo tablicu
        cursor.close() # moramo zatvoriti cursor, radili smo to i prije
        return conn #vratimo konekciju da kasnije možemo nad tom konekcijom opet neke querye "ravnat" na bazu,to je kao "lokalna varijabla" koja 
        # se mora returnat, vraćati iz funkcije??

    except sqlite3.Error as err: # kod sqlite3 postoji samo ta jedna vrsta erora
        print(f"ERROR: {err}")

# nakon što smo napravili funkciju za dohvaćanje konekcije get_connection moramo u našem programu i stvoriti konekciju
conn = get_connection("./pyflora/Moj profil/data/data.db") #u varijablu conn predamo funkciju za dohvaćanje konekcije i predamo putanju do baze
# i sad imamo konekciju nad bazom-data.db smo nazvali našu bazu padataka

#i nakon toga pravimo funkciju save_db, prvo dohvaćamo konekciju nad bazom-get_connection, pa spremamo vrijednosti u bazu sa save_db
def save_db(conn, photo_filename, name, skills):#predamo joj konekciju-conn,i predamo joj argumente koje smo napravili u tablici get_connection
    try:
        cursor = conn.cursor() # dohvaćamo cursor da možemo bili što izvršiti
# zato što u ovom zadatku želimo izbrisati stare vrijednosti i dodati samo nove, prvo ćemo delete sve iz baze, executati ćemo query koji
# će SVE  deletetati iz tablicu nazve User 
        # izbriši sve što se nalazi u tablici
        #cursor.execute("DELETE FROM User")
        # spremi redak u tablicu
        cursor.execute("""INSERT INTO User (name, photo_filename, skills)
        VALUES(?,?,?);""", (name , photo_filename, skills)) #dodajemo novog usera,insertamo query,dodali smo redom vrijednosti u kolone, tim redom 
#želimo insertati VALUES-?-wildcardovi,pa ćemo poslije mijenjati te vrijednosti,te smo VALUESE popunili u nastavku querya s parametrima u tuple-u
        conn.comit() # bez comit() nad konekcijom nećemo ništa vidjeti na bazi, 
         
    except sqlite3.Error as err: # kod sqlite3 postoji samo ta jedna vrsta erora
        print(f"ERROR: {err}")
    finally:
          cursor.close() #u finally da zatvori program,ako nešto gore faila da ga ipak zatvori,jer nam ne treba ništa vratiti iznutra,dovoljno je 
                        # samo da se spremi unutra            
# kad smo napravili funkcije za bazu podataka get_conection i save_db i pokrenuli program,stvorila se data.db i u Dbeaveru pokazale su se kolone


# kad smo ovu funkciju prebacili ovdje, nazvali smo ju umjesto save_db()- samo save(), valjda zato što je sad u db.py
# nakon toga smo u my_profile.py napravili from repo import csv, json, db- da se ovi moduli mogu odavdje tamo importirai

def get_connection(db_name): 
    try:
        conn = sqlite3.connect(db_name) 

        cursor = conn.cursor()
       
        cursor.execute(""" CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY,                      
        name TEXT NOT NULL,
        photo_filename TEXT NOT NULL,
        skills TEXT NOT NULL);""")
     
        conn.commit() 
        cursor.close() 
        return conn 
    except sqlite3.Error as err: 
        print(f"ERROR: {err}")


conn = get_connection("./pyflora/Moj profil/data/data.db") 

def save(conn, photo_filename, name, skills):
    try:
        cursor = conn.cursor()
       
        #cursor.execute("DELETE FROM User")
     
        cursor.execute("""INSERT INTO User (name, photo_filename, skills)
        VALUES(?,?,?);""", (name , photo_filename, skills)) 

        conn.commit()     
    except sqlite3.Error as err: 
        print(f"ERROR: {err}")
    finally:
          cursor.close() 