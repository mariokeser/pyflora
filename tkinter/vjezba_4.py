# radimo sa geometry manager, glavna 3 su pack, grid i place, za slaganje widgeta, od str. 83
# pack slaže widgete jedan ispod drugog
# grid slaže widgete u okviru tablice, ima redove i stupce(kolone), najviše se koristi
import tkinter as tk


root = tk.Tk() 

root.title("Cetvrta tkinter aplikacija")
root.geometry("600x400")

img = tk.PhotoImage(file="tkinter/python_logo_icon.png").subsample(170)
btn_img = tk.Button(root,text="Gumb i slika!", image=img, compound=tk.LEFT).place(x=150, y=75)#koristimo .place() umjesto .pack()
label=tk.Label(root, text="Neka oznaka").place(x=200, y=90) # .place() omogućava overlaping 2 widgeta, ovdje su btn_img i label
root.mainloop() 





