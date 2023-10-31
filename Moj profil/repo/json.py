# Nakon što smo ovo napravili u my_profile.py, napravili smo podfolder repo, potrebni __init__.py i spremili u poseban file ovu funkciju
import json # kako bi radio json.dump()
#spremi rječnik data u json datoteku
"""def save_json(path, data):  # parametri isti kao i za spremanje csv-a
    with open(path, "w") as f:
        json.dump(data, f, indent=4)"""# kod jsona podaci(data) upisuju se sa .dump(data, na file f i indentali smo da data bude jedno ispod drugog)
# kad klik na radiobuton json spremi se pod Moj profil data.json u json obliku s key:values navedenima u funkciji save_data

# kad smo ovu funkciju prebacili ovdje, nazvali smo ju umjesto save_json(path, data)- samo save(path,data), valjda zato što je sad u json.py
# nakon toga smo u my_profile.py napravili from repo import csv, json, db- da se ovi moduli mogu odavdje tamo importirai

def save(path, data):  
    with open(path, "w") as f:
        json.dump(data, f, indent=4)