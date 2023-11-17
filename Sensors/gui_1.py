import tkinter as tk

#klasa App, služi za stvaranje tkinter prozora u kojem ćemo prikazivati stvari iz baze podataka, napraviti ćemo sense_emu simulator na kojem će se 
#prikazivati vrijednosti koje ćemo dohvaćati kao što je temperatura, vlažnost i dr.
#sa def__init__(self, db_client)- aplikacija očekuje u kontruktoru jedan argument-db_client da mogu spremati stvari u bazu, zato što će ova
#aplikacija imati u sebi neke simulatore senzora i htjet ću ih upisivati u bazu, da bi mogao upisivati u bazu treba mi klijent za bazu
#db_client da bih mogao upisivati stvari unutra, db_client je neki objekt preko kojeg mogu pristupati bazi, ne zanima nas kao se ta baza zove
#bitan nam je samo pristup njoj i to je preko db_client i tako će tkinter App prikazivati podatke iz baze
"""
class App(tk.Tk): # naslijedila je klasu Tk i naša aplikacija postaje primjerak klase Tk
    def __init__(self, db_client):#njezin konstruktor,u gui aplikaciju dali smo db_client-to će biti klasa za bazu podataka DbClient iz repo.py
        #koju će predati u simulator.py kad napravimo db_client = repo.DbClient("data/readings.db") i app = gui.App(db_client) u def main()-
# u def mainu() u simulatoru.py povezali smo ovaj class App i class DbClient bazu podataka i tamo je mainloop za prikazivanje svega u prozoru
        super().__init__() # super() zbog naslijeđivanja tkinetra, da nema ovog super(), Tk se ne bi inicijalizirao, App ima sve iz Tk plus još
        #neke svoje stvari kao što je ovdje self.db_client = db_client

        self.db_client = db_client # postavili smo taj argumjent db_client u ovaj gui App sa self.db_client-varijabla u samoj klasi,
        #primio sam klijenta

        self.title("Sense Simulator") # dali smo gui aplikaciji title i veličinu prozora,sve ide na self. jer je klasa
        self.geometry("500x300")
# na početku izrade gui aplikacije počeo je ovo ispod prvo stavljati u ovu class App
#prvo smo napravili Lalbel koji će nam ispisati o kojoj se vrijednsti radi,Label smo stavili u self(konstruktor klase),text koji će label pokazivati
        tk.Label(self, text="Temperature(°C)").grid(column=0,row=0) #i s grid postavili smo da se temperature prikaže na 0-početna pozicija   
#dodajemo varijablu između labela i scl_temp pa da preko nje uzimamo stvari, s tk.IntVar pravimo varijablu/widget za prikaz/upis integera 
        #self.var_temp = tk.IntVar(self, 20)#value smo postavili na 20,to je početni value koji će pokazivati,value je optional i defaultno od 0
# odlučili smo da se temperatura u slideru pokazuje kao float number, za pokazivanje floata koristi se tk.DoubleVar
        self.var_temp= tk.DoubleVar(self, 20)
#sad dodajemo slider ispod labela, SVE što se postavlja u konstruktor klase, u klasu da vrijedi za nju mora imati self        
        self.scl_temp = tk.Scale(self,from_=105, to=-30,resolution=0.5,tickinterval=135,length=250,variable=self.var_temp)#sa tk.Scale postavlja 
#se slider,postavili smo ga od-do,od se piše from_=,svi parametri, se moraju odvojiti zarezom,do se piše to=,sa variable=u slider smo 
#postavili IntVar varijablu-pokazuje value,u njoj smo odredili smo da je početni value 20,kad pokrenemo gui pokaže se slider na vrijendosti 20 kako
#smo početno odredili u IntVar varijabli koja je predana u tk.Scale i sa mišom se može pomicati od -30 do 105 kako smo odredili u s tk.Scale,
#Scale/slider je po defaultu okomit,u njega se može upisati orient=tk.HORIZONTAL i onda će biti vodoravan, from_=vrijednost je gore u slideru,
# to=upisana vrijednost je dolje u slideru, kad je slider okomit/vertikalan, kad smo odlučili da se temp u slideru pokazuje kao float, onda
#smo u tk.Scale morali ubaciti i resolution=0.5, znači da pokazuje float number po 0.5, sa lenght=povećali smo duljinu slidera,
#s tickinterval=mogu se staviti svakih koliko da nam pišu vrijednosti pored slidera,kad smo stavili 10 pored slidera su se pokazali brojevi od
#105 do -25,svakih 10 su se vidjele vrijednosti(brojevi) pored slidera-piše koja je temperatura gdje,sa 135 vidi sa samo najveća(105) i najmanja(-30)
        self.scl_temp.grid(column=0,row=1)# slider smo gridali da se pokaže red ispod Labela
#ispod smo na slider stavili da se s .after nakon sekunde napravi funkciju print_temperature, sa self. postavljena je u konstruktor App-a
        self.scl_temp.after(1000, self.save_temperature)
#ova funkcija je da ispisujemo temperaturu
    def save_temperature(self):
        #print(self.var_temp.get())# za ispis IntVar varijable koja pokazuje temperaturu/value, s .get() se dohvaća temp/value te varijable
        self.db_client.save_temperature_reading(self.var_temp.get())#pozvali smo db_client iz ove klase,na njega smo pozvali metodu za spremanje 
#tempa u bazu iz DbClient klase koja je predana ovom self.db_clientu i metodi smo dali vrijednost(njezin value)-ovdje stvorena var za temp
        self.scl_temp.after(1000, self.save_temperature)#onda opet pozovemo istu stvar,kako bi radio ispis temp svake sekunde-napravljena je petlja
# kad smo u simulator.py pozvali da se pokaže prozor sa temperaturom, svake sekunde se u terminalu pokazivala temp, kako smo micali slider
#na prozoru, tako se promjena tempa pokazivala u terminalu i svake sekunde se pokazivala ta nova temp.
#umjesto ovog printanja tempa ovdje, možemo pozvati db_client iz ove klase i samo spremiti temp u db_client ove aplikacije, a on je u main()
#predan u app = gui.App(db_client), a prije toga u main() stvorili smo taj db_client na bazu preko db_client = repo.DbClient("data/readings.db")
#DbClient je klasa u repo.py koja je napravljena za doći do baze i spremiti sve te stvari, onda je zbog toga promjenio funkciju print_temperature,
#i preimenovali ju u def save_temperature() i sad umjesto da se temp ispisuje u terminalu, spremili smo ju u bazu, kad upalimo simulator, otvorimo
#sglite, nađemo readings.db, otiđemo na tablicu temperature,na view data i pokažu se tempovi u tablici, sa vremenom i id-em, kad pomaknem na 
#simulatoru temp i na tablici temperature- napravim refresh, onda se pokažu i ti novi tempovi, koji se update svake sekunde.
# Kad u dbeaver otiđem pod tablicom temperature na read data in SQL editor onda mi se iznad tablice temperature pokaže prostor za uređivanje
# temperaura pomoću naredbi u editoru, napisali smo ORDER BY read_time(kolona tablice) DESC(descending) LIMIT 10, i onda su se prikazivala vremena 
#od  najnovijih prema starijim samo njih 10 zadnjih, meni nije radilo jer samo imao ; poslije FROM temperature u editoru
#Onda smo nakon temperature išli na isti način dodati i tlak i vlažnost zraka na isti način. Obzirom da imamo više istih stvari, napravili
#smo novu klasu za Scale/slider i Label gore- to je class Slider, kad smo radili class Slider onda smo odavde prebacili tk.Label i tk.Scale
"""
class App(tk.Tk):
    def __init__(self, db_client):
        super().__init__()

        self.db_client = db_client

        self.title("Pyflora Simulator")
        self.geometry("500x300")              
