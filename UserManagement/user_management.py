import tkinter as tk 
from tkinter import messagebox # služi za pokazivanje error screena(boxa) useru, daje jednostavne screenove za jednostavne message-error message,
# warning message, info message ili možemo s njim postavljati pitanja-otvori se screen koji ima da/ne odgovore-askquestionbox
from repo import db # za import napravljenog db.py modula iz podfoldera repo


conn = db.get_connection("./pyflora/UserManagement/data/Users.db")#napravili smo konekciju na bazu,predali joj modul db i funkciju u tom modulu za  
#dohvaćanje konekcije i baze, i ("./put do baze/Users.db- je ime baze")
root = tk.Tk()
root.title("Upravljanje korisnicima")

var_welcome = tk.StringVar(value="Pozdrav!")#varijabla StringVar za upis texta-usera,predali smo ju u pozdravni label,mijenja se varijabla kako se 
#mijenjaju useri, mogli smo ju ostaviti i praznu, to će pokazivati dok  nešto drugo ne upišemo, to će biti useri/admin
var_selected_user = tk.StringVar()# varijabla StringVar za upis stringa-dodanog usera/admina u label(listbox) koji je u frm_manage okviru


def login(): # funkcija za dohvaćanje username i passworda s kojim se login, dohvatimo username i password s ovim entryima ispod
    username = ent_username.get() #varijabli smo dali entry varijablu napravljenu u frame frm_login i .get() za dohvaćanje username
    password = ent_pass.get() # ent_pass entry varijabla napravljena u istom fram_login i dali joj varijablu i .get() da dohvati lozinku
#prije nastavka stvorili smo konekciju na bazu i bazu(get_connection) i dohvaćanje usera preko username-a(get_user)-napravljeno u db.py
    user = db.get_user(conn, username)#dohvati mi usera preko funkcije get_user iz modula db, predali smo gore stvorenu konekciju na bazu  
    # i username-znači dohvati mi usera sa ovim username-om, što je napravljeno u funkciji get_user(conn, username)
#dolje pitamo da li je user None ili je password kriv- user[1] != password, jer kod user=db.get_user dohvatili smo listu gdje je username kao [0],
# a password kao [1] element iz select_query u funkciji get_user, password-user[1] je različit od passworda koji smo upisali unutra- != password
    if user is None or user[1] != password: # onda login nije uspješan i dolje ispišemo što je 
        messagebox.showerror("Greska", "Pogresno korisnicko ime ili lozinka!")#pozvali smo messagebox.showerror-pokazuje error screen i upišemo 
        #poruku i kad pogrešno upiše, useru se otvori screen s tom porukom
        return # i vratimo return, jer je user lokalna varijabla, da ju izvučemo van iz funkcije kako bi radila??
#kad se ulogiramo, dok se ne odlogiramo disable cemo stvari preko kojih smo se ulogirali da se tu ništa ne može dogoditi dokse ne odlogiramo 
    ent_username.delete(0, tk.END)#rekli smo da se upisano u entry username izbriše(.delete) od 0 do kraja(tk.END)
    ent_username.config(state="disabled")#konfiguriramo taj entry na disabled, moramo upisati u config state(stanje)="disabled"-u stringu

    ent_pass.delete(0, tk.END) # isto kao za username
    ent_pass.config(state="disabled")

    btn_login.config(state="disabled") # isto smo disable i buton-gumb za prijavu-buton Prijava,kad upišemo korisnika i lozinku i klik na prijavu
    #-to sve je disable-ništa se tu ne može upisati ni klikati, isto tako se sve odmah i izbriše
    btn_logout.config(state="normal")#buton za logout(odjava) konfigurirali smo da pređe u state "normal"(enable smo ga) kad smo ulogirani-
    #a u tk.Button-kad smoga stvarali postavili smo ga na state=disabled kad kliknemo na njega, da se ne može koristiti dok smo logout,odjavljeni
