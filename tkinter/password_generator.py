import tkinter as tk # import modula za generiranje lozinke
import random # za random generiranje lozinke
import string # za generiranje liste slova i znakova .letters i .digits
# pravimo funkcije za gumbe za password- generiranje, kopiranje i resetiranje

def set_password_visibility(): #pitamo na što je postavljena varijabla var_show_pass
    if var_show_pass.get() == "show": # ako je varijabla postavljena na show, sa .get() dohvaćamo što želimo
        ent_pass.config(show="")#postavili smo u ovu varijablu Entry za password kako bi password mogli konfigurirati kako hoćemo
#ako je var_show.pass = show, onda postavi Entry na show=""-prazan string, to je default, znači da taj parametar nije podešen
 # sa .config() možemo namještati u svim gumbima sav config koji stavljamo unutra preko tk.Radiobutton(), isto možemo i u widgetima 
    else:
        ent_pass.config(show="*") # inače postavi Entry ove varijable na zvjezdicu


def generate_password():
    password = ""   # prazan string za generiranje lozinke

# sad stvaramo character po charater za generiranje lozinke
    for _ in range(var_pass_len.get()): #iteriramo po broju charactera,broj charactera nam je zadan u ovoj varijabli,.get()-za dohvaćanje
        if var_characters.get() == "letters": #za svaki character pitam koji nam je radiobuton pritisnut da znam koje charactere
                        #uopće smijem uzimati u obzir, slova ili brojevi ili oboje - u klasi var_characters i .get() je za dohvaćanje istog
            char=random.choice(string.ascii_letters) #choice metoda kojoj kad date listu daje element iz liste.Uzeli smo random choice
                                                    # od svih ascii slova iz importiranog modula string
        elif var_characters.get() ==  "numbers": # ovdje ako u varijablu/klasu StringVar dohvaćamo brojeve
            char=random.choice(string.digits)     #stavimo u char -random choice iz liste brojeva preko modula string.digits  
        else:
            char= random.choice(string.ascii_letters + string.digits) #inače dodajemo obje -iz lista slova i brojevi
        password += char  # dodamo u naš password dobiveni character
    var_password.set(password) # za kraj postavimo dobiveni password na var_password sa .set(). get()-dohvati, .set()- postavi     

def copy_password(): # kopiranje trenutnog passworda
    root.clipboard_clear() # prvo clipboard_clear-očistimo password, ako ga imamo kopiranog od prije, clipboard vežemo na root
    root.clipboard_append(var_password.get())# apendamo(dodamo) varijablu u kojoj smo generirali password- pomoću clipborad.append
# i s .get() dohvatimo string iz varijable,ima i clipboard_get-to sve je povezano sa copy/paste/get text(string), povezan sa pyperclip module
# paste radi-kad klik na buton- kopiraj lozinku, onda istu paste u vsc

def reset_password(): # resetiramo varijable na ove koje su bile na početku
    var_characters.set("nl") # sa var_charaters.set("nl") postavili smo varijablu kakva je bila na početku
    var_show_pass.set("show") # za show i hide passworda
    var_pass_len.set(value=10)
    var_password.set("") # posatvili na prazan string jer je tako varijabla postavljena na početku 
root = tk.Tk()
root.title("Generator lozinki")

# pravimo generator lozinki
# prvo idu varijabilni dio sustava, koji ćemo mijenjati kroz naše gumbe, vrijednosti u stringu su proizvoljne, a preko tk.Radiobutton
# upisuju se vrijednosti koje nam trebaju - u stringu koji smo postavili preko value=""
var_characters = tk.StringVar(value="nl") #pravimo varijablu za lozinku slova i brojevi, zato smo predali value="nl", numbers i letters
var_show_pass = tk.StringVar(value="show") # varijabla da se prikaze lozinka, default je da se prikaže lozinka, za hide ćemo to napisati
var_pass_len = tk.IntVar(value=10)# var za dužinu lozinke(slider), koliko želimo imati charactera, postavili smo defaultni value na 10
var_password = tk.StringVar() # varijabla za generirani password, na početku je prazan string, default je prazan string za password
#preko tk.StringVa stvorili smo klase u koje onda dohvaćamo vrijednosti sa .get(), te vrijednosti dohvaćamo u value=""

#sada pravimo gumbe, prvo smo napravili okvir-layout, napravili smo 3 frame jedan ispod drugog i unutra idu druge stvari, gumbi, prozori,itd
lbl_frm_settings = tk.LabelFrame(root, text="Postavke")# root je parent od svih drugih widgeta, ispod ide geometry manager-grid()
lbl_frm_settings.grid(column=0, row=0)# pravimo stupce i retke u koje će ići gumbi, prozori i sve drugo, frame "Postavke" ide u nulti
# pravimo setove radiobutona kroz kolone i retke
#Radiobuttons - Slova/brojevi- pravimo prva 3 radiobutona, slova i brojevi, slova, brojevi
tk.Radiobutton(lbl_frm_settings,    #parent
               text="Slova i brojevi",  # naziv gumba
               variable=var_characters,    # predajemo varijablu koju ćemo mijenjati
               value="nl").grid(column=0, row=0) #predamo vrijednost koju ćemo mijenjati u varijabli var_characters,
                # value je "nl" i dajemo poziciju butonu preko grid()

