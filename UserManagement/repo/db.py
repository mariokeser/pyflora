
import sqlite3
# kad stavim pokazivač na funkciju i dok držim command na tipkovnici i kliknem ljevim mišom na tu funkciju onda mi pokaže gdje je ta funkcija 
#napravljena, a kad isto to kliknem na funkciju gdje je napravljena onda mi pokaže gdje se sve ta funkcija koristi i ako se koristi na više
# mjesta pokaže sva ta mjesta
# kad isto tako kliknem na varijablu isto tako prebaci na mjesto gdje je napravljena, a kad kliknem tamo gdje je napravljen pokaže na sva mjesta
#gdje se koristi

# query smo napravili posebno u varijabli pa se pozvali na nju/njega u funkciji-get_connection()-query za get_connection
#query za napraviti tablicu baze podataka nazvanu Users,naziv kolone je malim slovima,a karakteristike vrijednosti u njima su velikim slovima
#query za stvaranje inicijalne tablice, kad u priijavi upišemo dva put isti username, neće se opet upisati u bazu jer smo naveli da je UNIQUE
create_table_query = """CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);"""


#Izvršavamo neki query nad bazom koji će nam dati dohvatiti usera s tim username-om-to je query za funkciju get_user()-kojom dohvaćamo userse
# Selectali(read,tražili) smo iz ovog querya username i password pa nek  vratimo oboje
# ovo dolje znač: SELECT(dohvati) username, password(te dvije kolone) FROM(iz)  Users(tablice)
#WHERE dio zato što želimo dohvatiti konkretnog usera sa ovim username-om( ovim-znači username postavljen u funkciji get_user())
#WHERE(gdje)odnosi se na konkretnu kolonu(uvjet) koju u ovom slučaju SELECT-amo u queryu
#WHERE(gdje) username(ime kolone) =(jednako) ?(upitnik-wildcard je da tu možemo injecati bilo koji username kasnije,da ne moramo svaki put novi 
#string upisivati unutra, umjesto upitnika može ići i konkretni string(ime) od username-a)
#ovaj query će dohvatiti sve usere koji imaju ovaj tu username, odnosno dohvatiti će sve retke iz tablice koji imaju kolonu username postavljene na
#vrijednost koju mu damo umjesto napisanog upitnika, (WHERE uvjet;-znači - WHERE kolona=nešto;-ovdje- WHERE username=?)
select_query = """SELECT username, password FROM Users
WHERE username = ?;"""

# query za funkciju add_user- za inicijalno dodavanje usera u bazu, za dodavanje admina
# INSERT(dodaj) INTO(u) Users(bazu, tablicu) (username, password)-(koriničko ime, lozinka), id nismo dodali jer se on inkrementa(doda) sam
#VALUES(vrijednosti) (?, ?) -u upitnike values se dodaju se vrijednosti točno ovim redom kojim smo upisali u tablicu Users(usernama, password)
insert_query = """INSERT INTO Users (username, password)
VALUES (?, ?);"""
#query za dohvacnje svih usersa, koji nisu admin, za funkciju get_all_usernames
#kažemo SELECT(dohvati) username(korisničko ime) FROM(od) Users(baza, tablica)
# tražimo po username da dobijemo samo username, da smo stavili * onda bi dobili sve kolone
select_all_query = """SELECT username FROM Users""" 

# query za funkciju delete_users
#Delete(izbrisi) FROM (od) Users(baza)
#WHERE(gdje) username (korisničko ime)=? ovdje sa where kažemo kojeg usera da izbriše, usera sa username kojeg mi damo 
#ali nismo upisali konkretnog već sa upitnikom kako bi mi na ovaj query mogli dodavati različite username za delete
delete_query = """DELETE FROM Users
WHERE username = ?"""


#query za promjenu lozinke, koristimo UPDATE  naredbu za promjenu vrijednosti kolone u bazi-
#  u materijalima programiranje od str 60 sve je objašnjeno, uz UPDATE(ažuriraj)  ide i SET(postavi) i WHERE(gdje, u koju kolonu)
#UPDATE(ažuriraj) Users(bazu)
#SET(postavi) password(lozinku) jednako na novi pass-?
#WHERE(gdje je) username(korisnik) jednako netko-?
# kod update kolone se postavljaju obrnutim redom nego su postavljene kod kreiranja tablice, tamo je bilo username,password, ovdje je obrnuto
update_query = """UPDATE Users 
SET password = ?
WHERE username = ?"""




def get_connection(db_name):#pravimo konekciju na bazu i bazu,damo neko ime za bazu,baza je nazvana u user_management.py-Users.db-u conn varijabli
    try:
        conn = sqlite3.connect(db_name) # dohvaćamo/stvaramo konekciju na db_name pomoću sqlite3, spajanje na bazu

        cursor = conn.cursor() #cursor nad konekcijom mora biti idući korak,sve querye koje želimo executat nas bazom, executat ćemo nad cursorom

        # ako tablica Users ne postoji, kreiraj ju
        cursor.execute(create_table_query) #onda sa cursorom execute query koji smo napravili,ili bi tu napravili tablicu
        conn.commit() # i idući korak je .commit() da se stvori tablica u bazi
