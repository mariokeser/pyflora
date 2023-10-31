import tkinter as tk

# red rada s tkinterom, chain rada, hijerarhijska struktura, redoslijed rada
# na tk.Button može se naći puno opcija
def click():
    print("Gumb kliknut!")

root = tk.Tk() # prvo se stvara root u kojeg stavljamo sve ostakle stvari  u aplikaciji, to je prozor

root.title("Druga tkinter aplikacija")
root.geometry("600x400")# visinaxsirina, dali smo dimenzije rootu
button = tk.Button(root, text="Mali gumb")# pravimo widget,button moramo mu dati prozor na kojem se nalazi, to je trenutno root i damo text
                    # ne pokaže ništa dok mu ne kažemo na koji način da se pokaže
button.pack() # ovim smo  buttonu rekli da se pokaže, widget pack() služi da se nešto pokaže
button_clickable = tk.Button(root, text="Klikni!", command=click).pack()#pack() se može chainat, moramo dati pack() da se to pokaže
 #damo mu text,moramo mu dati i funkciju da se izvrši na klik gumba, dali smo mu funkciju preko command=click,ta funkcija je napravljena gore
#ovdje se na prozoru pokaže ispod Mali gumb, drugi gumb na kojem piše klikni, kako smo i zadali u textu,a kad se klikne,u terminalu se izvrši
# i ispiše se Gumb kliknut!, kako smo i naveli u funkciji koju smo predali button_clickable

img = tk.PhotoImage(file="tkinter/python_logo_icon.png").subsample(20)#ovo služi za dodavanje slike,u file damo sliku koju smo dovukli u vsc 
btn_img = tk.Button(root,text="Gumb sa slikom", command=click,compound=tk.LEFT,             
                    relief=tk.GROOVE,state=tk.DISABLED,image=img).pack()#predali smo root,text,sliku,komandu,polozaj slike,dizajn 
#imamo gumb sa slikom,kad se klikne izbaci sliku,ali se text ne vidi,pomoću naredbe compound=tk.LEFT-slika bude ljevo i vidi se text desno
# kad mu predamo da je DISABLED onda se gumb ne može koristiti

root.mainloop() #dodajemo da nam program traje i otvara prozor toga roota,aplikacije, vrti se loop da traje