#kad se user uspješno logirao, preko user = db.get_user(conn, username)
    frm_welcome.grid(column=0, row=1)#napravili smo da kad se bilo tko ulogira(gore),da se tek onda pokaže frm_welcome screen sa svojim sadržajem,
    # a dolje gdje smo napravili frm_welcome screen(okvir), zakomentirali smo ga
    var_welcome.set(f"Pozdrav {username}!")#u Label pozdravnog frame-frm_welcome-dali smo stringvar varijablu i nju .set()-postavljamo na "Pozdrav"
#u nju smo upisali taj string i {username}-kako bi pozdravili konkretnog usera-kad se prijavimo u Labelu tog frame pokaže se-Pozdrav username

#u frm_manage okvir zakomentirali smo njegov grid da se ne vidi kad se user prijavi,jer je samo za admina,a ispod smo napravili da se pokaže ako se
#ulogira admin
    if username == "admin": # ako je username jednako "admin"- to je ovdje određeno da je  username
        frm_manage.grid(column=0, row=2)#onda smo postavili frm_manage na grid-da se pokaže taj screen,ako nije ulogiran kao admin,neće se vidjeti
        load_users()# ako smo se ulogirali kao admin, onda loadamo usere preko funkcije za to-load_users, zato je ova funkcija unutar if-a
        # ako se nismo ulogirali kao admin nemamo što load usere, običan korisnik i ne vidi listu listbox, u ovoj fazi u listboxu pokazao se samo
        # admin user jer je samo on bio dodan 

#odjava usersa
def logout(): # pomoću mesaagebox.askquestion() pitamo usersa da li se želi odjaviti, pokaže se screen da yes/no
    ans = messagebox.askquestion(
        "Odjava", "Jeste li sigurni da se zelite odjaviti?")
#sa varijablom ans(answer) spremili smo u nju vrijednost odgovora koji je dao user yes/no kako bi mogli pitati ovo ispod sa if
    if ans == "no": # ako je odgovor jednako "no"
        return # onda ćemo samo return kao da nikad nismo ni stisnuli odjava
# ako smo klik yes, da smo se odlogirali onda radimo ovo ispod
    frm_manage.grid_forget()#manage screen maknili smo sa .grid_forget()-to je obrnuto od grid, moramo znati s čim smo postavili okvir
    #da smo ga postavili sa .pack(). onda bi morali napisati na taj okvir .pack_forget(), taj okvir vidi samo admin

    var_welcome.set("") #kao i kod login kod logout izbrisali smo stringvar pozdravnu varijablu sa .set("prazan string"),postavlja na prazan string
    btn_logout.config(state="disable")#konfigurirali smo odjavni buton na disable,kad se odjavimo,s .config mijenjaju se zadnje postavljene postavke
    frm_welcome.grid_forget()# maknili smo i pozdravni frame da se više ne vidi kad se logout

    ent_username.config(state="normal")#kad se odjavimo onda opet moramo enable sa .config(s tim se mijenjaju zadnje postavke) sve što smo
    ent_pass.config(state="normal")# s .config disable(onemogućili) u login funkciji, enable se radi sa state="normal"
    btn_login.config(state="normal")# to su korisničko ime lozinka i buton za prijavu


# za create novog usera koristimo iz tkintera tk.Toplevel- za otvaranje novog prozora, u tk.Buttonu(gumbu)-Dodaj nalazi se ova funkcija create_user
# i kad klik na gumb Dodaj, zbog korištenja tk.Toplevel otvori se novi prozor koji smo nazvali Dodaj korisnika
def create_user():
    tl_create_user = tk.Toplevel(root) #u novi prozor s tk.Toplevel uvijek stavimo root kao parent
    tl_create_user.title("Dodaj korisnika") # novom prozoru damo ime
    tl_create_user.focus() # s .focus() kad se otvori ovaj novi prozor da imamo odmah fokus na njega 
# funkcija za gumb dodaj, koji je napravljen u funkciji create_user
    def add_user(): # varijablama username i password dali smo entry varijable koje su napravljene u frame-u frm_login i na njih .get() da
