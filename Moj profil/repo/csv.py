# Nakon što smo ovo napravili u my_profile.py, napravili smo podfolder repo, potrebni __init__.py i spremili u poseban file ovu funkciju

# Funkcije smo radili nakon što smo kreirali tabove i unutar njih labele i butone
# Spremi listu data u CSV datoteku
"""def save_csv(path, data): # moramo predati argumente,parametre da znamo što želimo save-ati,moramo imati putanju-path-spremi mi na tu putanju
                                # i data-kojeg želimo spremiti
       with open(path, "w") as f: #otvorili smo putanju za pisanje(path,"w")jer želimo podatke pisati uvijek iznova,otvorili smo kao f file       
            f.write(";".join(data))"""# pišemo u data i sa - ";".join - rekli smo da podatke u data spajamo sa ;- to je delimiter-može i neki drugi
# u csv podaci, data upisuju se sa .write()
#kad kliknemo na radiobuton csv spremi se data.csv u csv obliku pod Moj profil/data, s elementima liste csv navedenima u funkciji save_data()

# kad smo ovu funkciju prebacili ovdje, nazvali smo ju umjesto save_csv(path, data)- samo save(path,data), valjda zato što je sad u csv.py
# nakon toga smo u my_profile.py napravili from repo import csv, json, db- da se ovi moduli mogu odavdje tamo importirai

def save(path, data):                        
       with open(path, "w") as f:        
            f.write(";".join(data))

