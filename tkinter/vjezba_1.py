# tkinter, najrašireniji modul za izradu GUI - grafičko korisničko sučelje, GUI-graphical user interface od str. 78, GUI
import tkinter as tk
# red rada s tkinterom, chain rada, hijerarhijska struktura, redoslijed rada

root = tk.Tk() # prvo se stvara root u kojeg stavljamo sve ostakle stvari  u aplikaciji

root.title("Prva tkinter aplikacija")
root.geometry("600x400")# visinaxsirina, dali smo dimenzije rootu

root.mainloop() #dodajemo da nam program traje i otvara prozor toga roota,aplikacije, vrti se loop da traje