tk.Radiobutton(lbl_frm_settings,    #parent
               text="Slova",  # naziv gumba
               variable=var_characters,    # predajemo varijablu koju ćemo mijenjati
               value="letters").grid(column=1, row=0)#predamo vrijednost koju ćemo mijenjati u varijabli var_characters,value je sad "letters"
#dajemo poziciju butonu preko grid(),da je gumb stisnut znamo po tome koja je nam vrijednost u varijabli koju on mijenja

tk.Radiobutton(lbl_frm_settings,    #parent
               text="Brojevi",  # naziv gumba
               variable=var_characters,    # predajemo varijablu koju ćemo mijenjati
               value="numbers").grid(column=2, row=0) #predamo vrijednost koju ćemo mijenjati u varijabli var_characters,
                     # value je sad "numbers" i dajemo poziciju butonu preko grid()


# Radiobuttons- Prikazi/sakrij, pravimo  druga 2 radiobuttona -prikazi lozinku, sakrij lozinku
tk.Radiobutton(lbl_frm_settings,    # od radiobuton parent je frame koji smo stvorili gore, u njega idu butoni 
               text="Prikazi lozinku",  # onda predajemo text od tog butona, buton za prikaz lozinke
               variable=var_show_pass,   # moramo predati i varijablu koju ćemo mijenjati
               value="show", #stavimo vrijednost koju ćemo promijeniti,u var_show_pass postavili smo "show" kao value
               command=set_password_visibility).grid(column=0, row=1)# naredba za funkciju koja skriva ili pokazuje password
#i taj buton stavili smo u grid,znači kad stisnemo na radiobutton prikazi lozinku,varijabla var_show_pass će vrijednost promjeniti na show

tk.Radiobutton(lbl_frm_settings,    # parent je isti
               text="Sakrij lozinku", # buton za sakrij lozinku
               variable=var_show_pass,  # varijabla je ista
               value="hide",    # value je drugi-"hide", 
               command=set_password_visibility).grid(column=2, row=1)#naredba za funkciju koji skriva/pokazuje pass i grid je u drugoj koloni

# Slider - duzina lozinke
tk.Scale(lbl_frm_settings, # slider radimo sa tk.Scale, damo parenta
         orient="horizontal",  # orijentaciju možemo damo horizontal i vertical
         variable=var_pass_len,    # predamo varijablu za slider
         length=400, 
         from_=8,  # sa from_= i to= lozinki smo dali najmanji i najveći broj charactera
         to=40).grid(column=0, row=2, columnspan=3)#moramo ju postaviti na njezino mjesto,upakirati sa grid,sa columnspan=3 dali smo lozinki
#da se proteže kroz sve 3 kolone,ali mu duzina nije bila od početka do kraja kolona,to je riješeno sa lenght=300, sa width ide vertikalno

#Frame- gumbi, između slidera i frame-a, za lozinku ubacujemo gumbe za genereirana, kopirana i resetirana lozinka
frm_action_buttons = tk.Frame(root) # opet u frame ubacujemo njegov parent, to je root
frm_action_buttons.grid(column=0, row=1)# damo poziciju ixmeđu slidera i generirane lozinke

# sad slažemo gumbe
#Button- generiraj
tk.Button(frm_action_buttons, # damo mu njegov parent
text="Generiraj lozinku", # njegov text
command=generate_password).grid(column=0, row=0)#predamo mu njegovu funkciju za akciju preko command, pozicije sa grid postavljaju 
                                                #  se unutar pripadajućeg frame-a
#Button- kopiraj
tk.Button(frm_action_buttons, # damo mu njegov parent
text="Kopiraj lozinku", # njegov text
command=copy_password).grid(column=1, row=0)#predamo mu njegovu funkciju za akciju preko command, pozicije sa grid postavljaju 
                                                #  se unutar pripadajućeg frame-a

#Button- resetiraj
tk.Button(frm_action_buttons, # damo mu njegov parent
text="Resetiraj lozinku", # njegov text
command=reset_password).grid(column=2, row=0)#predamo mu njegovu funkciju za akciju preko command, pozicije sa grid postavljaju 
                                                #  se unutar pripadajućeg frame-a


# frame za gereriranu lozinku, to je poseban frame, frame - lozinka
frm_pass = tk.Frame(root,) # za ovaj zadnji frame uzeli smo tk.Frame, dok smo za prvi uzeli tk.LabelFrame, parent je root
frm_pass.grid(column=0, row=2) # dali smo mu mjesto, columni i rows idu kao i liste, prvo mjesto se označava sa 0, row=2 je treci redak

tk.Label(frm_pass,text="Generirana lozinka",  #u widget label ubacili smo njegov parent,dodali njegov text i grid(pozicija)
         font=("", 14)).grid(column=0, row=0) # namjestili smo veličini texta, bez promjene pisma, s praznim stringom

ent_pass = tk.Entry(frm_pass,  #napravili smo varijablu za generiranje lozinke, napravili smo Entry za upis texta lozinke,predali frm_pass
                    textvariable=var_password,  #u textvariable predali smo gore stvorenu variablu za generiranje passworda
                    font=("", 16), #font je tuple, za praznim stringom ostavili smo isto pismo text,samo smo sa 16 promjenili veličini slova
                    width=30) # ovo je širina prozora za generiranje texta
ent_pass.grid(column=0, row=1)# opet smo preko grid varijablu upakirali na njenu poziciju


root.mainloop()

