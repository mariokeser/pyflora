import tkinter as tk
from tkinter import ttk # modul za stvaranje tabova
from PIL import Image, ImageTk # za otvaranje slika Image, i ImageTk za stavit sliku iz PIL-a u tkinter kontejner
from tkinter import filedialog # filedialog služi dodavanje slika
import json # modul za spremanje podataka u json-u
#import sqlite3 # za spremanje podataka u bazu podataka-db
from repo import csv, json, db # iz podfoldera repo(koji je u ovom foderu Moj profil) importaj te module, datoteke

root = tk.Tk()
root.title("Moj profil")

photo_filename = "./pyflora/Moj profil/images/profile_placeholder.jpg" #globalna varijabla za pristup konkretnom/oj placeholderu/slici

lblimg_profile_photo = None # globalne varijable za postavljanje novih slika u profile i edit tab, na None su na početku kako bi se mogle mijenjati
lblimg_edit_photo = None # pa će se pomoću funkcije set_images() mijenjati kako loadamo slike
# od var_name do var_repo povezano je sa kreiranjem tabova i njihovih labela i gumbova, što smo radili prvo kreiranje tabova,labela i gumbova
var_name = tk.StringVar(value="Ime i prezime")#StringVar za ime i prezime koji smo dali labelu u prvom tabu, dali smo value="string", to
var_skills = tk.StringVar(value="Vjestine") # je dok mi sami ne postavimo konkretno ima i prezime, isto je za vještine-label u prvom tabu
var_repo = tk.StringVar(value="db")#stringVar za upis baze podataka, value="db",a poslije će se mijenjati prema konkretnoj bazi podataka
#var_repo kaže koji medij smo odabrali za pohranu naše aplikacije
# ovo dvoje je napravljeno kad smo kreirali funkciju update_profile()

conn = db.get_connection("./Moj profil/data/data.db")#u conn smo predali funkciju za dohvaćanje baze podataka get_connection(unutra predali putanju)
#  koja je pozvana iz modula db.py- modul i funkcija su u podfolderu repo- sve smo mi napravili


var_edit_name = tk.StringVar()#varijable koje smo dali u Entry-za upis imena i vještina kad se otvori novi prozor-kad se klik na gumb-uredi profil
var_edit_skills = tk.StringVar()#koji je u drugom tabu,nismo dali value,kad upisujemo u Entry mijenjaju se te dvije varijable


# postavi veliku i malu sliku na sliku na koju pokazuje, napravili smo ovu funkciju jer ovu radnju ponavljamo više puta
# varijabla `photo_filename`
def set_images(): # uređuje postavljanje svih slika,prvi dio funkcije odnosi se na sliku u prvom tabu, a drugi na sliku u drugom tabu-iste su
    global lblimg_profile_photo, lblimg_edit_photo # globalne varijable postavljene vani na None, služe za dohvaćanje slika iz photo_filename
#img,lblimg_profile_photo,img_thumb,img_thumb.thumbnail,lblimg_edit_photo je rađeno kad smo pravili tabove,labele i gumbove, na početku
    img = Image.open(photo_filename).resize((400, 250))#naredba za otvaranje slike,resize mora biti tuple-da svaka slika bude iste veličine
    lblimg_profile_photo = ImageTk.PhotoImage(img)#naredba za stavljanje slike u tkinter kontejner,sliku smo dolje stavili u tk.Label,oba taba
                                                    #frm_profile i frm_profile_edit-lbl_profile_photo i lbl_edit_photo
    lbl_profile_photo.config(image=lblimg_profile_photo)# konfiguriramo profilnu sliku u labelu,postavljamo na novi image=lblimg_profile_photo

    img_thumb = Image.open(photo_filename).resize((400, 250))#naredba u PIl za otvaranje slike veličine kakva je određena. 
    img_thumb.thumbnail((200, 80))#onda ju dodatno smanjimo za pomoću .thumbnail((tuple))u varijabli img_thumb,PIL naredba,za editanu sliku 
    lblimg_edit_photo = ImageTk.PhotoImage(img_thumb)#i onda moramo tu dodatno resizanu sliku u img_thumb otvoriti u tkinteru, kao i iznad
    lbl_edit_photo.config(image=lblimg_edit_photo)#konfiguriramo sliku za editanje u labelu,postavljamo na novi image=lblimg_edit_photo




