import tkinter as tk


class Animal: #klasa Animal ne zna za Dog i Cat
    def __init__(self, name): #rekli smo da svaka životnja ima ime
        self.name= name # postavili smo ime u konstrukt

class Dog(Animal):# klasa Dog je naslijedila klasu Animal, klasa Dog je onda primjerak klase Animal, rekli smo svaki pas je životinja ali nije
    #svaka životnja pas, klasa je naslijedila SVA svojsta životinje i plus ima neka svoja specifična svojstva
    def __init__(self, name):#kad smo napravili konstrukt name za psa nećemo sad u psu reći self.name=name, jer name već imamo u nadklasi Animal               
        super().__init__(name) #poslali smo nek se pozove konstruktor moje nadklase,Animal, on će ishendlat name, sa super() smo naslijedili sva
        #obilježja klase Animal
        self.wof="woof!" # klasa Animal ne zna za taj wof, to je specifično za psa, i wof smo dali u klasu Dog da ga hendla
# ove varijable su izvan klase
pas1 = Dog("Mirko") # predali smo na pas1 klasu Dog i predali joj name iz njegovog konstruktora 
pas1.name # pas1 predstvalja klasu Dog i možemo upisati pas1.name iako nigdje u klasi Dog nismo rekli self.name=name, nego smo name delegirali u 
#klasi Animal jer ona zna hendlati sve te zajedničke stvari

class Labrador(Dog): #ova klasa je naslijedila klasu Dog, svaki labrador je pas, al nije svaki pas labrador, rekli smo u ovom nizu da je svaki
    #labradori i animal
    def __init__(self, name): # ovdje labrador primi ime, 
        super().__init__(name) # klasa kaže Dog zna hendali ime, a Dog će reći Animal mi zna hendlat ime
lab1= Labrador("Ime psa") # lab1 predali smo klasu Labrador i ime/name iz njegovog konstruktora
lab1.name # sad lab1 predstavlja klasu Labrador -možemo doći do imena(.name) koje je hendlano preko klase Dog, koje je hendlano preko klase Animal
lab1.wof # možemo doći i do wof jer je to naslijeđeno iz klase Dog(samo Dog to ima), to je vezano za super().__init

class Cat(Animal): # klasa Cat je naslijedila klasu Animal,rekli smo svaka mačka je životinja ali nije
    #svaka životnja mačka
    pass


#može se naslijediti i više klasa zajedno, ne mora samo jedna

class App(tk.Tk): 
    def __init__(self, db_client):
        super().__init__() 

        self.db_client = db_client 

        self.title("Sense Simulator") 
        self.geometry("500x300")
    def a(): #metoda specifična za App
        pass
    # tu rade sve stvari iz tk-a kao što je grid, pack, labeli, sve što se može koristiti u klasi Tk


root = tk.Tk # ovaj root je == kao super().__init__() u Class App koja je naslijedila tk.Tk- i naslijedili smo sve njene atribute i metode pa tako
# i .mainloop što je atribut klase Tk i zato u main() kad smo napravili app = gui.App(), mogli smo poslije napraviti app.mainloop()


#  kad kažemo
root = App(tk.Tk) # ovo je App koji je naslijedio Tk
#nad root možemo pozvati bilo koju metodu koju možemo pozvati u tk.Tk plus još metode koje su specifične za App kao što je
root.a()# metoda napravljena u App()
