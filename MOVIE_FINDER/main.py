import client # importirani moduli koje smo napravili u client.py i gui.py, predali smo klijenta u gui aplikaciju
import gui
"""
# od ovog ispod pa do def main() je sve izbrisao kad je napravio sve u client.py, tu je  isprobavao kako to radi
#import json #modul za json kako bi mogao raditi .dumps(),u client.py nije trebao .dumps() za čitanje json-a. Mislim zbog tamo metode get_movies?
#import requests # modul za dohvaćanje web stranice



URL_MOVIES = "https://www.omdbapi.com" # url put do stranice
api_key = api_key = open("./api_key.txt").read() # put do apikey

# response kao u metodi get_movies u klasi OmdbClient,jedino je u params stavljen konkretni query(upit)"marvel", konkretna stranica i na
#"r":"json"}).json() kako bi ispod odmah radio print sa konkretnim podacima u json-u, ovdje je response izvan klase/metode
response = requests.get(URL_MOVIES, params = {"apikey": api_key,
                                             "s": "marvel",
                                             "page": 3,
                                             "r": "json"}).json()
print(json.dumps(response, indent=4))#u print smo dali na json-naredbu .dumps da da response unutra kao dictionary u pythonu,(učili smo ste naredbe) 
#indent=4-da ima indent-da bude čitljiviji dictionary
"""
# ovdje u mainu je dao api_key(put do njega) i url preko movie_client = na importirani modul client dao je klasu iz njega OmdbClient i unutra
#predao zadane(spremljene) parametre od te klase a to je prvo url-put do stranice i drugo api_key-koji je potreban za svaki poziv na API stranicu
def main():
    api_key = open("./api_key.txt").read()
    movie_client = client.OmdbClient("https://www.omdbapi.com", api_key)
# s ovim printom isprobali smo da li ovo u main()radi, 
    #print(movie_client.get_movies("marvel"))#na movie_client(spremljeni put do API stranice) pozvali smo metodu iz OmdbClient za dohvaćanje filmova
# metoda napravljena nad klasom da bi radila mora biti pozvana, "marvel" je njezin zadani parametar query/search od get_movies()
#drugi primjer je:
    #page_1, _, _ = movie_client.get_movies("abc")#tu nam trebaju samo movies iz returna funkcije get_movies,return movies,total_results,total_pages
    #pa smo za movies dali page_1, a za ovo drugo samo placeholdere _, _. Return ove funkcije je napravljen kao tuple, ovdje je sa 3 vrijednosti i
    #budući se očekuju 3 vrijednosti iz tuple returna moramo staviti prije jednako 3 vrijednosti ili barem underscorove
    #for movie in page_1: # stavili smo movie iz page_1 na .title koji je između ostalih stvari spremljen u klasu Movie iz client.py
        #print(movie.title)# dobili smo u terminalu titlove filmova iz prve stranice, jer je u get_movies stavljen kao default page=1
    app = gui.App(movie_client) #u varijablu app predali smo iz importiranog modula gui njegovu klasu .App i predali joj njezin parametar koji
    # smo joj dali u init-u, sad je u app gui aplikacija za prikazivanje dohvaćenih filmova, gui aplikaciji predali smo klijenta iz clijent.py
    # za dobivanje filmova u gui aplikaciji
    app.mainloop() #dodajemo .mainloop() na app da nam program traje i otvara prozor toga roota,aplikacije app, vrti se loop da traje, 
    #gui aplikacija napravljena je sa klasom App u modulu gui.py


if __name__ == "__main__": # napravili smo da se tu spremi main funkcija i da se ne može importirati negdje dalje(to smo učili)
    main()

# da bi funkciralo ovo ispod treba ići u main()
# Objašnjenje kako je return funkcije get_movies tuple -return movies,total_results,total_pages, jer smo ga napravili u get_movies kao tuple
    #response = movie_client.get_movies("abc") # kad u gui app upišemo abc i search
    #print(response) #u terminalu je izbacio objekt klase Movie,samo prikaz objekta,filmove, pa ukupan broj filmova i ukupan broj stranica kao tuple
    #movies = response[0] #ovo je za filmove, prvi tuple
    #total_movies = response[1] # za ukupan broj filmova, drugi tuple
    #total_pages = response[2]# za ukupan broj stranica, treci tuple, nismo dali u print pa nije izbacilo ništa
# još jedan primjer
#   #movies, total_movies, total_pages = movie_client.get_movies("abc")
    #print(total_movies, total_pages) #izbaci ukupan broj moviesa i ukupan broj stranica u terminalu,prvo otvori gui,upiše u search pa klik search
    #for movie in movies:
        #print(movie.titles) # izbaci u terminalu naslove filmova, prva stranica, valjda zato što su filmovi u API prikazani po stranicama
    # mogli smo i ovako tražiti samo movies
    #movies = movie_client.get_movies("abc")[0] mogli smo i ovako tražiti samo prvu vrijednost iz tuple, prvi element i print(movies)
