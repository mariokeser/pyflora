from cgitb import text
import tkinter as tk

def click():
    label.config(text="Gumb kliknut!", font=("Helvetica", 18), fg="red")# u funkciji smo dali naredbu za konfiguraciju labela,
    #kad se klik na btn napravljen ispod koji ima ovu funkciju u comandu, onda se Poruka iz labela, pretvori u ovo napisano u label.config


root = tk.Tk()
root.title("Treca Tkinter aplikacija")
root.geometry("600x400")

label = tk.Label(root, text="Poruka", font=("Arial", 24))
#label je widget koji sadržava text,ne pišemo u njega,ali sadržava text i prikazuje ga,damo root,font je tuple,dali smo vrstu i veličinu fonta
# i u pack možemo svašta zadavati, zadali smo pad- pomiče buton?, možemo zadavati i margine
label.pack(padx=30, pady=40) # ovdje smo pack morali staviti posebno na label, a ne chainati, kad je bio chain izbaci error, zbog nekog
                    # returna funkcije, naziv label je u funkciji click()

btn = tk.Button(root, text="Klik!", command=click).pack(padx=10, pady=10)
img = tk.PhotoImage(file="tkinter/python_logo_icon.png").subsample(20) # uvezemo sliku,sa subsample smanjimo sliku ako nam je prevelika
label_img = tk.Label(root, text="Ovdje je slika!",
                      compound=tk.CENTER, image=img).pack(padx=5, pady=10)# dodajemo sliku u label=root, text, polozaj, sliku i pack
                                    # sad možemo chain pack jer label_img nije u funkciji click()

root.mainloop()