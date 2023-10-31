import repo # importali smo bazu koju smo napravili
import gui # isto i tkinter koji smo napravili

# simulator je main aplikacija koja povezuje gui i repo, baze iz repo i tkinter prozor iz gui
def main():
#sad u mainu stvaramo klijenta na bazu, napravili smo varijablu db_client i njoj predali iz repo.py, clasu DbClient-klasa za bazu
#stvorio sam klijenta na bazu, da bi klijent na bazu radio moramo dati i ime baze u u klasu za bazu, u repo.py je toj klasi predan samo
#db_name kao argument,a ovdje ćemo dati konkretno ime,stvorili smo podfolder data za putanju(gdje će biti) i dali smo ime bazi readings.db
#readings smo izmislili(jer ćemo tu svašta različito očitavati-temperature, humidity,..) a .db je oznaka za bazu(file koji je baza),
#spremili smo bazu u "data/readings.db", kad se stvori konekcija na bazu u DbClient i ovdje pokrene def main(), onda će se stvoriti baza u data
    db_client = repo.DbClient("SENSE_EMU/data/readings.db") #jedna klasa postavljena u main

    app = gui.App(db_client) #na app dali smo iz gui.py njegovu napravljenu klasu App koja ima tkinter za prozor,i predali smo joj klijenta na bazu
    #da ga može koristiti, klinet na bazu je stvoren ovdje , druga klasa postavljena u main
    app.mainloop() # i .maninloop na app kako bi se tkinter prozor mogao ovdje pokazati


if __name__ == "__main__": # spremili smo main funkciju u ovo da se ne može importati iz drugih modula(to smo naučili u osnove programiranja)
    main()