# slider za temperaturu   
        self.var_temp = tk.DoubleVar(self, 20) # varijabla za pokazivanje value tempa kao float, početna vrijednost 20
        self.sld_temp = Slider(self,  # sa self.sld_temp = Slider(self) postavili smo klasu Slider u App za pokazivanje temperature
                               "Temperature (°C)", #title iz tk.Label, ovo ispod je iz tk.Scale, a sve je postavljeno u class Slider
                               -30, #from_ ,ne moramo nazivati vrijednosti po parametrima kad ih sve dajemo redom po konstruktoru klase 
                               105, #to
                               0.5, # resolution
                               250, # lenght, nismo stavili orientation jer smo stavili u konstruktor class Slider da je po defaultu vertical,
                               #on je u class Slider u tk.Scale postavljen kao zadnji
                               self.var_temp) #varijabla za prikaz broja, a .get() smo stavili na tu varijablu u funkciji save_temperature
        #kako bi se brojevi mogli prikazati u terminalu ili bazi, kako želimo,za prikaz na slideru nije potreban .get()
        self.sld_temp.grid(column=0, row=0) # gridanje slidera na poziciju da se može prikazati
        self.sld_temp.after(1000, self.save_temperature)# slider smo stavili da nakon sekunde pokrene funkciju save_temperature, koja je
        #napravljena ovdje ispod
