import tkinter as tk
from tkinter import Toplevel # modul za stvaranje tabova
from PIL import Image, ImageTk # za otvaranje slika Image, i ImageTk za stavit sliku iz PIL-a u tkinter kontejner
from tkinter import filedialog # filedialog služi dodavanje slika
root = tk.Tk()
root.title("Moj profil")

def on_button_click():
    new_window = Toplevel(root)
    new_window.title("new_window")

var_status = tk.StringVar(value="Status ok" )
photo_filename = "./Moj profil/images/profile_placeholder.jpg"
img = Image.open(photo_filename).resize((50,100))
img_obj = ImageTk.PhotoImage(img)

tk.Button(root,anchor="ne", text = "Kuhinja-\npolica pored prozora", image=img_obj,compound="left", command=on_button_click).pack(fill="y")
tk.Entry(root, textvariable=var_status, justify="right" ).pack()






root.mainloop()
