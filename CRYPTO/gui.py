import tkinter as tk # tkinter za napraviti gui za kriptovalute
import fetcher #importirana funkcija za dohvaćanje svega što smo napravili tamo, gdje nam što zatreba
# umjesto stvaranja roota kako smo do sada radili root = tk.Tk() napravili smo root sa ovom klasom ispod -koja se zove tkinter klasa
# toj tkinter klasi inače se daje naziv App-to je neka root level aplikacija
#ova App klasa je sada root za GUI jer nasljeđuje taj tk.Tk() i zato što nasljeđuje tk.Tk moramo joj dati super().__init__()
class App(tk.Tk): # ovo je root klasa, tk.Tk smo naslijedili iz tkinter modula i sad je ova klasa postala taj root, postala je aplikacija(App)
    def __init__(self): #def __init__(self) moramo staviti jer je to klasa, self znači postavi ovaj konstrukt u klasu u kojoj se nalazi
        super().__init__()# dali smo joj super()__init_-() jer nasljeđuje tk.TK, super() je za nasljeđivanje kako smo već učili, sad naša klasa
        #postaje primjerak te klase koju smo naslijedili, i sad radimo sve s tim rootom kao i inače i sad umjesto root.title imamo self.title itd

        self.title("Crypto Market") #dali smo naziv sad sa self. umjesto root., u klasi što god stvaramo mora prvo biti self. pa varijabla
        self.geometry("500x500") #isto tako umjesto root.geometry samo self. jer je ova klasa sad root
#sve postavljamo na self i labele i gumbe jer smo root dali klasi koja radi sa self., umjesto u varijable stavljamo atribute u self
        self.lbl_title = tk.Label(
            self, text="Crypto Market", font=("Arial", 26), fg="green")#kao parenta postavljamo self umjesto roota,fg=green-obojan u zeleno text
        self.lbl_title.pack()# sa self. ga i postavljamo, ovdje smo sa pack(), sa grid bi mu morali postaviti i poziciju, ovdje nije trebalo

        self.btn_refresh = tk.Button(self, text="Refresh") # napravili smo gumb za refresh, i njega moramo postaviti u self, tu nismo dali command
#za refresh jer cemo taj command predati u FrameCrypto,tamo se loadaju i refreshaju valute,jer u ovom trenutku CryptoFrame još nije postavljen pa
#bi javio eror, ne bi prepoznao refresh buton
        self.btn_refresh.pack() # gumb smo pekali, kad packamo gumbe onda se oni postavljaju onim redom kojim  pravimo gumbe, dok sa grid nije
    #bitno kojim redom pravimo gumbe jer imamo column=, row=
#kad smi ispod napravili klasu sa Frame, sad ga ovdje stvaramo, predajemo taj Frame koji je napravljen i nalazi se u toj klasi
        self.frm_crypto = CryptoFrame(self)#u varijablu smo postavili klasu CryptoFrame i predali smo self-znači postavi se u mene(App) kao container,
        # znači postavi se u klasu App kao container,self uvijek znači da se to što se predaje postavi u klasu u kojoj se nalazi
        # sa self znači da je klasa App() parent od klase CryptoFrame
        self.frm_crypto.pack() # pekanje varijable sa klasom CryptoFrame da se pokaže
#Ispod configuriramo buton za refresh kriptovaluta s .config i tu predajemo command kojemu šaljemo funkciju za load valuta, nismo stavili zagrade
#funkcije jer u šaljemo, ovdje je funkcija za load valuta postavljena ispod sa self.frm_crypto(varijabla).load_crypto()
        self.btn_refresh.config(command=self.frm_crypto.load_crypto)# samo s ovim kad klik na gumb za refresh onda kako refresha tako i dodaje