# dohvate upisani username i lozinku u te entry varijable, uvijek mora ići .get() da se dohvate kad se upišu u napravljene Entrye
        username = ent_create_username.get()
        password = ent_create_pass.get()
# ovdje ne dozvoljavamo da username ili password budu prazni stringovi
        if username == "" or password == "": #ako je jedno ili drugo prazan string- return,vrati, if uvjet nije ispunjen return-vrati
            messagebox.showerror(  # ovdje smo ubacili i messagebox.showerror da pokaže error- sa natpisom što ne valja
                "Greska", "Korisnicko ime niti lozinka ne smiju biti prazni")
            return # u tom slučaju sa return vraćamo sve na početak upisa username i passworda, radi i bez messagebox
#kad je username i password upisan, moramo provjeriti da li taj user već postoji u bazi
#to radimo napravljenom funkcijom u db.py get_user(conn, username) u kojoj između ostalog provjeravamo da li konkretni user već postoji u bazi
# to je funkcija za dodavanje usera u sqlite3 bazu
# mogli smo to napraviti i da uzmemo query na bazi i taj query ubacimo u for petlju i provjerimo da li već imamo tog usera-vidi s Nikolom
        if db.get_user(conn, username) != None:# ako je ta funkcija različita(nije) od None- return,vrati-znači već postoji
            messagebox.showerror(  #i dali smo da ispiše error preko messagebox.showerror i pripadajući text-ide u zagradu u stringu
                "Greska", f"Korisnik {username} vec postoji!") # sa f"{username}"- dali smo da ispiše konkretni upisani username koji već postoji
            return # return da vrati na upis username i password
#ako nam je upit sa tom funkcijom jednak None-znači da taj user ne postoji u bazi i onda ga možemo dodati
#u db.py imamo funkciju add_user(conn, username, password) za dodavanje usera u bazu i nju koristimo 
#samo nju  ubacimo,postavimo, pozovemo u ovu funkciju add_user() koja je unutar ovdje glavne funkcije za dodavanje usera-create_user i preko nje 
#će se dodavati novi useri
        db.add_user(conn, username, password)
#nakon toga pokažemo poruku za korisnika da je uspješno dodan,,pomoću messagebox.showinfo(i u zagradi poruka u stringu, s f"{username}")-
#da piše konkretni user koji je dodan
        messagebox.showinfo("Dodaj korisnika",
                            f"Korisnik {username} uspjesno dodan!")

        tl_create_user.destroy() #kad se korisnik uspješno doda onda smo napravili s tl_create_user.destroy() da se taj novi prozor za dodavanje
        # usera automatski zatvori
# za kraj pozovemo funkciju load_users() koju smo napravili za dodavanje usera u listu-listbox, radi ažuriranja liste usera u bazi
        load_users()
#funkcija za gumb Izlaz, samo na novi prozor dodamo .destroy() i on se zatvori
    def close_create_screen():
        tl_create_user.destroy()
# ovdje u novi prozor dodajemo Labele i Entrye
    tk.Label(tl_create_user, text="Korisnicko ime:").grid(column=0, row=0)# Label da piše korisničko ime, root je novi prozor iz tk.Toplevel
    ent_create_username = tk.Entry(tl_create_user)# pored labela Entry za upis username, root je naravno novi prozor
    ent_create_username.grid(column=1, row=0)#grid da se pokaže na kojem je mjestu

    tk.Label(tl_create_user, text="Lozinka:").grid(column=0, row=1)#label lozinka
    ent_create_pass = tk.Entry(tl_create_user, show="*") #entry za pass, show="*" da ga sakrijemo sa zvjezdicama
    ent_create_pass.grid(column=1, row=1) #grid služi i da se pozicionira i da se pokaže gumb/label/widget

    tk.Button(tl_create_user, # gumb sa root novi prozor, natpis gumba, predamo funkciju da radi gumb, ta funkcija je stavljena u ovu
              text="Dodaj",  # funkciju create_user kao glavnu funkciju za dodavanje novog usera
              command=add_user).grid(column=0, row=2)# .grid da se pokaže i pozicioniranje gdje se nalazi

    tk.Button(tl_create_user, # gumb izlaz za closanje novog prozora, natpis gumba, funkcija za izvršenje, stavljena u glavnu funkciju
              text="Izlaz",         # create_user, ovu funkciju
              command=close_create_screen).grid(column=1, row=2)

    tl_create_user.mainloop()# kod tk.Toplevel, uvijek moramo imati i mainloop() za prikazivanje novog prozora