#u get_connection stvaramo konekciju na bazu i tablicu u istoj i dodajemo admina u bazu, koji je prvi, inicijalni user
#ako korisnik "admin" ne postoji u bazi,dodaj ga-ako je u get_user(koja dohvaća usera),kad se istoj preda conn i username-kako su u njoj navedeni
        if get_user(conn, "admin") == None: # parametri-ako je username("admin") jednak None(ako ga nisi dohvatio)-onda ga dodaj unutra s add_user
            add_user(conn, "admin", "admin")# nakon što smo s .commit() stvorili tablicu, idemo nakon toga stvoriti usera, pa pozovemo funkciju
#add_user koja je za dodavanje admina i predamo konekciju i predamo username i password u stringu-kako su i navedeni parametri u funkciji add_user
# a ako nije jednak None, ako postoji, nećemo ga dodavati preko funkciije add_user
        cursor.close() # moramo za kraj zatvoriti cursor

        return conn # i moramo vratiti van konekciju, jer nije globalna varijabla???
    except sqlite3.Error as err: # jedini error u sqlite3, ako bude error da ga pokaže
        print(f"ERROR: {err}")

# nakon što smo dohvatili bazu, sad moramo dohvatiti i usera(username) i konekciju na bazu iz get_connection()-za dohvaćanje usersa
# zato što je funkcija koja dohvaća usera, moramo predati parametar username i prije toga konekciju na bazu iz koje uzimamo username
def get_user(conn, username): #dohvaćamo usera,damo konekciju i username,da znamo password kojeg usera da nam dohvati funkcija-oboje iz get_connection
    try:  #conn smo dohvatili u get_connection(),a username je kolona u tablici create_table_query koja je executana u get_connection()
        cursor = conn.cursor()#za executanje querya ćemo uvijek stvoriti cursor sa konekcije, konekciju smo predali cursoru kao argument
#s cursor.execute executamo query napravljen za dohvaćanje usera sa username-,predali smo query i dali argument username u tuple(mora imati zarez)
        cursor.execute(select_query, (username, ))#-time smo popunili upitnik(kod WHERE) iz tog querya,da zna konkretne vrijednosti, po kojima će
# tražiti(queryjevati),ovo iznad će dohvatiti sve usere sa username koji smo zadali
        record = cursor.fetchone()#.fetchone()-rekli smo nemoj dohvatiti sve već samo jednog,odnosno listu prvog usera,ako postoji,ide nad cursorom
 #ima i naredba nad cursorom .fetchall() koja bi dala listu svih redaka koji bi vratio ovaj query nad bazom, .fetchone() je dovoljno jer
 # smo u tablici naveli da je username UNIQUE- znači i ima samo jedan
#taj jedan element dohvaćen sa .fetchone() je ili NULL ili su nam to vrijednosti iz tablice, NULL je ako ne postoji taj redak,
# username i password su postavljeni na NOT NULL, zato pitamo ovo dolje
        if record != None: # ako record(taj dohvaćeni element) nije None, ako je različit on None
            return (record[0], record[1]) # vrati username i password koji su elementi u recordu(listi) record[0]-username, i record[1]-password
        else:                       # u select_query tražili smo(selectali) 2 elementa ovim redom username[0] password[1]
            return None # inače vrati None, znači nema tog usera
    except sqlite3.Error as err:
        print(f"ERROR: {err}")
    finally:  # kod finally zatvaramo cursor, da se zatvori u svakom slučaju bio error ili ne
        cursor.close()


#da bi se mogli ulogirati kao neki user, moramo prvo,inicijalno dodati(spremiti) nekog usera unutra,u bazu,za dodavanje admina-prvog usera
def add_user(conn, username, password):# predamo konekciju na bazu, username i password-sve što user ima za login
    try:
        cursor = conn.cursor() # uvijek prvo cursor nad konekcijom

#ako username vec postoji u bazi(jer je označen kao UNIQUE),ne možemo ga dodati ponovno i onda bi nam baza javila error u except-u,
# da to izbjegnemo, napravili smo ovo ispod, ovim prvo provjeravamo da li user već postoji u bazi,ako postoji ne želimo ga/ne možemo dodati
        if get_user(conn, username) != None:#ako je funkcija get_users(dohvaća usere,pitamo s njom) različita od None,znači da već postoji taj user
            return False  #vrati False,s False spriječili smo executanje ispod, user već postoji u bazi i nisam ti dodao novog usera

        cursor.execute(insert_query, (username, password)) #onda executamo cursor i dodamo naš insert_query i njemu damo vrijednosti u tuple