#ispod iste valute,slaže ih refreshane jedne ispod drugih,to smo riješili u CryptoFrame sa def clear(self),oni sami na stranici rade update 
#vrijednosti valuta svakih nekoliko minuta
        self.frm_crypto.load_crypto()#ovdje smo sa self. napravili varijablu kojoj smo dali metodu .load_crypto() za lodanje valuta, tu metodu
        #napravili smo u klasi CryptoFrame koja je ovdje predana, kojoj je parent ova klasa App()-naredba učitaj kriptovalute, ovdje idu zagrade
 #funkcije jer ju s .load_crypto() postavljamo/dajemo unutra, kad se šalje onda ide bez zagrade, ŠALJE SE DA SE DAJE IZA ZNAKA = ?? 
        self.after(2000, self.refresh_task)#self označava klasu u kojoj se radi i ovdje smo napravili da se aplikacija sama refresha ako mi
#ne kliknemo na refresh buton, .after() je metoda koja poziva funkciju nakon danog vremena,self.after(2000-ovo je 2 tisuće milisekundi= 2 sekunde
#danog vremena-radi u milisekundama , self.refresh_task-je metoda napravljena nad ovom klasom koja se poziva), u .after() mora se predati vrijeme
# i funkcija/metoda koja se poziva na pokretanje nakon toga vremena koje je predano(moramo ju napraviti nad .self kao i sve), sa dolje definiranom 
#metodom kad se pokrene aplikacija u main.py napravi refresh samo jednom nakon 2 sekunde 
    def refresh_task(self):#metoda koja treba izvršavati zadatak refreshanja kako bi refresh radio  kad se pokrene aplikacija
        self.frm_crypto.load_crypto()#unutra smo pozvali varijablu za load kriptovaluta, koja je napravljena iznad pomoću metode load_crypto
#znači nakon load kriptovaluta iznad sa self.frm_crypto.load_crypto(), onda ispod pozovemo self.after(2000, self.refresh_task) da to isto napravi 
#nakon dvije sekunde samo jednom pomoću def refresh_task(self):,i onda smo ispod opet dali istu callback metodu-self.after(2000, self.refresh_task)
# koja omogućuje da se radnja refreshanja kriptovaluta ponavlja konstanto svake dviije sekunde
        self.after(2000, self.refresh_task)

# u ovoj klasi pravimo Frame za kriptovalute. zato smo u klasu dali tk.Frame, naslijedili konstrukt iz tkinter modula i sad cemo sve iz tk.Frame
#hendlati u ovoj klasi, CryptoFrame je za popis kriptovaluta
class CryptoFrame(tk.Frame): #inače tk.Frame stavljamo u varijablu,self je u svakoj funkciji container od te funkcije gdje se sve stavlja tk.Frame
    def __init__(self, container): #napravimo init sa self i predajemo container,jer frame ima container za organizaciju gdje se što nalazi,jer ga
        #moramo negdje smjestiti-Frame, gore u klasi App gdje je root nema containera
        super().__init__(container)#sa super() radimo naslijeđivanje containera iz tk.Frame,smjestili smo Frame u container koji smo dali u 
  #def__init__(self, container)
# ovdje ispod napravili smo praznu listu u koju ćemo dodavati kriptovalute, uvijek mora ići self u klasi kad se bilo što stvara, sad je prazna,ali
#kad pozovemo fetch_crypto u metodi load_crypto onda će loadati valute unutra,to smo napravili ispod sa self.crypto_entries.append(ent) u for petlji
        self.crypto_entries = []
#ovdje smo napravili clear metodu tako da mi,kad klik na refresh buton,ne dodaje iste refreshane valute jedne ispod druge,vec samo te refreshane
    def clear(self):
        for ent in self.crypto_entries:#za svaki entry(ent) u listi za kriptovalute koji je dodan ispod sa .append
            ent.pack_forget() #kažemo da mi se taj entry(ent) makne sa screena sa .pack_forget() jer smo dolje taj ent packali da se prikaže
            #na ekranu, funkcija pack_forget() miče to što smo packali, unpacka
#nakon micanja ent-a sa pack_forget, ispod smo ispraznili listu self.crypto_entries sa .clear()-ta metoda clearuje sve što je u listi
        self.crypto_entries.clear()
# sad nad Frame dodajemo metodu(kako smo učili o metodama) za load kriptovaluta kad ju pozovemo
    def load_crypto(self): # metodi predajemo self, svakoj metodi u klasi moramo predati self-označava da se nalazu u ovoj klasi kao parentu
        self.clear()# svaki put kad loadam crypto prvo napravim clear tog load_crypto sa self.clear()-znači da se izbriše sve iz klase
        #CryptoFrame koja je ovdje parent koja je za popis kriptovaluta, kako mi se ne bi refreshane valute slagale jedna ispod druge i