# funkcija za mijenjanje passworda usera
def update_password(): # ovdje odmah dohvaćamo username i novi pass koji želimo postaviti
    username = var_selected_user.get() #na username damo stringvar varijablu(koja se koristi za usera koji je u bazi,u label frm_manage) i .get()-dohvati
    new_password = ent_update_pass.get()# na new_password dodali smo entry varijablu za dodavanje novog passworda iz labela frm_manage i .get()-dohvati
# prvo pitamo da li je novi pass prazan, ako je prazan string onda damo da pokaže error i return
    if new_password == "":
        messagebox.showerror(
            "Greska", "Lozinka ne smije biti prazna!")
        return
#ako nije prazan string, onda pitamo DA LI user NE POSTOJI
    if db.get_user(conn, username) == None:# ako je user iz ove funkcije jednako None, znači da ne postoji
        messagebox.showerror(           # i javljamo grešku
            "Greska", f"Korisnik {username} ne postoji!")
        return # i sa return prekidamo operaciju
#prije promjene lozinke pitamo korisnika da li želi promjeniti lozinku s messagebox.askquestion(poruka u stringu)
    ans = messagebox.askquestion(  # messagebox.askquestion stavili smo u varijablu ans(answer)-tako smo ju nazvali
        "Promjena lozinke",
        "Jeste li sigurni da zelite spremiti promjene",
        icon="warning" # s icon="warning" možemo mjenjati iconu, kad pitamo askquestion pokaže taj icon
    ) # icon isto mora biti u zagradi askquestiona, pokaže se icona warning
    if ans == "no": # i onda pitamo ako je ans== "no"
        return # onda samo return, odustanemo od operacije promjene
# ako u if db.get_user() == None, to tako nije, znači ako postoji onda dodamo funkciju za ažuriranje passa u bazi,koja je napravljena u db.py
    db.update_password(conn, username, new_password)#ovdje je iza conn redoslijed parametara drugačiji nego je bio postavljen u toj istoj funkciji
    # u db.py
#nakon promjene lozinke dodamo messagebox.showinfo sa porukom(stringom) da je ista uspješno promijenjena
    messagebox.showinfo("Promjena lozinke",
                        f"Lozinka uspjesno promijenjena!")

    ent_update_pass.delete(0, tk.END) # za kraj deletali smo sve iz entrya ent_update pass koji je na početku funkcije postavljen na 
    #varijablu new_password kako nakon promjene lozinke nebi ništa ostalo upisano u tom entryu,npr. ako smo u entry počeli upisivati novu lozinku
    #pa smo odustali i kad klik u listbox na drugog usera, onda se to upisano delete


def delete_user():
    username = var_selected_user.get()#prvo moramo dohvatiti username usera kojeg želimo izbrisati iz baze,dohvaćamo pomoću stringvar varijable
#var_selected_user koja je u labelu frm:manage-a i s .get() dohvaćamo usera upisanog u tu varijablu, preko ove varijable upisujemo konkretnog
# usera kojeg želimo izbrisati, tako radi ovo dohvaćanje
    if username == "admin": # pitamo ako je username  jednako "admin"- username od admina, ubacimo .showerror() i return,vrati na početak
        messagebox.showerror(  # ako izbrišemo admina nećemo više ništa moći raditi u aplikaciji
            "Greska", "Nije moguce izbrisati korisnika admin!")
        return # napravili smo da se ne može izbriati admin, zato sa return vratimo brisanje na početak, returnamo se van iz brisanja
