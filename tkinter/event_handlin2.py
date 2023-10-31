import tkinter as tk

# pravimo funkcije za zbrajanje i oduzimanje

def add():            #(0, tk:END) znači od nule pa do zadnjeg znaka preko ove funkcije tkinetra
    txt_en_res.delete(0, tk.END)#prvo moramo izbrisati prethodni rezultat u Entry za rezultat i moramo reci od kojeg do kojeg znaka
# sad dohvaćamo brojeve koje cemo zbrojiti odnosno oduzeti
    num1 =  int(txt_en1.get())# pretvorimo u integer prvi Entry jer je text(string), s .get() dohvaćamo vrijednost koja je upisana u Entry
    num2 = int(txt_en2.get())# ovo je drugi Entry, drugi broj
# sad te brojeve zbrajamo
    result = num1 + num2
# i onda taj rezultat insertamo u Entry za rezultat
    txt_en_res.insert(tk.END, str(result) )#u zagradi kazemo na koje mjesto insertati,(0)-na nulto mjesto,na početak,(tk.End)-dodamo na kraj,
# i kažemo šta da doda, to je rezultat u stringu, mora biti string jer se u Entryu prikazuje string
 #budući imamo .delete() neće se rezultat dodavati jedan iza drugog zbog tk.END u .insert,kod (0) rezultat bi se dodao na prvo mjesto


def sub(event): #funkcija za keylistenere mora imati event,iako smo ga ignorirali u funkciji, jer dolje u bind znamo koji je keylistener
    txt_en_res.delete(0, tk.END )

    num1 =  int(txt_en1.get())
    num2 = int(txt_en2.get())

    result = num1 - num2

    txt_en_res.insert(tk.END, str(result))
        


root = tk.Tk() 

root.title("Sedma tkinter aplikacija")
root.geometry("600x400")

lbl1 = tk.Label(root, text="Prvi broj")
lbl1.grid(column=0, row=0)
txt_en1 = tk.Entry() #tk.Entry() služi da možemo sami upisivati neki text, pojavi se prozor u rootu za upisivanje texta
txt_en1.grid(column=1, row=0) # column=1 da txt_en1 bude pored lbl1

lbl2 = tk.Label(root, text="Drugi broj")
lbl2.grid(column=0, row=1) # lbl2 i txt_en2 stavili u drugi red u usporedbi sa lbl1 i txt_en1, pojave se jedno ispod drugog
txt_en2 = tk.Entry() 
txt_en2.grid(column=1, row=1) 

# sad stavljamo gumbe

btn_add = tk.Button(root, text="Zbroji", command=add) # buton za zbrajanje, dodali smo u komandu funkciju za zbrajanje,najbolji način
btn_add.grid(column=0, row=2) # dali smo mu grid() gdje će biti

btn_sub = tk.Button(root, text="Oduzmi") # buton za oduzimanje
btn_sub.grid(column=1, row=2)
btn_sub.bind("<Button-1>", sub) # ovdje smo za oduzimanje bindali listener, a kod zbrajanja(za primjer) dali smo command=funkcija za radnju
#"<Button-1>" listener znači-ljevi klik miša i dodamo samo funkciju sub za izvršenje keylistenera,ljevi klik miša ide na buton "Oduzmi"
# sad pišemo rezultat, svaki key listener ide u stringove i u jedne ove < >, jedino ListboxSelect ide u ove dvostruke << >>
lbl_res = tk.Label(root, text="Rezultat") # label je za widgete, a Entry je za prostor(prozor) za upisivanje
lbl_res.grid(column=0, row=3) # mijenjamo columne 0 i 1 da widgeti budu jedno pored drugog, i rowse da budu jedno ispod drugog
txt_en_res = tk.Entry() 
txt_en_res.grid(column=1, row=3) 



root.mainloop() 