#a to su ove koje smo predali tom insert_query kad smo ga gore napravili, one popunjavaju wildcardove koje smo dali u VALUES, kad pozovemo
# ovu funkciju pozvati će se ovaj query i username i password koji smo predali funkciji, zaljepiti će se na mjesta umjesto upitnika i takav
# će se query pozvati nad bazom
        conn.commit() # .commit() mora ići uvijek nakon execute-a cursora
# funkcije vraćaju True ili False-da li je operacija uspjela ili nije
        return True #zato smo dali ovaj return True, koji znači user ti je uspješno unesen u bazu, dopušta da operacija uspije
    except sqlite3.Error as err:
        print(f"ERROR: {err}")
        return False # kod excepta smo dodali return False-znači operacija nije uspjela, nisi uspio dodati usera unutra
    finally:
        cursor.close()

# funkcija za dohvaćanje usersa koji nisu admin u bazu
def get_all_usernames(conn): # funkciji za bazu moramo uvijek predati konekciju nad bazom-logično
    try: 
        cursor = conn.cursor() #dohvatimo cursor na konekciju

        cursor.execute(select_all_query) # execute query

        records = cursor.fetchall() # dohvaćamo na cursoru sve što nam vrati query, sve username

        usernames = [] # sad ćemo sve username skupitiu jednu listu, prvo napravimo praznu
        for record in records: # for petljemo izlistavamo sve username skupljene u records
            usernames.append(record[0])#u listu appendamo record na 0, redords[0]-na elementu 0 su username,jedini koji tražimo u select_all_quert

        return usernames # za kraj vraćamo varijablu/listu usernames
    except sqlite3.Error as err:
        print(f"ERROR: {err}")
    finally:
        cursor.close() # u finally dodamo zatvaranje cursora


# brisanje usera iz baze
def delete_user(conn, username): # predamo konekciju i username, jer za brisanje usera je dovoljno da znamo username
    try:
        cursor = conn.cursor() # dohvaćamo cursorn
#prije brisanja pitamo da li user postoji u bazi, tu ćemo iskoristiti funkciju za dohvaćanje usera
# ako je get_user(conn, username)-uvijek moramo predati konekciju na bazu i username-jer smo naveli da je on unique pa preko njega radimo sve
# sa ovim dolje pitamo DA LI username NE postoji u bazi
        if get_user(conn, username) == None: # ako je username jednako None, znači da ne postoji u bazi i onda je greška
            return False # kad ne postoji onda damo return False-time se vratimo iz funkcije i ne napravimo query nad bazom,
#a kad postoji(nije jednak None) onda ćemo izvršiti query nad bazom i nakon toga damo return True-operacija je uspjela
        cursor.execute(delete_query, (username,)) #execute cursor na query-damo mu query i argument za query, a to smo u where postavili da je
        #username, element za query je uvijek tuple i kad je element u tuple jedan mora iza ići zarez i razmak-da se razlikuje od liste

        conn.commit() # i izvršenje na bazi

        return True # ovaj return je povezan sa if-om gore, i znači da user po username postoji i da je uspješno izbrisan, operacija je uspjela
    except sqlite3.Error as err:
        print(f"ERROR: {err}")
    finally:
        cursor.close()

# funkcija za promjenu passa u bazi, iza conn parametri su postavljeni redom kojim su postavljeni u update_query, u add_user je bilo postavljeno
# username, password, a ovdje je obrnuto jer tako ide zadani query
def update_password(conn, new_password, username, ):# moramo joj dati conn,novi pass,username-parametre
    try:
        cursor = conn.cursor() # postavi cursor
# prvo pitamo DA LI user NE POSTOJI u bazi pomoću funkcije za dohvaćanje usera, ako ne postoji onda vrati False, izađi iz funkcije
        if get_user(conn, username) == None:
            return False # return False nije vezan za dolje return True
#ako nije False executamo cursor na query-predamo ga u cursor i damo argumente postavljene u tom queryu u tuple-u(SET je new_password, WHERE je username)
        cursor.execute(update_query, (new_password, username))# po tim argumentima izvršavamo njihov query, u executanju query promjenili smo
        #useru s tim username password na novi password, i redoslijed argumenata mora biti isti kako su postavljeni u query

        conn.commit() # commit zatvori

        return True #vratimo True da smo uspješno izvršili operaciju, nije vezano za return False iznad
    except sqlite3.Error as err:
        print(f"ERROR: {err}")
    finally:
        cursor.close()

# u def_update password umjesto rješenja sa update_query možemo remove username i na njegovo mjesto dodamo novi username,
# budući da nema queryvanja onda nam ne treba ništa u vezi cursora-znači cursor je za executanje upita query nad bazom, naime
# te funkcije već imaju svoje cursore u sebi, ali tu se mijenja id od username-a

"""def update_password(conn, username, new_password):
    try:
        if get_user(conn, username) == None:
            return False
# samo ubacimo napravljene funkcije za brisanje i dodavanje usera, jedino u add_user umjesto parametra password predamo new_password
        delete_user(conn, username)
        add_user(conn, username, new_password)
 
        return True
    except sqlite3.Error as err:
        print(f"ERROR: {err}")"""
    