import repo_1 # import repo zbog importa napravljene baze i njezinih funkcija u repo.py
import time # zbog primjene sleep() metode iz tog modula, koja daje da se funkcije ponavljaju u vremenu koje je zadano u sleep()

# aplikacija za provjeru da li rade funkcije za dohvaćanje zadnjih vrijednosti iz baze, (za seminarski rad)
db_client = repo_1.DbClient("./pyflora/Sensors/data/readings_1.db") #napravili smo clienta kojem smo iz modula repo klasu DbClient koja ima bazu podataka koji nam trebaju
# i njoj smo predali putanju do stvorene baze i njeno ime

while True: # sa ovim smo otvorili petlju koja se stalno vrti(znam to otprije), sa print dajemo da se prikazuje u terminalu
    print(f"Temperature: {db_client.get_temperature()}°C") # u formatu dajemo prvo ime vrijednosti koju očitavamo i clientu predamo
    print(f"Pressure: {db_client.get_ph_value()} pH") #metode za dohvaćanje vrijednosti koje su iz clase DbClient koja je predana db_clientu
    print(f"Humidity: {db_client.get_humidity()}%")#ta varijabla je u bracketsu da ju dohvati i za kraj u stringu mjerna jedinica

    time.sleep(0.9) # time.sleep smo dali na 0.9 sekundi da radi malo brže nego što se upisuje u bazu,brzinu upisa u bazu smo odredili u
    #gui.py u klasi App preko njenih metoda, da nema sleep(), ispisivale bi se vrijednosti svake sekunde da se vrijednosti upisuju u bazu 
    # kako smo odredili u gui.py
    #Onda smo napravili da sam u simulator.py otvorio slider, nakon toga sam otvorio novi terminal i u njega upisao
    #python3 ./client.py i enter. tako samo mogao gledati u terminalu ispise vrijednosti, dok imamotvoren slider i na njemu pomicati slider,
    #mijenjati vrijednosti i tako su se onda mijenjale i vrijednosti koje su se ispisivale u terminalu od client.py
    # sad imamo komunikaciju između dvije aplikacije-simulator koja upisuje stvari u bazu(tek kad se pokrene simulator stvari se upisuju u bazu)
    #i ona javlja drugoj aplikaciji-client.py- te vrijednosti i ta druga aplikacija sad može ispisivati na ekran(uterminalu) te vrijednosti.
    # tako možemo raditi i sa stvarima za seminarski rad u vezi biljaka i očitanja vrijednosti koje moramo pratiti kod njih, dodavati
    #druge slidere

