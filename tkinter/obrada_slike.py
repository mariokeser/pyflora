import tkinter as tk
from tkinter import filedialog # ovo je za funkciju load_image(),da otvori onako kako se u mom OS sustavu otvara kad izabirem s mog OS neki file
from PIL import Image, ImageTk # s Image loadamo sliku, s ImageTk pravimo kontejner za slike u tkinteru, upload sliku iz PIL i tkinter

root = tk.Tk() #stvorimo root
root.title("Obrada slike") #damo rootu naslov

# globalne varijable za loadanje slike, jer su izvan funkcije
photo_filename = "./tkinter/algebra_ucionica.jpg" #putanja do slike, global varijabla koju možemo mijenjati kad učitamo neku drugu sliku
width = 800 # odredili smo dimenzije slike,da uvijek bude ista,na ovaj način i kad druge slike upload sa diska-risajzaju se na ovu veličinu
height = 550
# sa PIL Image otvorimo sliku, resize ju kako smo napisali-u tupleu i convertali smo da radimo sa uvijek istim tipom, modom slike
img = Image.open(photo_filename).resize((width, height)).convert(mode="RGB")#global varijabla koju možemo mijenjati kad primjenjujemo razne filtere 
#img.show() # sad se pokaže slika al to nije slika u tkinter windowu, već u windowu koji se otvori kad napravim show nad PIL slikom-Image.open-PIL
#sliku iz PIL-a prebacujemo u tkinter okvir,kontejner, a onda sliku prebacimo u label(widget)-napravljeno pod komentarom Slika
img_tk = ImageTk.PhotoImage(img) # predali smo sliku u tkinter preko modula iz PIL-a, loadali smo sliku iz PIL-a


def flip_left_right():
    global img, img_tk  #upisali smo global img i img_tk jer nećemo mijenjati lokalne varijable u funkciji već ćemo mijenjati vanjske varijable
                        #konkretno-kad flipamo sliku mi želimo flipati slike izvan funkcije koje su stavljene u img i img_tk okvir/kontejner
    img = img.transpose(Image.FLIP_LEFT_RIGHT) # img smo pomoću transpose funkcije flipali left-right-to je iz PIL modula
    img_tk = ImageTk.PhotoImage(img) #a ispod img  moramo upisati istu sliku-koja je predana u tkinter okvir
    lbl_img.config(image=img_tk) #ovdje konfiguriramo sliku iz labela, jer lbl_img(dolje napravljen) stoji takav kakav je dok mu ne kažemo ovo je
#nova slika koju moraš pokazati,img_tk predan u parametar image u ovoj funkciji je nova slika napravljena u ovoj funkciji-kako je iznad napravljeno
# lbl_img preko config predali smo na novu sliku napravljenu u funkciji, u tom trenu se mijenja slika na ekranu
#varijabla lbl_img ne  mora ići u global jer primjenjujemo metodu nad njom, a varijablama iznad dodajemo nove vrijednosti i tako ih mijenjamo
# ispod smo napravili funkcije za 3 upravljačka gumba


def save_image():
    img.save(f"{photo_filename}_01.jpg", "JPEG")#spremimo sliku PIL naredbom-.save i predamo img-u sliku spremljenu u photo_filename,"JPEG" je 
    # mode u koji save sliku,kad klik na save buton na slici ista se save u vsc codu,i svaki put kad se save - override prethodno save-anu sliku 
# def close_image():
    #root.destroy #funkcija za zatvaranje slike, samo treba napraviti buton sa close i predati ovu funkciju, .destroy() doda se rootu
    #root.quit() # u ovom slučaju radi isto, zatvara sliku