# funkcija koja je u commandu radiobuttona-koji su stvoreni za save-anje u bazama podataka, drugi tab, i koja je napravljena prije nego
# smo napravili repo podfolder i u njega spremili save-anje csv, json i db podataka, kad smo to napravili, onda smo u ovoj funkciji promjenili
#naziv funkcije iz save_csv() u csv.save()- jer smo ju nazvali save() u csv.py= csv je importirani modul, a save() je funkcija u tom modulu
#i povezali smo ih s točkom. Primjer takve funkcije je ispod ove, isto smo napravili sa json i db funkcijama
"""def save_data():
    if var_repo.get() == "csv": #ako je var_repo-stringvar za upis medija kojeg smo odabrali za pohranu naše aplikacije, .get() za dohvaćanje
        save_csv(               #jednak csv onda popunjavamo save_csv funkciju
            "./Moj profil/data/data.csv",    # u zagradi je putanja(path) i lista(data), pozvali smo se na funkciju save_csv(path, data)
            [                   #  putanja(path) je -"./data/data.csv", a lista ispod je data
                photo_filename,  # slika.   
                var_name.get(),  # ime i prezime, treba .get() na varijablu
                var_skills.get()  # vještine
            ]
        )
    elif var_repo.get() == "json": # ako je jedank json
        save_json(              # onda popunjavamo save_json() funkciju
            "./Moj profil/data/data.json",  # pozvali smo se na funkciju save_json(path, data), path je "./data/data.json"
            {               # data je dictionary ispod
                "photo_filename": photo_filename,  # dictionary je sa key:value
                "name": var_name.get(),
                "skills": var_skills.get()
            }
        )
    elif var_repo.get() == "db":  # ako je postavljen na database- db, spremamo u bazu
        save_db(conn, photo_filename, var_name.get(), var_skills.get())# popunjavamo funkciju save_db- conn, photo_filename,name i skills su
#sadržani u StringVar varijablama na koje ide .get()-radi dohvaćanja upisanih vrijednosti u te varijable-to želimo spremiti u bazu
    else:           # ovo je ako se dogodi greška onda ide pass,nećemo ništa napraviti 
        # dogodila se greska  # neće se dogoditi osim ako je postavljen na neki drugi var_repo-kojeg nemamo
        pass"""

# funkcija koja je u commandu radiobuttona-koji su stvoreni za save-anje u bazama podataka, drugi tab
def save_data():
    if var_repo.get() == "csv": #ako je var_repo-stringvar za upis medija kojeg smo odabrali za pohranu naše aplikacije, .get() za dohvaćanje
        csv.save(               #jednak csv onda popunjavamo save_csv funkciju
            "./pyflora/Moj profil/data/data.csv",    # u zagradi je putanja(path) i lista(data), pozvali smo se na funkciju save_csv(path, data)
            [                   #  putanja(path) je -"./data/data.csv", a lista ispod je data
                photo_filename,  # slika.   
                var_name.get(),  # ime i prezime, treba .get() na varijablu
                var_skills.get()  # vještine
            ]
        )
    elif var_repo.get() == "json": # ako je jedank json
        json.save(              # onda popunjavamo save_json() funkciju
            "./pyflora/Moj profil/data/data.json",  # pozvali smo se na funkciju save_json(path, data), path je "./data/data.json"
            {               # data je dictionary ispod
                "photo_filename": photo_filename,  # dictionary je sa key:value
                "name": var_name.get(),
                "skills": var_skills.get()
            }
        )
    elif var_repo.get() == "db":  # ako je postavljen na database- db, spremamo u bazu
        db.save(conn, photo_filename, var_name.get(), var_skills.get())# popunjavamo funkciju save_db- conn, photo_filename,name i skills su
#sadržani u StringVar varijablama na koje ide .get()-radi dohvaćanja upisanih vrijednosti u te varijable-to želimo spremiti u bazu
    else:           # ovo je ako se dogodi greška onda ide pass,nećemo ništa napraviti 
        # dogodila se greska  # neće se dogoditi osim ako je postavljen na neki drugi var_repo-kojeg nemamo
        pass


