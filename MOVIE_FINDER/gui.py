import tkinter as tk # za pravljenje GUI aplikacije
#klasa služi za spremanje i čuvanje podataka,dok funkcija služi ako neku radnju želimo ponavljati više puta, pa samo opet pozovemo funkciju


# parametri koji se daju u konstrukt služe sa dohvaćanje stvari izvana-kao što je movie_client, a ono što vrijedi samo unutra, samo unutar klase
# kao što je ispod self.title ne ide  u init, self znači da u ono što se stvara prvo se postavlja ta klasa u kojoj se radi
# napravljena je klasa za gui aplikaciju i predan tk.Tk kao root
class App(tk.Tk):
    def __init__(self, movie_client): #u konstruktor pored obveznog self,kao parametar predali smo movie_client jer želimo dobiti klijenta, 
        #za dohvaćanje klijenta izvana,klasa će morati raditi fetchpozive kad stisnemo gumb da se pozove get_movies, ovaj movie_client je
        #iz main.py u def main() kojem smo predali client.OmdbClient("https://www.omdbapi.com", api_key)-put do API stranice i u OmdbClient klasi
        #je metoda get_movies koju moramo pozvati za dohvaćanje filmova, kako smo napravili ispod u probnom printu, predali smo gui aplikaciji
        #klijenta za dohvaćanje filmova u main.py modulu
        super().__init__() # ovaj super mora biti zbog nasljeđivanja tk.Tk

        self.movie_client = movie_client#postavili smo movie_client u nju,u klasu, sad klasa ima toga klijenta unutra u varijabli self.movie_client 

        self.title("Movie Finder") # klasi App dali smo naslov, kako će se zvati kad se otvori

#ovaj print smo probali da vidimo da li smo dobro povezali ovu gui aplikaciju sa main.py
        #print(self.movie_client.get_movies("abc", page=30))#u print smo dali self.movie_client postavljen u ovoj klasi i njemu predali 
        #s .get_movies() metodu za dohvaćanje filmova i u get_movies njezine parametre "abc" koji je query/upit i broj stranice koju tražimo
     #kad u main.py pokrenemo program pored što se otvori gui aplikacija s ovim print u terminalu od main.py pokaže se što smo dali da se printa

        self.ent_search = tk.Entry(self)#napravljen entry za search,za upis što searchamo,jer je u klasi mora ići na self, klasa je parent
        self.ent_search.grid(column=0, row=0) # pozicioniranje entrya

        self.btn_search = tk.Button(  #napravljen je buton za search,isto mora imati self jer je u klasi,text(zove se gumb) search,command=None
            #bilo je na početku, kad smo napravili metodu u klasi za fetchanje filmova, stavili smo ju u command da bi gumb funkcionirao
            self, text="Search", command=self.fetch_movies)#metoda stavljena u command je postavljena na self. jer je u klasi, da se postavi u nju
        self.btn_search.grid(column=1, row=0) #pozicioniran je pored entry za search
# klasu MovieFrame predali smo u App i predali mu self da bude u klasi App
        self.frm_movies = MoviesFrame(self) # uvijek se mora sve postaviti na self jer je u klasi
        self.frm_movies.grid(column=0, row=1, columnspan=2)# pozicionirali smo(gridali) ga u red ispod da se razvuče na 2 columna, 
#ispod pravimo metodu nad klasom App koja će dohvaćati filmove, naravno mora imati self da se postavi u klasu u kojoj je
    def fetch_movies(self):#na početku dohvaćamo query(upit) koje filmove želimo dohvatiti,u ovoj klasi moramo dohvatiti jer je njoj predan client
        query = self.ent_search.get()# na query postavili smo varijablu sa tk.Entry za upis/search filmova koje tražimo i .get() je za dohvaćanje
        #toga Entrya i dobijemo ono što je ispisano unutra u self.ent_search
        if query == "": # ovdje smo rekli ako je query prazan, to označava ovaj prazan string
            return # samo napravimo return, ne želimo pretraživati prazan query