#ovdje ispod pitamo DA LI user NE postoji, zato smo upisali ako je funkcija za dohvaćanje usera iz baze db.get_user() jednaka None(nema), znači
# da user ne postoji u bazi i upišemo odgovarajuću poruku,string u message.showerror
    if db.get_user(conn, username) == None:
        messagebox.showerror(
            "Greska", f"Korisnik {username} ne postoji!")
        return # i return, idemo van iz brisanja
# prije brisanja usera i update usera pitamo askquestion da li stvarno želimo izbrisati korisnika ili mu promjeniti password
    ans = messagebox.askquestion(  #messagebox.askquestion(pitanje-string) spremili smo ans(answer) varijablu-tko smo ju nazvali
        "Izbrisi korisnika",
        f"Jeste li sigurni da zelite izbrisati korisnika {username}",
        icon="warning"  # u poruku možemo ubaciti i icon="warning" koja onda pokaže u messageboxu tu ikonu, radi i u .showerror
    )
    if ans == "no": # pitamo ako je ans== "no"
        return # onda se returnamo van, odustanemo
# ako je ovo gore sve u redu onda brišemo usera, ali prvo moramo napraviti podršku za brisanje usera-funkciju u db.py delete_user
#ako u if-u sa db.get_user je različit od None-znači da username postoji, onda predajemo ispod funkciju za brisanje iz baze napravljenu u db.py
    db.delete_user(conn, username)
# nakon brisanja username(usera) dodali smo messagebox.showinfo(i poruka-string u istom da je taj korisnik uspješno izbrisan)
    messagebox.showinfo("Izbrisi korisnika",
                        f"Korisnik {username} uspjesno izbrisan!")

    ent_update_pass.delete(0, tk.END) # za kraj deletali smo sve iz entrya ent_update pass, jer kad izbrišemo usera u listboxu pomakne se na 
    # drugog usera-kako nakon delete nebi ništa ostalo upisano u tom entryu za upis/promjenu lozinke pored labela lozinka u frm_manage
# radi ažuriranja liste u bazi, nakon izbrisanog usera dodajemo funkciju load_users() za ažuriranje usera u bazi
    load_users()


# s load users pročitamo sve usere (upisane, spremljene) iz baze i upišemo ih u napravljeni listbox u frm_manage i ažuriramo ih
def load_users(): # u ovoj funkciji usersi se upisuju u listbox(lb_users) i u label pored preko var_selected user varijable koja je u njemu
    usernames = db.get_all_usernames(conn) #za početak dohvaćamo usernames iz modula db i funkcije kojom dodajemo sve usere
#budući možemo više puta load sve usere iz baze u lb_users(listbox), onda bi se isti useri više puta dodali, pa ćemo zato prvo isprazniti lb_users
    lb_users.delete(0, tk.END) #lb_users deleteamo od 0(početak) do kraja (tk.END)-isprazni mi cijeli label,listbox 
#sad insertamo userse unutra, inserta se na index, možemo pratiti inedx na kojem jesmo i insertamo na taj index
    for i in range(len(usernames)): # vrtimo petlju po indexu[i] u rangeu dužine liste username(len(usernames))
      lb_users.insert(i, usernames[i])# u lb_users.insert na indeks i i želimo insertati usernames na [i],ova petlja kaže-idemo po svim indeksima i
     #i insertam na taj indeks tog usera- koliko god ih ima pojaviti će se u listbox
    #lb_users.insert(1, "user")#ovdje smo manualno insertali na drugi index-(1),na drugo mjesto,mjesto ispod-drugog usera naziva "user", radi
    #nekog primjera

#kad insertamo sve usere onda sktiviramo prvog od njih
    lb_users.activate(0) # s .activate(0) aktiviramo prvog usera(0) od svih koje smo insertali u gornjoj petlji u lb_users
    var_selected_user.set(lb_users.get(0))# ovdje smo aktivirali varijablu za upis izabranog usera u label koji je pored listboxa u frm_manage
    #sa .set(lb_users.get(0)) postavili smo u var_selected_user- korisnika kojeg smo aktivirali u listboxu. lb_user.get(0)-znači da nam dohvati
    # prvog usera od svih insertanih usera u lb_user varijabli napunjenoj gore u petlji, s .get(0)- get index možemo dohvatiti element na tom
    #indexu iz te liste, kako se mijenjaju useri u listboxklikom miša tako se mijenjaju useri u tom labelu pored

