import requests # modul za pozivanje(slanje zahtjeva) podataka sa stranice, unutar njega je metoda get() koja dohvaća ono što tražimo sa requests
# kad se spajamo na Api na neki server onda smo mi klijent, zato smo ovaj modul nazvali client

# ovo je klasa napravljena za spremanje filmova kad smo dolje napravili praznu listu movies= [] i u nju apendali ovu klasu sa svim 
#parametrima koje želimo spremiti, to je klasa koja samo čuva podatke-zove se i dataclass
class Movie:
    def __init__(self, title, year, imdbId, type, poster):#u konstruktor smo poslali sve parametre koje dobijemo iz filmova koje dobijemo iz API  
        #poziva, koji su u API json formatu
        self.title = title # ovdje smo to spremili u klasu
        self.year = year
        self.imdbId = imdbId
        self.type = type
        self.poster = poster

#napravili smo klasu za klijenta za dohvaćanje posataka sa servera
class OmdbClient:  #self uvijek mora ići i to prvi-postavlja konstruktor koji stvaramo u klasu, sve što stvaramo postavlja u klasu u kojoj radimo
    def __init__(self, url, api_key):# u konstruktoru smo predali url-put do servera i api key, 
        self.url = url # spremili smo url i api key, zahvaljući ovom spremanju ne moramo metodi ispod koja dohvaća filmove davati url i api_key
        self.api_key = api_key
#nakon što smo dohvatili put do servera, sad pravimo metodu za dohvaćanje servera
#metoda za dohvaćanje filmova,definirana nad klasom OmdbClient,self uvijek mora ići u metodu nad klasom i mora ići prvi-postavlja klasu u sebe
    def get_movies(self, query, page=1):#predali smo query to je Search dio(što tražimo,npr Marvel) i page=1,defaultna vrijednost,ako ne 
#predamo argument page,sam će dohvatiti page 1,self znači da je metoda nad klasom OmdbClient,svaka metoda u klasi mora imati self kao i konstruktor klase
#s response= u get_movies pozivamo nešto s te stranice,s requests.get()pozivamo,u get smo postavili self.url(put do stranice) koji smo dali u klasi 
#OmdbClient i sa params= dajemo query parametre, .get() ima argument params= u njemu se stvari daju kao i dictionary {key:value}, tu smo 
#postavili api_key mora ići sa self.jer je predan kao parametar u ovu klasu, "s"- je iz OMDb stranice parametar za Search njemu smo dali value 
#query(koji je upit), "page":page-parametar za stranicu, po defaultu smo ju u ovu klasu stvavili na 1, i "r" parametar za vrstu datoteke u OMDb API 
#stranici:dali smo value da tip responsa bude json, sa response tražimo dohvaćanje onoga što nam treba
        response = requests.get(self.url, params={"apikey": self.api_key,
                                                 "s": query, # stavili smo query da možemo upisati koji god query/upit
                                                 "page": page,  # stavili smo samo page tako da možemo dohvaćati koju god stranicu, default je 1
                                                 "r": "json"})


       


        if response.status_code != 200:#na response dodajemo .status_code-ako bi bio response code razliciti od 200 da smo dobili error,
            print(f"ERROR: status code {response.status_code}")#ako je različiti od 200,dali smo print u formatu-response.status_code-da vidimo koji je
            return [], 0, 0 #ovdje želimo returnat listu filmova koje smo dohvatili/trazili-[],ukupan broj filmova koje ima taj server-0,i ukupan 
        #broj stranica filmova na serveru-0, ako je error onda hoćemo da nam vrati praznu listu filmova i 0 filmova i 0 stranica
#[],0,0 odnosi se na navedeno jer json iz API tako daje podatke-lista filmova,ukupan broj filmova i budući ima 10 filmova po stranici pod 
#drugom nulom može dati i ukupan broj stranica i na kraju "Response":"True"-ako je sve u redu- u obliku dictionary. Ovaj error možemo provjeriti
#ako stavimo pogrešan naziv "apikey" u response
        
#nakon toga uzimamo json value odnosno popis svega što smo tražili u json formatu da dobijemo traženo iz response=..., json ima oblik dictionarya       
        movies_json = response.json()# na varijablu movies_json dali smo taj response i .json() i dobiti ćemo python dictionary, sa popisom
        #filmova, "total results"="neki broj" i "Response"="True"
        
#Sad pitamo "Response" koji dobijemo na kraju json datoteke kao "True"(ako je sve u redu) iz movies_json= response.json()    
        if movies_json["Response"] == "False": #ako je "Response" na movies_json == "False"
            print(f"ERROR: {movies_json['Error']}")#print grešku,u formatu je movies_json-da dobijemo koji je njegov error, ispis
            #{movies_json['Error']}-znači poruka iz movies_json na Error dijelu-['Error']-to je na error dio.String je ' jer već imamo " u formatu
            return [], 0, 0 #i ako smo dobili eror ispisati će se ovo gore i opet vracamo praznu listu, 0 filmova i 0 stranica
        # ovaj eror se može priovjeriti ako na page value u response damo npr +777(prevelik broj stranica)
        
 # sad uzimamo sve filmove is responsa       
        movies = [] # prazna lista koju dohvaćamo u for petlji
        for movie in movies_json["Search"]: # movies_json stavili smo na ["Search"] je je taj "Search" na početku liste svih filmova u responsu 
            #API jsona
            movies.append(Movie(movie["Title"],# u listu movies appendamo gore napravljenu klasu Movie sa svim argumentima koje smo predali toj klasi
                                movie["Year"], # movie koji se iterira ide na te argumente koji su napisani u stringu u json formatu iz API poziva
                                movie["imdbID"], # pa ide movie["argument"]- znači movie na to što smo predali
                                movie["Type"], # ovi stringoci idu umjesto varijabli koje smo predali argumentima u klasi Movie
                                movie["Poster"]))
        
        
       
        total_results = int(movies_json["totalResults"])# računamo koliko smo dobili ukupno filmova, int-da bude integer, od movies_json na 
        #["totalResults"]- "totalResults" je string koji se dobije iz API poziva na omdbapi.com stranici  u json formatu na kraju dictionarya