# sada radimo dohvaćanje filmova, na self(da se stavi u ovu klasu)postavili smo movie_client varijablu koja je napravljena u main.py koja označava
#put/url do stranice i ima api_key preko client.OmdbClient("https://www.omdbapi.com", api_key)(napravljeno u client.py) i taj movie_client smo
#postavili u ovu klasu gore tako da preko njega imamo pristup stranici sa filmovima. I na movie_client postavili smo funkciju .get_movies koja
# je napravljena u client.py nad klasom OmdbClient i služi za dohvaćanje filmova i na get_movies predali smo ovaj naš query/upit u koji smo
#postavili entry varijablu za search/upis onoga što tražimo. To smo postavili u ovu trostruku varijablu page_1, _, pages jer funkcija 
#get_movies u client.py returna ovo-return movies, total_results, total_pages- tri stvari pa će na page_1 ići movies, na _ ići će total_results,
#s ovim _ placeholderom rekli smo da nam ne treba total_results, a na pages ići će total_pages(broj stranica), return je napravljen kao tuple, 
#pa onda moraju ići ove 3 varijable, svaka za jedan element u tuple, _ ovo znači da taj element u tuple-u ignorira
        page_1, _, pages = self.movie_client.get_movies(query)# dohvati page 1 jer smo u get_movies stavili u parametar default page=1
        #print(page_1)# ovo smo napravili da nam dohvati samo filmove da vidimo da li radi, nisu bili lijepo prikazani,jer su u obliku klase Movie
        #iz client.py koja samo čuva podatke, vidjeli smo samo da je to objekt te klase, ali nismo vidjeli koji su točno filmovi, tu smo nakon što
        #smo napravili print(page_1) u main.py pokrenuli App za search, upisali nešto u search i onda se to prikazalo u terminalu, onda smo 
        #napravili ovo ispod, isto smo nakon napravljene ove for petlje u main.py pokrenuli App za search i upisali u search abc
        #for movie in page_1: #iz page_1 izvukli smo movie na .title-jer smo u klasu Movie iz client.py između ostalog spremili i title i onda su se
            #print(movie.title)#u terminalu prikazali filmovi lijepo ispisani,samo 10,samo prva stranica,jer smo u get_movies stavili default page=1
#tražili smo broj stranica (pages) tako da možemo pitati ako je broj stranica 0, nismo dobili ni jedan film pa možćemo napraviti return  
        if pages == 0:
            return
#ovdje hendlamo stranice nakon što smo u MoviesFrame napravili populate_movies pomoću for petlje i u self.frm_movies predali populate_movies(page_1)
        movie_pages = [page_1]#movie_pages(prazna lista napravljena u MoviesFrame) je jednako i postavili smo ju na page_1
        for i in range(2, pages + 1):#krećemo od 2 jer prvu stranicu već imamo(page_1),stavili smo pages+1 jer su stranice indeksirane od 1 ne od 0,
            #to je pages(stranice) iz  page_1, _, pages = self.movie_client.get_movies(query)
            page_i, _, _ = self.movie_client.get_movies(query, i)#page_i(page_1 sad je page_i jer sad dohvaćamo filmove sa svih stranica po kojima
            #smo prošli sa i),_,_(tu ne želimo ništa dohvatiti) i to smo stavili na movie.client.get_movies za dohvaćanje filmova i predali smo
            #mu opet isti query ali sad smo mu rekli stranica ti je i(sve stranice po kojima smo prošli u petlji), gore nismo zadali stranicu pa
            #je stranica bila defaultna prva
            movie_pages.append(page_i)# za kraj smo na praznu listu apendali taj page_i- filmove sa svih stranica
            #print(movie_pages) isprobali smo da li radi,nakon ovog printa pokrenuli smo gui u main.py i upisali nešto u search i klik na search

# kad smo u MoviesFrame napravili metodu populate_movies i dohvatili ih u listboxu sa for petljom, sad ih postavljamo ovdje u self.frm_movies
#u koju smo stavili klasu MoviesFrame, tako da u self.frm_movies predamo populate.movies
        #self.frm_movies.populate_movies(page_1)# metodi populate_movies predali smo page_1-varijablu napravljenu gore za filmove u fetch_movies
        # i dobijemo filmove prve stranice, default page=1 iz klase get_movies
#nakon što smo izhendlali stranice u petlji sa movie_pages = [page_1] onda smo u populate_movies predali popunjenu listu sa svim filmovima
        self.frm_movies.populate_movies(movie_pages)

# ovo ispod je klasa napravljena za listu filmova
class MoviesFrame(tk.Frame): # tk.Frame je naslijeđena klasa 
    def __init__(self, container): # u konstruktor predan je parametar container (kao i prije) mora ga imati zbog tk.Frame,u njega idu filmovi
        super().__init__(container)# super() moramo postaviti zbog naslijeđivanja containera iz tk.Frame
# ispod je prazna lista za spremanje popisa svih filmova iz searcha/querya, prvo smo u klasi App napravili movie_pages i sve u nju apendali
#onda smo ju spremili u self.frm_movies.populate_movies i u def populate_movies i nakon toga smo ju ovdje kreirali kao praznu listu
        self.movie_pages = []