# radimo varijablu i slider za tlak
        self.var_ph_value = tk.DoubleVar(self, 7) # stavili smo da je default obični atm tlak 1013
        self.sld_ph_value = Slider(self,
                                "pH_value (pH)",
                                1, #from
                                14,
                                0.5, # to, ovdje smo preskočili resolution koji je postavljen u class Slider na default 1,zato ga možemo preskočiti
                                length=250, #ali zato onda ove vrijednosti ispod resolutiona trebamo nazvati po njihovim parametrima iz
                                variable=self.var_ph_value) # konstruktora klase Slider
        self.sld_ph_value.grid(column=1, row=0) # pozicioniran da se pokaže pored slidera za temp
        self.sld_ph_value.after(1000, self.save_ph_value) # slider smo stavili da nakon sekunde pokrene funkciju save_pressure
#Na isti način smo dodali i vlažnost, varijablu i slider, i pokrenuli na slider funkciju sa .afetr
        self.var_hum = tk.IntVar(self, 50) # defaultb broj je 50
        self.sld_hum = Slider(self, # vrijednosti se postavljaju redom kako su navedeni parametri u konstruktoru klase
                              "Humidity (%)",
                              0, #from_
                              100, #to
                              length=250,
                              variable=self.var_hum) #postavili varijablu za prikaz value vlažnosti,kad pomičemo slider mijenjaju se brojevi u njoj
        self.sld_hum.grid(column=2, row=0)
        self.sld_hum.after(1000, self.save_humidity)
#dali smo da funkcija pozove db_client iz ove klase i da on pozove metodu za spremanje temperature iz class DbClient i njoj predali ovdje stvorenu 
    def save_temperature(self): #DoubleVar varijablu za pokazivanje floata i dali joj funkciju .get()-za return/dohvaćanje value float or integer
        self.db_client.save_temperature_reading(self.var_temp.get())
# i onda smo opet postavili slider za temp da nakon sekunde pokrene funkciju save_temperature i tako smo napravili da svake sekunde pokaže/upiše
#temperaturu u bazi DbClient
        self.sld_temp.after(1000, self.save_temperature)
# napravili smo save-anje tlaka, na isti način kao save-anje tempa, sa funkcijom kojoj iz clienta predamo metodu za spremanje tlaka u bazu i 
#njoj predamo ovdje napravljenu IntVar varijablu za pokazivaje integera i s funkcijom  .get() zovemo taj broj da ga pokaže u bazi
    def save_ph_value(self):
        self.db_client.save_ph_value_reading(self.var_ph_value.get())