# funkcija za izvršenje bindanog eventa "<<ListboxSelect>>" na listbox, event se dogodi kad klikamo na neki element iz listboxa
def on_listbox_select(event): # uvijek moramo predati event jer je to event u takvoj funkciji,na taj parametar mora ići .widget za dohvaćanje istog
    widget = event.widget# u eventu postoji event.widget-služi za dohvaćanje widgeta-listboxa, lb_users je widget na koji smo bind Listboxselect i
#ovu funkciju, kad sam bind na lb_users keylistener i ovu funkciju tako samo dohvatio listbox iz lb_users na osnovi naredbe event.widget
    if len(widget.curselection()) == 0: #ako je duljina ovog 0, ako nismo stisnuli taj event koji je ispod, neka returna, izađe van,
        return # kako ne bi izbacio error ispod opisan
# ovo ispod .curselection()[0] je neki tuple i on je index retka kojeg smo stisnuli,i kad radimo nešto drugo, iz nekog razloga on trigera taj 
#event kojeg smo bindali, al mu tuple bude prazan jer nismo stisnuli na ništa pa izbaci error- tuple index out of range
    index = widget.curselection()[0]#.curselection()[0] znači da dohvati u widgetu(listboxu) prvi element-[0], dohvatili smo na koji index smo
# kliknuli, kad imamo index, na osnovi njega dohvaćamo username na kojeg smo kliknuli
    username = widget.get(index)#znamo index na kojeg smo stisnuli i sad smo dohvatili username koji se nalazi na tom indexu, widget je dohvaćeni
    #listbox i s .get(index) dohvaćamo index na kojeg smo stisnuli(kliknuli)-element u listi

    var_selected_user.set(username)# ovdje smo update varijablu za upis izabranog usera u label-u pored listboxa, tako na na nju sa .set()
    #postavimo dohvaćenog usera-username, i kad imamo više usera u listboxu, kako klikamo mišem na njih tako se u labelu pored mijenjaju njihova
    # imena
    ent_update_pass.delete(0, tk.END) # za kraj deletali smo sve iz entrya ent_update pass 
#kako ništa ne bi ostalo upisano u tom entryu za upis lozinke koji je pored labela lozinka u frm_manage, kad prebacimo na drugog usera u listboxu




# logi-in dio , ttk se isto može koristiti za izradu butona i entrya
frm_login = tk.LabelFrame(root, text="Prijava")#napravili smo frame za login pomoću LabelFrame,damo root i naziv frame-a, kad se predaje neki
# konkretni text-string onda mora ići text=
frm_login.grid(column=0, row=0)# postavimo ga na početne postavke

tk.Label(frm_login, text="Korisnicko ime:").grid(column=0, row=0)# label za korisničko ime, root je frame frm_login pa mu je grid opet 0
ent_username = tk.Entry(frm_login) #varijabla s entry za upis username-a, korisničko ime
ent_username.grid(column=1, row=0) # grid je isti red, drugi stupac

tk.Label(frm_login, text="Lozinka:").grid(column=0, row=1)#label za lozinku, root je isti frame, red ispod
ent_pass = tk.Entry(frm_login, show="*")#varijabla s entry za upis lozinke, vrijednost show="*", znači da istu prikaže s zvjezdicama
ent_pass.grid(column=1, row=1)#pozicioniranje,na label je odmah stavio .grid(),dok na entry varijable nije,već ju je ispod ponovio pa .grid()
# kod varijabli za frame-tk.LabelFrame isto je .grid() stavio u varijablu ponovljenu ispod