# onda ide load valuta sa ovim ispod, znači prvo clear pa onda loadaj kriptovalute
        cryptos = fetcher.fetch_crypto() #u metodi load_crypto pozvali smo iz modula fetcher funkciju fetch_crypto za dohvaćanje valuta/loadanje
#preko petlje dohvaćamo sve iz liste cryptos nakon štu ju napunimo valutama za funkcijom iznad
        for crypto in cryptos:#sa crypto idemo po svim kriptovalutama u listi cryptos
            ent = CryptoEntry(self, crypto)# ovdje stvaramo novi entry sa klasom CryptoEntry, predamo self kao parenta,gdje da se postavi klasa(kad
#stavim miš na self pokaže mi da je parent klasa CryptoFrame, znači postavila se u CryptoFrame) i predamo crypto koji prima valutu i nju prikazuje,
#iz nje uzima ime i cijenu,preko klase Cryptocurrency koju smo dali u funkciju fetch_crypto i koja je dala toj klasi ime i cijenu u .name i .price
            self.crypto_entries.append(ent)#u praznu listu iznad napravljenu apendamo taj entry sa imenima i cijenama valuta- ent
            ent.pack()# i packamo() taj entry-ent- kako bi ga prikazali na ekranu, inače se ne bi vidio
#kad bi dodavali nove stvari u vezi valuta to bi dodavali samo u klasu CryptoEntry i preko ove petlje ovdje to bi se vidjelo, samo bi u nju 
#dodavali nove labele sa novim stvarima

#ovom klasom pravimo labele za ime i cijene dohvaćenih kriptovaluta, pravimo container/entry za jednu valutu, CryptoEntry je za izgled dohvaćenih
#valuta u vezi imena i cijene svake valute, self je u svakoj funkciji container od te funkcije gdje se sve stavlja tk.Frame
class CryptoEntry(tk.Frame): # nasljeđujemo novi frame za labele
    def __init__(self, container, cryptocurrency):#u konstruktor dali smo container iz CryptoFrame-to će biti njegov container,jer je ova klasa 
#predana u klasu CryptoFrame u for loopu i cryptocurrency-to je primjerak klase iz fetch.py,kad stvaramo CryptoEntry odmah znamo što stavljamo 
#unutra, ta klasa dohvaća name i price-Cryptocurrency
        super().__init__(container)# sa super()opet nasljeđujemo container iz tk.Frame koji smo predali ovoj klasi, uvijek mora ići kod
        #naslijeđivanja predane klase u klasu kojoj predajemo neku klasu, kako bi imali container u ovoj klasi
#ovdje dodajemo labele za ime i cijenu, self mora ići u label kao parent
        self.lbl_name = tk.Label(self, text=cryptocurrency.name)#labelu name dali smo ime-text=cryptocurrency.name-to je iz klase Cryptocurrency iz
# fetcher.py-. name, cryptocurrency je parametar koji smo ovdje predali,a .name i .price su iz klase Cryptocurrency kojoj smo appendali crypto_name
# i crypto_price na self.name i self.price
        self.lbl_name.grid(column=0, row=0) # gridali smo label da budu ova dva labela jedno ispod drugog u frame-u ove klase
# isto to napravili smo za price/cijenu
        self.lbl_price = tk.Label(self, text=f"${cryptocurrency.price}")# ovdje smo stavili text/ime na cryptocurrency.price, .price je iz klase 
        #Cryptocurrency i text smo stavili u format/formatirali radi iskazivanja cijene u dolarima 
        self.lbl_price.grid(column=1, row=0)

# ovdje je pojašnjenje kako radi root-anje između ovih klasa 
#root = App() - ovo je root, glavno, prvi parent
#frm = CryptoFrame(root)- frame je CryptoFrame i njemu smo predali root App() kao parenta
#lbl = CryptoEntry(frm) - CryptoEntry je label kojem smo predali frm(CryptoFrame) kao parenta u koji ide text name i price