# ispod je za dobiti ukupan broj stranica,ovo smo dobili, jer od 1 do 10 filmova je jedna stranica, od 11 do 20 je druga itd i to dobijemo
#sa cjelobrojnim dijeljenjem, jer kad od  oduzmemo 1 onda dobijemo od 0 do 9 filmova i to možemo cjelobrojno podijeliti sa 10 i 
#da nam 0 i zato dodamo 1 na kraju, za jedan više i dobijemo prvu stranicu,onda od 10 do 19 filmova(kad sam oduzeo 1) dobijem jedan kad 
#cjelobrojno dijelim sa 10 i dodam jedan više za drugu stranicu, onda od 20 do 29(kad sam oduzeo 1) kad podijelim cjelobrojno sa 10 dobijem 2 
#i dodam 1 na kraju i tako na kraju dobijem točan broj stranica
#cjelobrojno dijelimo sa 10 jer znamo da ima deset filmova po stranici i kad oduzmemo ukupan broj od 1, cjelobrojno podijelimo sa 10 i dodamo
#1 više broj-dobijemo ukupan broj stranica
        total_pages = (total_results-1) // 10 + 1 #ovo smo tražili da znamo koliko trebamo listati u gui-u,ako listamo previše/izvan dobijemo error
        
        return movies, total_results, total_pages # na kraju vracamo dobivene filmove, total_results i total_pages i tek tu smo izbacili ovaj
    #return movies_json, koji je postavljen u kodu kad mu je predan movies_json = response.json()
    #return movies_json #kad smo response dali u movies_json onda smo umjesto return response dali ovaj return, jer smo u dali taj response
    #odmah nakon što smo napravili metodu get_movies i njoj dali response, return sluzi da se može koristiti izvan funkcije
    # i kad pokrenemo program onda u terminalu izbaci što smo tražili
        
    

# s ovim ispod  provjerili smo da li nam sve do sada radi kako treba, nakon definiranja get_movies,a prije rada sa if-ovima za error i ostalim 
#što slijedi ispod if-ova    
#return response #da nam vrati response izvan metode get_movies da se može koristiti vani,gore smo taj response dali u movies_json = response.json()
#api_key = open("./api_key.txt").read()# tu smo spremili api_key , znači da ga otvori i .read() pročita
#url = "https://www.omdbapi.com" # put do stranice
#client = OmdbClient(url, api_key) # varijabli client dali smo klasu i njoj predali definirani url i api_key koji i jesu njeini parametri
#print(client.get_movies("marvel")) #dali smo da se printa klasa koja je u client i njoj smo dodali metodu napravljenu nad tom klasom OmdbClient,
#ona služi za dobivanje response kako smo i napravili varijablu response u njoj-morali smo joj predati njezin parametar query(upit)-nazvali smo ga
#marvel, a page nismo jer smo dali da je default page=1,ako se ne zada page. Dobio sam response code [200]-radi!! Imamo kontakt sa serverom. 
#Dobili smo samo taj response, nismo iz njega uzeli pravi text, to će biti kad response iz get_movies damo .json() u movies_json

# Nakon što smo napravili movies_json = response.json() i  return movies_json, prije nastavka coda isprobali smo kako to radi
#api_key = open("./api_key.txt").read()
#url = "https://www.omdbapi.com"
#client = OmdbClient(url, api_key)
#movies = client.get_movies("marvel") # movies dali smo client(klasa OmdbClient) i metodu napravljenu nad tom klasom OmdbClient
#print(movies) # dobili smo listu filmova, total results i response:true-kao  python dictionary jer tu već imamo da smo u movies_json dali 
#response.json() kako bi dobili python dictionary iz json datoteke i napravili return movies_json. Metoda napravljena nad klasom mora biti
#pozvana da bi radila, zato je client.get_movies("marvel")
"""
# ovo smo napravili kad smo došli do kraja koda do return movies, total_results, toral_pages
api_key = open("./api_key.txt").read()
url = "https://www.omdbapi.com"
client = OmdbClient(url, api_key)
#movies, results, pages = client.get_movies("marvel")# napravili smo višestruku varijablu i njoj dali klasu i njezinu metodu za dohvaćanje filmova
# ove varijable kad im je predano client.get_movies("marvel") postale su varijable iz return movies, total_results, toral_pages
movies, results, pages = client.get_movies("marvel", 30) #ovdje smo predali page 30 u metodu,inače smo gore kad smo ju stvarali 
#dali da je page=1 defaultna stranica
for movie in movies: #movies je lista filmova
    print (movie.title) # svaki movie koji se iterira u movies, dan mu je title koji je u listu movies apendan preko klase Movies
print(results) #rezultati iz total_results
print(pages) #pages iz total_pages
# Kad smo u main.py napravili main()sa api_key i sa url-om direktno preko client=(pogledaj u main) onda je ovo zakomentirano izbrisao
"""