btn_login = tk.Button(frm_login, text="Prijava", command=login)# gumb za prijavu(login),isti frame je parent,i funkcija za izvršenje butona
btn_login.grid(column=0, row=2, columnspan=2)# pozicioniranje gumba, s columnspan=2-da se gumb protegne na 2 stupca

# kad se koristi tk.LabelFrame onda ide i text u LabelFrame a kod tk.Frame, nema texta, već samo okvir??

frm_welcome = tk.Frame(root) # pravimo pozdravni frame,parent je opet root
#frm_welcome.grid(column=0, row=1)# ovaj frame je ispod login frame-a,zakomentirali smo ga da se pozdravni label i logout buton ne vide dok se 
#bilo tko ne ulogira, kad se ulogira onda se se pokažu, to je napravljeno u funkciji login()

tk.Label(frm_welcome, textvariable=var_welcome).grid(column=0, row=0)# pozdravni label,root je pozdravni frame, a za text smo predali varijablu
#zato što će se mijenjati u zavisnosti koji je user ulogiran, kad se predaje varijabla mora ići textvariebale=
btn_logout = tk.Button(frm_welcome,  # parent, buton koji se klika za odjavu
                       text="Odjava",  # što će pisati na njemu
                       command=logout,  # funkcija za izvršenje
                       state="disabled")#ovdje smo postavili sa state="disabled"-da bude disabled kad napravimo logou,odjavut-sve dok se ne 
#ulogiramo,a u funkciji login(),konfigurirali smo ga na state="normal"- da se vrati iz disabled kad se ulogiramo
btn_logout.grid(column=1, row=0)# pozicioniranje butona-gumba, pored pozdravnog labela

frm_manage = tk.Frame(root) # frame za  manageriranje, upravljanje
#frm_manage.grid(column=0, row=2)#okviri su pozicionirani jedan ispod drugog u istom stupcu,zakomentiramo ga da se ne prikazuj za usere,jer
#taj frm_manage okvir je za admina, a ne za druge usere,u funkciji login, napravljeno je da se taj okvir pokaže ako se admin ulogirao

lb_users = tk.Listbox(frm_manage)#tk.Listbox-pravi prazan okvir(box) u zadanom frame-u,upisuju se admin i drugi useri pomoću funkcija
lb_users.bind("<<ListboxSelect>>", on_listbox_select)#na listboxu bindamo selectanje tog listboxa, poseban event za listbox, taj event se
#stavlja u ove dvostruke << >> i dodamo funkciju za izvršenje tog eventa, tako da kad klikamo mišem na različite usere u listboxu, preko 
#dodane funkcije tako se mijenjaju njihova imena u labelu pored listboxa
lb_users.grid(column=0, row=0, rowspan=3)#rowspan=3-da se proteže kroz 3 reda

tk.Button(frm_manage, text="Dodaj", command=create_user).grid(column=0, row=3)#ispod listboxa napravili smo gumb-dodaj i dali funkciju za izvršenje
# da se kreira-stvori user, kad da funkciju u bilo kojem butonu,za početak gore napravi samo naziv funkcije i pass, pa ju poslije popuni

tk.Label(frm_manage, textvariable=var_selected_user).grid(
    column=1, row=0,columnspan=3)#label u kojem piše izabrani user/admin,predali smo string varijablu,jer će se mijenjati,razvukli na 2 stupca,
    # taj label je pored listboxa, i prikazuje izabranog usera

tk.Label(frm_manage, text="Lozinka:").grid(column=1, row=1) #label da piše Lozinka:
ent_update_pass = tk.Entry(frm_manage) # entry za upis lozinke odmah pored labela Lozinka:
ent_update_pass.grid(column=2, row=1)
# i napravljeni su butoni za spremanje i brisanje u tom istom frame-u, dobili su naziv, funkciju što rade i pozicionirani su preko .grid()
tk.Button(frm_manage,
          text="Spremi",
          command=update_password).grid(column=1, row=2)

tk.Button(frm_manage,
          text="Izbrisi",
          command=delete_user).grid(column=2, row=2)

root.mainloop()

