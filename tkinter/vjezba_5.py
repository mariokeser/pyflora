import tkinter as tk


root = tk.Tk() 

root.title("Peta tkinter aplikacija")
root.geometry("600x400")
#pravimo grid 3x3, znači sa 9 elemenata, grid() ima redove i kolone, grid(column=, row=)

for i in range(3): #konfiguracija kolone(column) ili reda(row) svakog i elementa da se resiza do određene veličine kad se ekran(root) smanjuje
    root.columnconfigure(i, weight=1, minsize=75)# moraju biti i weight i minsize da bi radila konfiguracija
    root.rowconfigure(i, weight=1, minsize=75)
    for j in range(3):  #borderwidth i relief=tk:RAISED daju da ovih 9 elemenata izgledaju kao gumb,inače izgledaju samo npr. 0x0, 0x1,itd
        frame= tk.Frame(root,borderwidth=3,relief=tk.RAISED ) #frame je kao neki kontejner za organizaciju gdje se što nalazi na rootu

        frame.grid(row=i, column=j, padx=15, pady=15)# na widgetu grid() elementi isto idu od 0, redovi i kolone

        label = tk.Label(frame, text=f"{i} x {j}")# u frame možemo stavljati druge widgete, 
        label.pack(padx=15, pady=15)  #.pack() da se widget pokaže. #sad je frame "parent" od label umjesto root jer smo isti predali u frame

root.mainloop() 
