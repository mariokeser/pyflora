import gui # import smo gui file jer ga ovdje želimo pokrenuti
# sa main postavili smo file koji nam je ulazna točka
if __name__ == "__main__":
    app = gui.App() # ovdje postavili grafičko sučelje tako da smo varijabli app dali iz modula gui-klasu App kojom smo napravili grafičko sučelje,
    # s ovim gore kao da smo rekli app= tk.Tk i stvorili root, ali će se unutra stvoriti i ostale stvari koje smo dali konstruktoru App()
    app.mainloop() # i tu moramo dati mainloop() kao bi root gore mogao raditi, tog mainloopa nema u klasama gui modula