# funkcija za buton-dodavanje slike profila, drugi tab
def change_profile_photo():
    global photo_filename #moramo ovu varijablu napraviti kao globalnu,jer s njom učitavamo početnu sliku, s ovom varijablom krećemo s učitavanjem
            #ta varijabla postavljena je vani s putanjom na konkretnu sliku,funkcija je u butonu za dodavanje slike profila

    # ucitaj putanju do nove slike profila
    photo_filename = filedialog.askopenfilename(title="Odaberi sliku")# modul iz tkintera služi za odabir nove slike, otvori se documents
                                            # u računalu gdje onda biramo novu sliku. Moramo predati title="odaberi sliku"
 # Nakon otvaranja documentsa bira se nova slika za dodavanje u profil i onda funkcija ispod uređuje slike
    # postavi veliku i malu sliku na tu novu sliku
    set_images() # i onda smo u funkciju change_profile_photo() dodali funkciju koja uređuje postavljanje slika

# funkcija za uređivanje profila na gumbu uredi profil,drugi tab,zato što je funkcija edit_profile_screen u tk.Button-Uredi profil
# u kojoj je tk.Toplevel- kad se klikne na taj gumb Uredi profil-otvori se novi prozor koji smo opet nazvali Uredi profil
def edit_profile_screen(): # ova funkcija je predana kao command u tk.Button- gumb Uredi profil-na klik tog gumba izvrši se ovo dolje
    # stvaranje novog prozora, tl_edit_profile varijabla predstavlja novi prozor koji se otvori kad klik na gumb uredi profil zbog tk.Toplevel
    tl_edit_profile = tk.Toplevel(root)#widget Toplevel služi za otvaranje novog prozora,root je parent,otvori se prozor kad se klik na Uredi profil
    tl_edit_profile.title("Uredi profil") #postavili smo  novom prozoru title koji se otvori kad se klik na gumb Uredi profil-zbog Toplevel iznad
    tl_edit_profile.geometry("300x150") # odredili smo mu veličinu, novom prozoru
    # moze bez ovoga, prebacuje fokus automatski
    # kao da smo misem kliknuli na taj prozor
    tl_edit_profile.focus()

    # azuriraj novo ime, prezime i vjestine, ovdje smo stavili funkciju u funkciju, ovo je funkcija za spremanje promjena kad se otvori
    # novi prozor u gumbu uredi profil i kad upišemo novo ime i vještine,kao nutarnja funkcija služi samo za edit_profile_screen() funkciju
    def update_profile():#vrijednosti koje smo upisali unutra moramo uzeti i postaviti ih van
        var_name.set(var_edit_name.get())#mijenjamo var_name i .set()-postavljamo na ono ime koje piše u var_edit_name i .get da ga dohvati
        var_skills.set(var_edit_skills.get())#var_name i var_skills su u prvom tabu, a ovo drugo je u drugom u gumbu uredi profil

        var_edit_name.set("") #ovo smo napravili kako ne bi u prozoru uredi profil-tl_edit_profile- kad ga ponovno otvorimo ostale
        var_edit_skills.set("")#vrijednosti koje su upisane od zadnjeg puta, sa .set("") postavili smo ih na prazan string 

        # potrebno je spremiti nove podatke
        save_data()# čim upišemo podatke u uredi profil i klik na spremi pozvali smo ovu funkciju da se automatski spreme ti podatci, ova funkcija
        # je postavljena u ovoj funkciji update_profile() i ovdje vrijedi samo za nju

        # zatvori novi prozor nakon spremanja novih podataka
        tl_edit_profile.destroy()# .destroy() služi da kad upišemo podatke u novom prozoru i klik na spremi, prozor se zatvori

    # ovo je za bind kad stisnemo Enter
    # mora biti jedan argument, ali funkcija samo prosljeđuje
    # poziv da update_profile funkcije
    def update_profile_event(event): # varijabla event treba da ne faila funkcija iako se u istoj ne mora koristiti,
        update_profile() #predali smo funkciju za upisivanje i spremanje promjena(sprema preko ubačene funkcije save_data()) i ova se 
    # primjeni kad klik na enter tipkovnice,ako klik na-spremi-onda se primjeni ona iznad- def update_profile()

    # ako stisnemo Enter, to je kao da smo stisnuli gumb Spremi
    tl_edit_profile.bind("<Return>", update_profile_event) #<Return> predstavlja enter na tipkovnici i na taj prozor smo bindali keylistener
    #<Return> i dodali funkciju update_profile_event- moramo dodati funkciju i to onu koja ima upisan event, zato smo gore napravili
    #def update_profile_event(event) i njoj predali funkciju update_profile koja se odnosi na ovaj novi prozor za upisivanje i spremanje promjena

    # Label i Entry za unos novog imena-kad se klik na gumb uredi profil-koji otvara novi prozor,jer smo u funkciju tog gumba dali tk.Toplevel
    # tl_edit_profile predstavlja taj novi prozor za upisivanje promjena 
    tk.Label(tl_edit_profile, text="Unesite ime i prezime").pack()#novom prozoru damo label sa textom i packamo ga da se pokaže
    ent_update_name = tk.Entry(tl_edit_profile, textvariable=var_edit_name)#Entry za upis texta na parentu tl_edit_profile i damo mu StringVar 