# i opet smo pozvali slider da nakon sekunde pozove funkciju save_pressure i tako napravili da te vrijednosti stalno pokazuje svake sekunde
        self.sld_ph_value.after(1000, self.save_ph_value)
# napravili funkciju za dohvaćanje vlažnosti iz baze i njoj predali IntVar varijablu koja služi za upis inegera i s .get() da ih prikaže u bazi

    def save_humidity(self):
        self.db_client.save_humidity_reading(self.var_hum.get())
# s drugim pozivom slidera da pokrene funkciju za dohvaćanje vrijednosti vlažnosti iz baze,a između mora biti ta funkcija-pokazuje value svake sek
        self.sld_hum.after(1000, self.save_humidity)

# klasa za Scale/slider i Label koju ćemo u App ubacivati za svaki svaku vrijednost posebno temp, tlak i vlažnost
class Slider(tk.Frame): #naslijedili smo class tk.Frame 
    def __init__(self, #napravili smo konstruktor klase Slider koja je naslijedila tk.Frame, to su sve parametri koje nudi tk.Frame
                 master,
                 title, # title je iz tk.Label, dodali smo Label s naslovom
                 from_,
                 to,
                 resolution=1, # stavili samo da bude po defaultu 1 - integer
                 length=None, # stavili smo da default duljine bude None, kako bi mogli zadati duljinu izvana
                 variable=None,# isto None, ako želimo zadati vrijednost varijable izvana što smo i napravili 
                 orientation=tk.VERTICAL):# orijentacija smo stavili da bude default tk.VERTICAL
        super().__init__(master) # sa super() smo naslijedili klasu tk.Frame, master je od tk.Frame, zbog nečeg smo ga upisali ovdje i u 
        #konstruktor class Slider, valjda da class slider može koristiti master od tk.Frame, google što je master iz tk.Frame
# s ovim smo obrnuli pozicije max i min vrijednosti koje su stavljene u to i from_
        if orientation == tk.VERTICAL: #ako je orijentacije == tk.VERTICAL
            from_, to = to, from_ # zamjeni from_ i tu , from_, to je to, from_ from_ je otišao na poziciju to i to na poziciju from_
# pro smo prebacili iz App tk.Label, na text smo umjesto u App text=Temperature,jer sad vrijedi za sve stavili text=title i taj title smo stavili u
#konstruktor klase,da možemo izvana dati naslov
        tk.Label(self, text=title).grid(column=0, row=0)# postavljen Label u klasu, text=title- iz konstruktora da ga možemo uzeti izvana 
#Onda smo iz App prebacili tk.Scale, vrijendosti koje ima Scale, smo dali u konstruktor da ih možemo popuniti izvana
        self.scale = tk.Scale(self, # sa self.scale predali smo tk.Scale u konstruktor ove klase, kao i tk.Scale što smo morali dati self
                              from_=from_, #from_ je sa underscore jer je ključna riječ, da se razlikuje od običnog from
                              to=to,  #drugi parametar je onaj koji je postavljen u konstruktor, a prvi je iz Scale, koji koristi scale i
                              resolution=resolution,# vrijednosti iz parametara konstruktora idu u parametre Scale-a
                              tickinterval=abs(to-from_),# sa to minus from_ stavili smo da pokaže samo prvi i zadnji broj, nismo ga stavili u 
#konstruktor, jer su to i from_ postavljeni u konstruktor i oni će kad se napišu automatski odrediti tickinterval, abs()vraća apsolutnu vrijednost
#kad smo napravili if orientation,onda je tickinterval dao negativne brojeve pa smo s abs()postavili brojeve na apsolutnu vrijednost(pozitivni broj)
                              length=length,
                              variable=variable, #to je varijabla za prikaz brojeva, valuesa tempa, vlažnosti i tlaka
                              orient=orientation) # ja nisam stavio gore u App tk.Scale(orient= tk.VERTICAL), jer je taj orient ionako default
        self.scale.grid(column=0, row=1) #gridanje self.scale da se slider može prikazati, ispod labela