# ovdje pravimo listbox gdje ćemo poredati sve filmove, preko varijable self.lb_movies = tk.Listbox
        self.lb_movies = tk.Listbox(self, width=30)# naravno ide na self jer je u klasi, sa width povećali smo širinu listboxa
        self.lb_movies.grid(column=0, row=0, columnspan=3) # gridanje na self.,na početne pozicije u frame i razvučemo listbox na 3 columna, na
        #kojima su previous i next buton, i label/stranica sa popisom filmova
# ovdje na self(sve što se pravi u klasi mora ići na self)pravimo buton za previous page, zato smo mu dali za text ovaj znak u stringu "<"
        self.btn_prev_page = tk.Button(  # command=None na početku, u tk.Buton mora se predati text ili textvariable-da piše što je i u command
            self, text="<", command=self.previous_page)#mora ići funkcija za funkcioniranje istog, u klasi naravno da mora ići na self
        self.btn_prev_page.grid(column=0, row=1) 

        self.var_page = tk.IntVar(value=0)#tk.IntVar varijabla koja pokazuje broj stranice u labelu ispod kome je predana,dan je početni value=0,
        #ako ne fetchamo ništa od filmova u self.lbl_page label/stranicu sa filmovima vrijednost ce biti 0
        self.lbl_page = tk.Label(self, textvariable=self.var_page)#label je stranica sa filmovima,textvariable=jer se predaje varijabla, a ne text,
        #text ili textvariable mora se predati u label, predana je tk.IntVar varijabla sa početnim value=0 koja pokazuje broj stranice sa filmovima
        self.lbl_page.grid(column=1, row=1)# stranica gridana između previous i next butona
#buton za next page, sve isto kao za previous page samo se odnosi na next page
        self.btn_next_page = tk.Button(self, text=">", command=self.next_page)
        self.btn_next_page.grid(column=2, row=1)#u istom redu kao buton previous page,ali ostavljen je 1 column prazan,između ide stranica za filmove

#pravimo metodu na MoviesFrame kojom ćemo popuniti filmove
    #def populate_movies(self,movies): #predali smo movies za popunjavanje filmova u listbox
        #self.lb_movies.delete(0, tk.END)# prvo smo izbrisali sve iz listboxa da nam se filmovi ne "nadoštiklavaju" ako 2 put pozovemo query
#sad ubacujemo unutra filmove, tako da prolazimo po svim filmovima
        #for i in range(len(movies)): # prolazimo kroz dužinu svih filmova preko len(movies) na indeks i
            #self.lb_movies.insert(i, movies[i].title)#insert movies u listbox s insert na indeks i, dohvati mi movies na i .title-želimo samo naslove
        # sad smo dobili sve filmove i to je stavio gore u self.frm_movies.populate_movies(page_1) u klasi App
     
    def populate_movies(self, movie_pages):#nakon što smo u class App popunili listu movies_pages i predali ju u 
        #self.frm_movies.populate_movies(movie_pages) onda smo ovdje parametar movies preimenovali u movie_pages
        self.movie_pages = movie_pages # i sad smo listu s popisom svih stranica filmova spremili preko ove metode u klasu MoviesFrame.
        #Nakon što je ovako napravio metodu populate_movies sa parametrom movie_pages-onda je sve iz prve(iznad) metode populate_movies prebacio
        #u metodu populate_page i to je s vremenom drugačije konstruirao
#nakon što smo postavili movie_pages u ovu klasu i ispod napravili metodu za hendlanje stranica populate_page,onda smo postavili pomoću
#self. metodu populate_page  u ovu klasu i predali joj 1- dakle postavi mi prvu stranicu, fetchati ću ti sve filmove i postavi mi prvu stranicu
        self.populate_page(1) 

#ispod u komentaru je prikazano kako je prvo radio u ovoj metodi za hendlanje stranica dohvaćenih filmova i zašto, prvo pogledati to    
    def populate_page(self, page):
        if page < 1 or page > len(self.movie_pages):#ako je page manji od 1 ili veći od duljine stranica movie_pages ovdje predane iz populate_movies
            return # samo napravimo return i neće se dogoditi error
#ispod smo napravili smo ako smo (if) na stranici 1 onda smo pomoću .config disable buton za previous page
        if page == 1:
            self.btn_prev_page.config(state="disabled")
        else:  # inače ga stavimo na normal- to je za enable
            self.btn_prev_page.config(state="normal")
#isto smo napravili za next page buton,ako je stranica = broju stranica svih filmova(len daje broj svih stranica koji je ujedno i zadnja stranica)
        if page == len(self.movie_pages):
            self.btn_next_page.config(state="disabled") # pomoću .config  smo next_page buton disable(state=disabled)
        else: # inače(ako nije tako) onda smo ga opet enable pomoći config.(state=normal)
            self.btn_next_page.config(state="normal")

        self.var_page.set(page)

        self.lb_movies.delete(0, tk.END)

        movies = self.movie_pages[page-1]

        for i, movie in enumerate(movies):
            self.lb_movies.insert(i, movie.title)
