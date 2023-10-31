import requests # moduli za dohvaćanje stranice sa html podacima sa stranice coinmarketcap za kriptovalute
from bs4 import BeautifulSoup

#dolje je napravljen put do te stranice URL_CRYPTO =
URL_CRYPTO = "https://coinmarketcap.com" # sa copy coinmarketcap.com i ovdje paste-paste-alo se i https://, stringove smo sami dali

# napravili smo ovu klasu za kriptovalutu jer u nju moramo staviti cijenu i ime za svaku kriptovalutu,ova klasa ide u funkciju fetch_crypto()
class Cryptocurrency:
    def __init__(self, name, price): # napravili smo init za name i price kriptovalute, self uvijek mora ići na početku inita-radili smo to prije 
        self.name = name # u vezi inita 
        self.price = price #dali smo svakom parametru(desno) varijablu(ljevo) sa self.

# ova funkcija je za vraćanje/dohvaćanje cijena i imena kriptovaluta
def fetch_crypto():
    page = BeautifulSoup(requests.get(URL_CRYPTO).content, "html.parser")# sa page= i modulima BeautifulSoup(za parsiranje podataka) i unutar njega
    #requests.get(u requestu predali smo put do stranice)s .content sluzi za dohvacanje sadrzaja stranice u bytes, i string html.parser- piše se
    #kad se parsira sa beutifulSoupom na kraju istog, mogali smo prvo napraviti varijabla=requests.get(URL).content, pa onda ići na varijabla=
    #beautifulSoup(i unutra varijabla od requests i "html.parser"-string uvijek ide na kraju ovog modula)-dohvatili smo tu stranicu sa svim podacima,
    #print(page.prettify())# s ovom naredbom u funkciji i ispod pozivom funkcije u terminalu smo dobili podatke te stranice
#fetch_crypto()
    # onda smo isli na stranicu da ju inspect, trazili smo div koji ce plavom bojom oznaciti te kriptovalute, 
    #kad smo nasli taj div i kad smo ga otvorili nasli smo tablicu-string table na kojeg kad stavimo mis oznace se sve valute,ispod njega je bio 
    #body koji se zvao tbody ispod kojeg su bile sve valute pojedinacno oznacene sa tr-svaka
    #tables = page.select("table")#potrazili smo tablice sa svim valutama, na page smo isli .select i u stringu naveli table, jer su u tom table
    # bili sve valute oznacene sa tr, da vidimo koliko će biti tablica sa valutama
    #print (len(tables)) # da vidimo koliko tables ima stranica, bila je jedna
    #rows= page.select("table tbody tr") dohvaćamo sve retke valuta(tr) iz taga tbody iz taga table-idemo od općenitijeg prema konkretnom stringu
    #print(len(rows))# za valute da vidimo koliko ima redaka-bilo ih je 100, takve su oznake u toj tablici kod inspecta
    # kad klik na konkretni tr jer ima ovaj puni znak < otvore se elementi svakog retka kao što je zvjezdic,  redni broj, ime, cijena i dalje
   

    rows = page.select("table tbody tr")[:10]# ovdje smo preko [:10] odredili sa zelimo samo prvih 10 valuta u listi rows, jer samo za prvih 10
    #odmah daje sve vrijednosti, za ostale valute dao je samo 5 elemenata jer ih loada dinamički,to je pokazao kad smo ispod print(len(columns))

    cryptos = []# naravili smo listu za ubacivanje redaka
# dolje je petlja za dohvaćanje kolona sa imenima i cijenama, vrijednosti jedna ispod druge 
    for row in rows: 
        columns = row.select("td")# sa .select dohvacamo iz svakog row(retka) iz liste rows "td"-string oznaka za sve elemente jednog retka valute
        #print(len(columns))# u terminalu smo dohvatili broj vrijednosti(elemenata)svakog retka-koliko ih ima
        crypto_name = columns[2].select_one("p").text# columns[2]-znaci 3 vrijednost(ime),columnu smo dali .select_one jer zelimo dobiti samo taj
        #jedan text, ("p")-pored imena valute(npr Bitcoin) bio je naziv <p>(paragraf) što se odnosilo na naziv valuta i to smo dali u select_one 
        #i .text- znači da si zelimo uzeti text iz njega-string <p>, kad print(crypto_name)-da njihova imena
        crypto_price = float(columns[3].select_one(
            "a").text[1:].replace(",", ""))# cijena je četvrta vrijednost,element[3].select_one("a").text-selectamo samo text iz <a koji je 
        #označavao cijenu,float smo uzeli jer je cijene izbacivao u stringu("a"),na text[1:] izbacili smo prvi element[0] iz cijene koji je 
        #oznacavao $, kad smo išli print(crypto_price) izbacio je error could not convert string to float:"27,402,02"-imali smo zareze, a float
        #poznaje samo točke, pa smo napravili na kraju .replace(",", "")- da zamijeni zarez u stringu sa praznim stringom. Nakon svake napravljene
        #varijable radio je print(ta varijabla) da provjeri da li to radi i kako to pokazuje
# ispod smo u praznu listu cryptos appendali gore napravljenu klasu Cryptocurrency i predali umjesto njezinih parametara nase varijable za
# ime i cijenu kriptovaluta 
        cryptos.append(Cryptocurrency(crypto_name, crypto_price))

    return cryptos # moramo vratiti van iz funkcije varijablu(listu) je je lokalna vrijabla da ju mozemo koristiti izvan funkcije

# ovdje smo samo isprobali da li funkcija radi, tako što smo za svaki element crypto u funkciji fetch_crypto dali da printa crypto.name i
#crypto.price- to su objekti klase Cryptocurrency koja je predana u tu funkciju-.name i .price -objekti te klase kojima smo predali varijable 
#crypto_name i crypto_price kad smo ih appendali u listu cryptos, crypto je element u petlji po kojem se iterira a .name i .price su varijable koje
# smo stvorili sa self.name i self.price u klasi Cryprocurrency
"""
for crypto in fetch_crypto():
    print(crypto.name, crypto.price)
"""