# varijablu za upis imena,stvorena gore, kad se predaje varijabla mora ići textvariable=
    ent_update_name.pack() # pack da se pokaže
    ent_update_name.focus() #kad se otvori prozor za upisivanje promjena,- .focus() odmah stavi kursor na entry varijablu za upis imena i prezimena
    # odmah možemo krenuti pisati

    # Label i Entry za unos novih vjestina, za vještine isto vrijedi kao za ime gore
    tk.Label(tl_edit_profile, text="Unesite vjestine").pack() #label s imenom
    ent_update_skills = tk.Entry(tl_edit_profile, textvariable=var_edit_skills) # entry za upis vještine
    ent_update_skills.pack()

    # Gumb za spremanje novih promjena, treba nam da možemo spremiti promjene kad se otvori novi prozor i upišemo promjene i klik na spremi
    tk.Button(tl_edit_profile, text="Spremi", command=update_profile).pack()#root je isto novi prozor i damo funkciju za spremanje promjena
    # i opet pack() inače sse gumb neće pokazati

    tl_edit_profile.mainloop() # moramo pokrenuti mainloop, jer svaki prozor moramo mainloopati da se otvori- tl_edit_profile je novi prozor
# Ovo iznad je sve u funkciji def edit_profile_screen()

# Tabovi s vrha aplikacije -Prvo što smo napravili poslije root.title sve do funkcije set_images()
tabs = ttk.Notebook(root) #za stvaranje tabova ide modul ttk.Notebook i njemu predamo root kao parent
tabs.grid(column=0, row=0) #postavljanje na grid, početni jer je novi okvir

# Frame koji sadrzava prvi ekran, tu se još ništa ne vidi na placeholderu
frm_profile = tk.Frame(tabs) # frame,prvi ekran - predamo tabs kao parent, tk.Frame za stvaranje frame-a, prvi tab-profil
frm_profile.grid(column=0, row=0) #postavljen na nulti stupac, red kao početna vrijednost jer je novi okvir

# Frame koji sadrzava drugi ekran,
frm_profile_edit = tk.Frame(tabs) #frame, drugi ekran -predamo tabs kao parent, drugi tab-uređivanje profila
frm_profile_edit.grid(column=0, row=0)

# Dodaj 2 taba i povezi ih sa Frame-ovima, tek ovdje se vide tabsi profil i uređivanje profila na placeholderu
tabs.add(frm_profile, text="Profil") # dodajemo tabsu na Frame, pomoću .add(preda se varijabla sa Frameom, ekranom i text za naziv)
tabs.add(frm_profile_edit, text="Uredi profil")# u .add(), moraju biti ta 2 argumenta, tim redom


# TAB Profil, stavljamo stvari sa tab profila, to su slika, ime i prezime, naslov Vještine, popis vještina
#radimo sa tk.label koji dodaje widgete sa slikom i tekstom, ali se ništa s tim ne radi, samo se vidi što znači ili pokazuje

# slika
lbl_profile_photo = tk.Label(frm_profile) # parent je prvi tab
#image=lblimg_profile_photo#slika je bila predana ovdje,ali je izbačena kad smo napravili set_images() i lblimg_profile_photo = None,jer je na 
# početku None, sliku postavljamo sa configom u set_images() -funkcija je postavljena dolje na kraju 
lbl_profile_photo.grid(column=0, row=0)# u label widgetu ekranu slika je na nultom stupcu i retku, profilni foto

# ime i prezime
tk.Label(frm_profile, # na isti frame stavimo ime i prezime, kao parent
         textvariable=var_name,#varijabla sa imenom,kod predaje varijable mora ići textvariable=,varijabla jer će se taj text, ime mijenjati
         font=("Arial", 18)).grid(column=0, row=1) #tip fonta i veličina, i drugi redak, ispod slike, na sredini