# metoda za listanje prethodne stranice nad klasom MovieFrame
    def previous_page(self): # moramo uvijek dati self da se postavi u ovu klasu
        page = self.var_page.get()#prvo smo dobili broj stranice iz var_page varijable koju smo prvo postavili u def populate_page,.get()za dohvaćanje
#u toj var_page varijabli znamo na kojoj smo stranici i onda postavimo sa self. metodu populate_page i njoj predamo page koji smo dobili u retku
#iznad ali -1 : daj mi samo populate prethodnu stranicu
        self.populate_page(page - 1)
#isto vrijedi i za metodu next_page
    def next_page(self):
        page = self.var_page.get()# prvo s .get() dohvatimo trenutnu stranicu(page) iz var_page i ispod samo postavimo populate_page i njoj predamo 
#dobiveni page u retku iznad i samo damo +1 : daj mi iduću stranicu
        self.populate_page(page + 1)


"""
# prvo je metodu populate_pages napravio ovako, metoda za hendlanje stranica dohvaćenih filmova, ovim redom je radio u njoj
    def populate_page(self, page): # dali smo parametar page jer hendlamo stranice
        movies = self.movie_pages[page-1]#ovdje od liste movie_pages sa filmovima želimo uzeti page sa filmovima,odnosno page minus 1 zato što naše 
        #indeksiranje liste ide od 0, a stranica od filmova idu od 1,[indeksiranje]-filmovi koje treba prikazati su ovi self.movie_pages[page-1]
        # i njih smo ubacili u varijablu movies
        self.lb_movies.delete(0, tk.END) # ovo ostaje za delete prethodnog querya
# ovdje sad iteriramo  iz range len moviesa(svih filmova) indeks -i- , iteriramo po indeksu i i insertamo movies na indeks i(koji je njegov broj)
        for i in range(len(movies)): #znači prođi po svim filmovima i stavi ih u listbox. movies[i].title je naslov filma, i je njegov broj
            self.lb_movies.insert(i, movies[i].title)#insertamo u listbox na indeks [i] movies(filmove) na [i], i .title-želimo samo naslove
#kad želim iterirati po nečemu ali me zanima i indeks, kao što je ovdje gore gdje nas zanima i indeks, da možemo reći insert na indeks -i- ovaj
#tu naslov(zanima nas redni broj filma), ovo gore jedan način, drugi način je onda on napravio umjesto ovog prvog
        for i, movie in enumerate(movies): #umjesto range(len) ide enumerate(movies)to je da idem po filmovima, ali van dobijem ne film nego tuple
#gdje je prvi element indeks [i]-broj,a drugi element je film movie,bitan je redoslijed prvo ide indeks pa film,zato smo upisali for i, movie in 
#enumerate(movies)-enumerate is useful for obtaining an indexed list pa pokaže (0,seq[0]), (1,seq[1]), (2,seq[3]) itd
            self.lb_movies.insert(i, movie.title)# i onda dolje ide prvo i(indeks) pa movie-kako smo ih u for loop napisali i damo .title na movie
#indeks [i] predstavlja broj na koji se postavlja naslov filma zato da imamo samo ovako ispod
        for movie in movies:
            self.lb_movies.insert(i, movie.title)# tu imamo naslov filma ali nemamo indeks[i] i onda ne znamo gdje insertati taj film, ovo nije 
#samo izlistavanje filmova iz liste movies već i insertanje istih u listbox i tu nam treba indeks[i] da znamo gdje ih insertati.
#enumerate koristimo ako želimo znati i indekse i konkretne vrijednosti.
#nakon toga je išao postaviti stranicu da nam pokazuje broj stranice u labelu,nju smo kreirali gore u ovoj klasi MoviesFrame i postavili na value=0
#postavio ju je odmah ispod ovoga - movies = self.movie_pages[page-1]
        self.var_page.set(page) #tk.IntVar varijabli sa .set() postavili smo vrijednost na page-koji je parametar ove metode 
# za hendlanje stranica populate_page(self, page), ne želimo da više pokazuje 0 već stranicu koja je. Nakon ovoga smo išli raditi metode
#next_page i previous_page. Nakon toga je radilo klikanje na previous i next page, ali kad se dođe iza zadnje stranice javljalo je 
#error list index out of range. Onda je u populate_page iznad ove gore naredbe složio kako je prikazano u def populate_page iznad i riješio 
#error list index out of range na početku metode populate_page kako je i prikazano iznad
"""