def load_image(): # i ovdje uzimamo globalne varijable jer globalno mijenjamo sliku, ovdje dodajemo neku drugu sliku
    global img, img_tk, photo_filename #treba i photo_filename jer ćemo loadati neku drugu sliku

    photo_filename = filedialog.askopenfilename(title="Izaberi sliku")#pitat će nas da se otvori filename(ime u stringu) i damo naslov 
                            #kad klik na otvori na slici, u ovoj fazi otvori mi documents u OS, dobili smo putanju do novog file
    img = Image.open(photo_filename).resize((width, height)).convert(mode="RGB")# pa nam treba Image.open, otvorimo sliku s tog
    # filename da ju resiza i konvertira
    var_img_props.set(f"Mod slike:\t\t{img.mode}\nDimenzije slike:\t{img.size}")#StringVar postavljen na label buton u 9. retku
        # prikazuje mode i size nove slike, pomoću naredbe .set()-postavi
    img_tk = ImageTk.PhotoImage(img)# onda ide prikaz te slike
    lbl_img.config(image=img_tk) # i postavimo label da tu sliku prikažemo u widgetu

def reset_image(): #budući sliku resetamo iz vanjskih varijabli, moramo uzeti slike iz globalnih varijabli, isto kao u flip_left_right()
    global img, img_tk # zato je i postupak isti kao u flip_left_right(),samo što ovdje promjenjenu sliku resetamo, vracamo kakva je bila
    img = Image.open(photo_filename).resize((width, height)).convert(mode="RGB")#predamo original sliku iz PIL-a
    img_tk = ImageTk.PhotoImage(img)# predamo sliku iz tkintera
    lbl_img.config(image=img_tk) # i konfiguriramo sliku iz labela



# Slika, sliku prebacujemo u label(widget) nakon što smo istu upload iz PIL-a u tkinter okvir- napravljeno gore pod globalne varijable
lbl_img = tk.Label(root, image=img_tk)#labelom(widgetom) ćemo prikazati slike na ekranu,lbl_img stavimo u root i predamo sliku preko parametra
lbl_img.grid(column=0, row=0, rowspan=9) #label stavimo u grid,s rowspan=9 rekli smo da se slika proteže kroz 9 redaka,toliko će nam trebati 

#Gumbi
tk.Button(root, text="Flip lijevo-desno",   # gumb predan u root i u parametar predan text gumba
          command=flip_left_right).grid(column=1,row=0, padx=10, pady=10,ipadx=5,ipady=5)#padxy određuje udaljenost između gumba i slike
#command na funkciju da buton radi kako je napisano i grid-postavljanje butona na mjesto,ipadxy određuje iznutra udaljenost između texta i gumba
#funkcije na comand= primjenjuju se na klik gumba,pa tim funkcijama nije potreban return,funkcija koja ništa ne vraća, ne bi trebala primiti
# nijedan argument. Znači da funkcije koje primaju argumente trebaju return?

#upravljački gumbi- 
frm_mng_buttons = tk.Frame(root) #za njih smo napravili novi frame
frm_mng_buttons.grid(column=1, row=7)
#sad pravimo gumbe
tk.Button(frm_mng_buttons,  # predali smo novi frame, njihov parent
          text="Spremi",
          command=save_image).grid(column=0, row=0) # buton za save, row je 0 jer je ovaj buton u novom frame-u
tk.Button(frm_mng_buttons,  # predali smo novi frame, njihov parent
          text="Otvori",
          command=load_image).grid(column=1, row=0) # buton za open, row je 0 jer je ovaj buton u novom frame-u
tk.Button(frm_mng_buttons,  # predali smo novi frame, njihov parent
          text="Resetiraj",
          command=reset_image).grid(column=2, row=0) # buton za reset, row je 0 jer je ovaj buton u novom frame-u


#Info o slici,to se može mijenjati obzirom da možemo loadati druge slike pa smo to stavili u neku string varijablu pomoći tk.StringVar(value=)
var_img_props= tk.StringVar(value=f"Mod slike:\t\t{img.mode}\nDimenzije slike:\t{img.size}")
#props znači neki property,img je PIL slika i nad img pozvali smo .mode-to je iz PIL-a,\t-tab,\n-novi redak,nad img pozvali smo .size- iz PIL-a
# onda napravimo Label koji će sadržavati tu varijablu
tk.Label(root,  
textvariable=var_img_props,  #varijabla u label predaje se pomoću textvariable=,preko grid, row=8 stavili smo label u 9. redak
justify="left").grid(column=1,row=8)#justify="left" poravna smo mode i size img-a u lijevo,te vrijednosti upisali smo na početku-img=Image.open(...)


root.mainloop()