# naslov Vjestine
tk.Label(frm_profile, #isti frame
         text="Vjestine", # ovdje nema varijabl,Vještine su naziv tog odjeljka,neće se mijenjati pa smo predali text, mora ići text="string"
         font=("Arial", 16)).grid(column=0, row=2, sticky="w")#sticky je parametar za poravnavanje labela,"w"=west,zaljepi ga "w" u istom stupcu

# popis vjestina
tk.Label(frm_profile, # isti frame
         textvariable=var_skills, # varijabla jer je mijenjaju vještine
         font=("Arial", 12)).grid(column=0, row=3, sticky="w")

# TAB uredi profil,stvari s tog taba,frame za gumbe, gumbi(radiobutoni) za pohranu u bazu, CSV i JSON datoteku, gumbi(tk.Buton) za 
#dodavanje slike profila,uređivanje profila i slika(label).Sa tk.Radiobutton i tk.Button prave se gumbi koji imaju neku funkciju(izvršavanje) 

# Frame za gumbe
frm_repo = tk.LabelFrame(frm_profile_edit, text="Odabir pohrane")#naziv frame-a repo jer biramo neki repozitorij podataka,drugi tab smo predali u
# tk.LabelFrame jer pravimo frame za gumbe i dali mu text, frm_profile_edit je parent
frm_repo.grid(column=0, row=0, columnspan=2) #sa columnspan=2 rekli smo da se ovaj tab proširi na dvije kolone, jer ćemo ovdje imati 2 kolone
# unutar cijelog frame-a, redak i stupac je 0 jer je početni okvir u ovom tabu

# gumb za pohranu u bazu
tk.Radiobutton(frm_repo,  # predamo frame za gumbe, parent
               text="Baza podataka", # text je za bazu podataka
               variable=var_repo, #varijabla StringVar za bazu podataka,definirana gore,tu je variable=jer se neće mijenjati text,već baza podataka
               value="db", # defaultni value za baze podataka, kod radiobuttona mora imati value="string"
               command=save_data).grid(column=0, row=0) #command na koji ide funkcija za izvršenje butona i grid za poziciju-prvi gumb u frm_repo

# gumb za pohranu u CSV datoteku
tk.Radiobutton(frm_repo, # isto kao baza podataka
               text="CSV datoteka",
               variable=var_repo,
               value="csv",
               command=save_data).grid(column=1, row=0) # druga kolona

# gumb za pohranu u JSON datoteku
tk.Radiobutton(frm_repo, # isto kao baza podataka
               text="JSON datoteka",
               variable=var_repo,
               value="json",
               command=save_data).grid(column=2, row=0)# treća kolona

# gumb za dodavanje slike profila
tk.Button(frm_profile_edit, #ovdje parent nije frm_repo kao za radiobuttone, već drugi tab(širi parent),i za dodavanje slika ide tk.Button
          text="Dodaj sliku profila",
          command=change_profile_photo).grid(column=0, row=1) #u commandu funkcija za dodavanje slike profila i red je ispod frm_repo okvira

# slika
lbl_edit_photo = tk.Label(frm_profile_edit) # parent je drugi tab
#image=lblimg_edit_photo)#slika je bila predana ovdje,ali je izbačena kad smo napravili set_images() i lblimg_edit_photo = None,jer je na početku
# None, sliku postavljamo sa configom u set_images()
lbl_edit_photo.grid(column=1, row=1) #grid je pored gumba za dodavanje slike profila

# gumb za uredjivanje profila
tk.Button(frm_profile_edit,  # gumb za uređivanje profila, parent isto drugi tab
          text="Uredi profil",
          command=edit_profile_screen).grid(column=0, row=2)#predana funkcija za uređivanje, grid je ispod gumba dodavanje slike profila


# postavi veliku i malu sliku
set_images() #na kraju smo postavili ovu funkciju koja postavlja slike u labelu u oba taba, nakon što smo loadali sve ove labele i napravili
# sve buttone onda funkcija postavlja slike počevši od početne slike određene u photo_filename
save_data()

root.mainloop()
# ovo je ubacio pa delete, kad se piše ime i prezime i skills,kad se otvori novi prozor klikom na gumb uredi profil, u drugom tabu
#to što se piše, preko ovih labela prikazuje se u drugom tabu ispod slike- zanimljivo
"""tk.Label(frm_profile_edit,
         textvariable=var_edit_name).grid(column=1, row=2)
tk.Label(frm_profile_edit,
         textvariable=var_edit_skills).grid(column=1, row=3)"""

