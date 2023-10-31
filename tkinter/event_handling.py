#Event handling je svaki kontakt mišem i tipkovnicom sa aplikacijom, ljevi, desni, klik, klik na tipkovnici, klik i držanje klika s mišem, 
# howeranje mišem 
import tkinter as tk

entered_chars = ""   # napravili smo varijablu gdje će biti sva do sad unesena slova, zato je prazan string i ista ide u funkciju

# rezultat ove funkcije dolje je da se ispisuje u prozoru kad ga otvorimo sve što upisujemo u terminal
def handle_keypress(event):  #funkcija za hendlanje evenata, zato ima parametar (event)- dohvaća sve akcije
    print(event.char) # ispisuje character koji smo stisnuli na tipkovnici, bez ovog text se ispisuje samo u prozoru
    global entered_chars # moramo ju u funkciju spremiti kao globalnu varijablu, inače shadowa gornju varijablu kao nova istog naziva
    entered_chars += str(event.char) # rekli smo da dodajemo u varijablu sve iz event.char i da to stvori u string - str(event.char)
    txt_var.set(entered_chars) # u varijablu txt_var koja je postavljena kao string(dolje) .set-amo varijablu za spremanje stringova



root = tk.Tk() 

root.title("Prva tkinter aplikacija")
root.geometry("600x400")

#tkinter je za sve "primitive" napravio posebne klase-klasa koja se zove ime "primitive" pa Var, StringVar, IntVar,
 # za varijabilne dijelove koje želimo mijenjati u našoj aplikaciji

txt_var = tk.StringVar() # tu smo rekli da je ova varijabla string
txt_var.set("Ovdje idu unesena slova!")# postavljamo vrijednost string varijabli pomoću .set

lbl_title = tk.Label(root, text="Dogadjaj")
lbl_title.grid(column=0, row=0)

lbl_out = tk.Label(root, textvariable=txt_var, fg="red")#widget za ispisivanje slova koje pišem na tipkovnici, pomoću textvariable=txt_var
lbl_out.grid(column=0, row=1) # grid je drugačiji naprema lbl_title da ne budu na istom mjestu

root.bind("<Key>", handle_keypress) # keylistener za hendlanje evenata mora se bindat na root i da se funkcija za hendlanje evenata
               # <Key> je tip eventa, keypress, na google ima popis evenata za bindanje, jedan od njih je keypress-<key>
# kad se pokrene izvršenje pokaže se prozor, ali i kad se tipka bilo što na tipkovnici to se ispisuje u terminalu
# znači bindali smo root da sluša <key> eventove i kad se to dogodi izvršit će se  handle_keypress funkcija

root.mainloop() 



