from tkinter import *
from tkinter import Tk, Toplevel, Label, LabelFrame,Button, Entry, Frame, messagebox, ttk, Canvas, filedialog
from tkinter.messagebox import askyesno
from PIL import Image, ImageTk 
from repo import db



#konekcija na bazu podataka
conn = db.get_connection("./pyflora/GUI/data/Pyflora.db")
#root GUI-a
root = Tk()
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


#prvi window za login
def login_window(): 
    global tp
    tp=Toplevel()
    tp.withdraw()
    def login():
        username = ent_username.get() 
        password = ent_pass.get() 
        user = db.login(conn, username)
        if user is None or user[1] != password: 
            messagebox.showerror("Error", "Wrong username or password!")
            return
        else:
            root.withdraw()
            main_window("<Button-1>")
    root.attributes("-fullscreen", False)
    root.title("")
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=True)
    Label(frame,bg="green", text="Pyflora Container",font=("Arial", 28)).pack(anchor="ne", expand=True,fill=X, side=TOP, ipady=5)
    frm_login=LabelFrame(frame,fg="green", text="Log in", font=("Arial", 30,))
    frm_login.pack(anchor="n", side=TOP, expand=True)
    Label(frm_login,bg="green", text="User name:").grid(row=2, column=0, padx=30, pady=30)
    ent_username = Entry(frm_login) 
    ent_username.grid(row=2, column=1) 
    ent_username.focus()
    Label(frm_login,bg="green", text="Password:").grid(row=3, column=0, padx=30, pady=30)
    ent_pass = Entry(frm_login, show="*")
    ent_pass.grid(row=3, column=1)
    button_login=Button(frm_login,fg="green",text="Log in", command=login, width=10)
    button_login.grid(row=4, column=0, columnspan=2, pady=20)
    def update_date_profile(event):
        login()
    root.bind("<Return>", update_date_profile)
    

# za pohranu/odustanak od dodavanja novih pycontainera i povrat na window sa listom pycontainera-main window

def store_addnew_pycontainer():
    global id_herb
    def remove(string):
            return string.replace(" ", "") 
    if remove(input_container_name.get()) == "":
        messagebox.showerror("Error!", "When creating pycontainer - name is mandatory!")
        return
    else:
        db.add_containers(conn=conn, name=input_container_name.get(),herb_id =id_herb)
    input_container_name.set("")
    main_window("<Button-1>")
def cancel_addnew_container():
    main_window("<Button-1>")


input_container_name = StringVar(value=" ")
id_herb = StringVar(value="")
def addnew_pycontainer(event):
    global tp
    tp.withdraw()
    tp = Toplevel()
    width=tp.winfo_screenwidth()
    height=tp.winfo_screenheight()
    tp.geometry("%dx%d" %(width, height))
    tp.title("")
    frame = LabelFrame(tp)
    frame.pack(side=TOP, fill=X, ipady=10)
    l1=Label(frame, text="PyFlora Container", font=("Arial", 23), fg="green")
    l1.pack(side=LEFT, expand=True)
    l1.bind("<Button-1>", main_window)
    l2=Label(frame, text="Herbs", font=("Arial", 23), fg="green")
    l2.pack(side=LEFT, expand=True)
    l2.bind("<Button-1>", herbs_window)
    Button(frame, text="MY PROFILE",fg="green", command=my_profile,width=12, height=1).pack(side=LEFT, expand=True)
    Button(tp, text = "SYNC", fg = "green", width=12).pack(anchor=E, side=TOP, pady=20, padx=173)
    frame_2 = Label(tp)
    frame_2.pack(fill=BOTH, expand=True)
    Label(frame_2, text="Pycontainer", fg="green", font=("Arial", 20)).grid(row=0, column=0, sticky="w",pady=50, padx=173)
    Label(frame_2, text="Pycontainer name", fg="red").grid(row=1, column=0, sticky="w",  pady=5, padx=173)
    Entry(frame_2, textvariable=input_container_name,  background="white", fg="black", width=50).grid(row=2, column=0, pady=5, padx=173)
    all_herbs = db.get_all_herbs(conn=conn)
    all_herbs.append({"id": [0], "name" :"Empty pycontainer"})
    option_list = []
    for herb in all_herbs:
        option_list.append(herb["name"])
    value_inside = StringVar(frame_2)
    value_inside.set("Select option")
    def get_herb_name(*args):
        global id_herb
        for herb in all_herbs:
            if herb["name"] == value_inside.get():
                id_herb = herb["id"]     
        return id_herb
    herb_menu = OptionMenu(frame_2, value_inside, *option_list, command=get_herb_name) 
    herb_menu.config(width=46)
    herb_menu.grid(row=2, column=1, sticky="w")
    store_button =Button(frame_2, text="STORE", command=store_addnew_pycontainer, height=1, width=12)
    store_button.grid(row=7, column=0, sticky="w", pady=220, padx=180)
    cancel_button =Button(frame_2, text="CANCEL", command=cancel_addnew_container, height=1, width=12)
    cancel_button.grid(row=7, column=0, sticky="e", pady=220, padx=173)
    return event

# za gumb update/ažuriranje podataka o postojećim containerima

def store_update_pycontainer():
    var_container_name.set(edit_container_name.get())
    db.update_container(conn, name=var_container_name.get(), container_id=var_container_id.get(), herb_id=id_herb)
    details_pyflora_container("<Button-1>", var_container_id.get())

def cancel_update_pycontainer():
    details_pyflora_container("<Button-1>", var_container_id.get())
edit_container_name = StringVar(value=" ")
edit_container_id = StringVar(value="")
edit_con_herb_id = StringVar(value="")
def update_pycontainer(event):
    global tp, id_herb, no_id_herb
    tp.withdraw()
    tp = Toplevel()
    width=tp.winfo_screenwidth()
    height=tp.winfo_screenheight()
    tp.geometry("%dx%d" %(width, height))
    tp.title("")
    frame = LabelFrame(tp)
    frame.pack(side=TOP, fill=X, ipady=10)
    l1=Label(frame, text="PyFlora Container", font=("Arial", 23), fg="green")
    l1.pack(side=LEFT, expand=True)
    l1.bind("<Button-1>", main_window)
    l2=Label(frame, text="Herbs", font=("Arial", 23), fg="green")
    l2.pack(side=LEFT, expand=True)
    l2.bind("<Button-1>", herbs_window)
    Button(frame, text="MY PROFILE",fg="green", command=my_profile,width=12, height=1).pack(side=LEFT, expand=True)
    Button(tp, text = "SYNC", fg = "green", width=12).pack(anchor=E, side=TOP, pady=20, padx=173)
    frame_2 = Label(tp)
    frame_2.pack(fill=BOTH, expand=True, padx=160)
    edit_container_name.set(var_container_name.get())
    edit_container_id.set(var_container_id.get())
    
    
    if var_container_herb_id.get() != "None":
        edit_con_herb_id.set(var_container_herb_id.get())
        herbs_id, herb_name, soil_moisture, luminosity, air_temperature, ph_value, features, herb_height, herb_width, image = db.get_herb(conn, edit_con_herb_id.get())
    else:
        herb_name = "Empty pycontainer"
        

    Label(frame_2, text="Pycontainer", fg="green", font=("Arial", 20)).grid(row=0, column=0, sticky="w",pady=50, padx=50)
    Label(frame_2, text="Change Pycontainer name", fg="red").grid(row=1, column=0, sticky="w",  pady=5, padx=50)
    Entry(frame_2, textvariable=edit_container_name,  background="white", fg="black", width=50).grid(row=2, column=0, pady=5, padx=50)
    
    all_herbs = db.get_all_herbs(conn=conn)
    all_herbs.append({"id": [0], "name" :"Empty pycontainer"})
    option_list = []
    for herb in all_herbs:
        option_list.append(herb["name"])
    value_inside = StringVar(frame_2)
    value_inside.set(herb_name)
    def get_herb_id(*args):
        global id_herb
        id_herb = db.get_herb_id_by_name(conn, name=value_inside.get())
        return id_herb
    herb_menu = OptionMenu(frame_2, value_inside, *option_list, command=get_herb_id)
    herb_menu.config(width=46)
    herb_menu.grid(row=2, column=1, sticky="w", padx=22)
    store_button =Button(frame_2, text="STORE", command=store_update_pycontainer, height=1, width=12)
    store_button.grid(row=7, column=1, sticky="w", pady=180, padx=25)
    cancel_button =Button(frame_2, text="CANCEL", command=cancel_update_pycontainer, height=1, width=12)
    cancel_button.grid(row=7, column=1, sticky="e", pady=180, padx=20)
    return event


#varijable za input iz get funkcije u entrye, labele i canvas
var_herb_id = StringVar(value="")
var_herb_name = StringVar(value="")
var_herb_moisture = StringVar(value="")
var_herb_air_temp = StringVar(value="")
var_herb_ph = StringVar(value="")
var_herb_features = StringVar(value="")
var_herb_height = StringVar(value="")
var_herb_width = StringVar(value="")
var_herb_luminosity = StringVar(value="")
var_herb_image = StringVar(value="")

# za select/get images
herb_image = StringVar(value="")
bigimg_herb_photo = None 
smallimg_herb_photo = None 
images = []
thumbnail_photo = Label()


# za dohvaćanje i prikaz imagesa iz
def get_images(): 
     global bigimg_herb_photo, smallimg_herb_photo, thumbnail_photo, thumbnail_herb_photo, input_herb_photo
     if input_herb_photo == "":
         return
     else:
        big_img = Image.open(input_herb_photo).resize((303, 303))
        bigimg_herb_photo = ImageTk.PhotoImage(big_img)
        small_img = Image.open(input_herb_photo).resize((100, 140)) 
        smallimg_herb_photo = ImageTk.PhotoImage(small_img)
        img_thumb = Image.open(input_herb_photo).resize((300,300))
        img_thumb.thumbnail((80,200))
        thumbnail_herb_photo = ImageTk.PhotoImage(img_thumb)
        thumbnail_photo.config(image=thumbnail_herb_photo)
def add_herb_photo():
        global input_herb_photo, herb_image
        input_herb_photo = filedialog.askopenfilename(title="Select herb image")
        herb_image.set(input_herb_photo)
        get_images()   

# za dodavanje novih biljaka u windowu addnew herb
input_herb_name = StringVar(value=" ")
input_soil_moisture =StringVar(value=" ")
input_luminosity = StringVar(value=" ")
input_air_temperature = StringVar(value=" ")
input_ph_value = StringVar(value=" ") 
input_features = StringVar(value=" ")
input_herb_height = StringVar(value=" ")
input_herb_width = StringVar(value=" ")
input_herb_photo = "./pyflora/GUI/images/herb_photo.jpg"
        
def store_addnew_herb(): # za dodavanje u bazu db.add_herbs-radi, isključena je samo zbog isprobavanja drugih funkcija
    global herb_image, input_herb_photo
    def remove(string):
            return string.replace(" ", "") 
    if remove(input_herb_name.get() and input_soil_moisture.get() and input_luminosity.get() and input_air_temperature.get() and input_ph_value.get() 
              and input_features.get() and input_herb_height.get() and input_herb_width.get() and herb_image.get() ) == "":
        messagebox.showerror("Error!", "All parameters must be chosen!")
        return
    else:
        db.add_herbs(conn=conn, name=input_herb_name.get(), soil_moisture=input_soil_moisture.get(), luminosity=input_luminosity.get(), air_temperature=input_air_temperature.get(),
            ph_value=input_ph_value.get(), features=input_features.get(), herb_hight=input_herb_height.get(), herb_width=input_herb_width.get(),image=herb_image.get())
    input_herb_name.set("")
    input_soil_moisture.set("")
    input_luminosity.set("")
    input_air_temperature.set("")
    input_ph_value.set("")
    input_features.set("")
    input_herb_height.set("")
    input_herb_width.set("")
    herb_image.set("")
    get_images()
    herbs_window("<Button-1>")

def cancel_addnew_herb():
    herbs_window("<Button-1>")

def addnew_herb(event):
    global tp, thumbnail_photo, input_herb_photo
    tp.withdraw()
    tp = Toplevel()
    width=tp.winfo_screenwidth()
    height=tp.winfo_screenheight()
    tp.geometry("%dx%d" %(width, height))
    tp.title("")
    frame = LabelFrame(tp)
    frame.pack(side=TOP, fill=X, ipady=10)
    l1=Label(frame, text="PyFlora Container", font=("Arial", 23), fg="green")
    l1.pack(side=LEFT, expand=True)
    l1.bind("<Button-1>", main_window)
    l2=Label(frame, text="Herbs", font=("Arial", 23), fg="green")
    l2.pack(side=LEFT, expand=True)
    l2.bind("<Button-1>", herbs_window)
    Button(frame, text="MY PROFILE",fg="green", command=my_profile,width=12, height=1).pack(side=LEFT, expand=True)
    Button(tp, text = "SYNC", fg = "green", width=12).pack(anchor=E, side=TOP, pady=20, padx=173)
    frame_2 = Label(tp)
    frame_2.pack(fill=BOTH, expand=True, padx=160)
    Label(frame_2, text="Herb", fg="green", font=("Arial", 20)).grid(row=0, column=0, sticky="w",pady=40, padx=50)
    Label(frame_2, text="Add herb name", fg="red").grid(row=1, column=0, sticky="w",pady=5, padx=50)
    Entry(frame_2, textvariable=input_herb_name,  background="white", fg="black", width=50).grid(row=2, column=0, pady=5, padx=50)
    Label(frame_2, text="Add soil moisture", fg="red").grid(row=3, column=0, sticky="w",padx=50)
    Entry(frame_2, textvariable=input_soil_moisture,  background="white", fg="black", width=50).grid(row=4, column=0, pady=5, padx=50)
    Label(frame_2, text="Add luminosity", fg="red").grid(row=5, column=0, sticky="w", pady=5, padx=50)
    Entry(frame_2, textvariable=input_luminosity,  background="white", fg="black", width=50).grid(row=6, column=0, pady=5, padx=50)
    Label(frame_2, text="Add herb height", fg="red").grid(row=7, column=0, sticky="w" ,pady=5, padx=50)
    Entry(frame_2, textvariable=input_herb_height,  background="white", fg="black", width=50).grid(row=8, column=0, pady=5, padx=50)
    get_images()
    thumbnail_photo = Label(frame_2)
    thumbnail_photo.grid(row=9, column=0, sticky="e", padx=50, pady=5)
    Button(frame_2, text="Select herb image", command=add_herb_photo).grid(row=9, column=0, sticky="w",padx=50,  pady=5)
    Label(frame_2, text="Add air temperature", fg="red").grid(row=1, column=1, sticky="w", pady=5,padx=20)
    Entry(frame_2, textvariable=input_air_temperature,  background="white", fg="black", width=50).grid(row=2, column=1, pady=5, padx=20)
    Label(frame_2, text="Add ph value", fg="red").grid(row=3, column=1, sticky="w",  pady=5, padx=20)
    Entry(frame_2, textvariable=input_ph_value,  background="white", fg="black", width=50).grid(row=4, column=1, pady=5, padx=20)
    Label(frame_2, text="Add features", fg="red").grid(row=5, column=1, sticky="w",  pady=5, padx=20)
    Entry(frame_2, textvariable=input_features,  background="white", fg="black", width=50).grid(row=6, column=1, pady=5, padx=20)
    Label(frame_2, text="Add herb width", fg="red").grid(row=7, column=1, sticky="w", pady=5, padx=20)
    Entry(frame_2, textvariable=input_herb_width,  background="white", fg="black", width=50).grid(row=8, column=1, padx=20)
    store_button =Button(frame_2, text="STORE", command=store_addnew_herb, height=1, width=12)
    store_button.grid(row=11, column=1, sticky="w", pady=150, padx=40)
    cancel_button =Button(frame_2, text="CANCEL", command=cancel_addnew_herb, height=1, width=12)
    cancel_button.grid(row=11, column=1, sticky="e", pady=150, padx=20)
    return event


#za gumb update/ažuriranje podataka o postojećoj/dodanoj biljci
def store_update_herb():
    global var_herb_image, input_herb_photo
    def edit_herb():
        db.update_herb(conn, var_herb_name.get(), var_herb_moisture.get(), var_herb_luminosity.get(), var_herb_air_temp.get(), var_herb_ph.get(), var_herb_features.get(),
                   var_herb_height.get(), var_herb_width.get(), herb_image.get(), var_herb_id.get())
    var_herb_name.set(edit_herb_name.get())
    var_herb_moisture.set(edit_soil_moisture.get())
    var_herb_luminosity.set(edit_luminosity.get())
    var_herb_air_temp.set(edit_air_temperature.get())
    var_herb_ph.set(edit_ph_value.get())
    var_herb_features.set(edit_features.get())
    var_herb_height.set(edit_herb_height.get())
    var_herb_width.set(edit_herb_width.get())
    var_herb_image = input_herb_photo
    herb_image.set(var_herb_image)
    get_images()
    edit_herb()
    details_herb("<Button-1>", var_herb_id.get())


def cancel_update_herb():
    details_herb("<Button-1>", var_herb_id.get())

edit_herb_name = StringVar(value=" ")
edit_soil_moisture = StringVar(value=" ")
edit_luminosity = StringVar(value=" ")
edit_air_temperature = StringVar(value=" ")
edit_ph_value = StringVar(value=" ")
edit_features = StringVar(value=" ")
edit_herb_height = StringVar(value=" ")
edit_herb_width = StringVar(value=" ")

def update_herb(event):
    global tp, thumbnail_photo, var_herb_image, input_herb_photo
    tp.withdraw()
    tp = Toplevel()
    width=tp.winfo_screenwidth()
    height=tp.winfo_screenheight()
    tp.geometry("%dx%d" %(width, height))
    tp.title("")
    frame = LabelFrame(tp)
    frame.pack(side=TOP, fill=X, ipady=10)
    edit_herb_name.set(var_herb_name.get())
    edit_soil_moisture.set(var_herb_moisture.get())
    edit_air_temperature.set(var_herb_air_temp.get())
    edit_ph_value.set(var_herb_ph.get())
    edit_features.set(var_herb_features.get())
    edit_herb_height.set(var_herb_height.get())
    edit_herb_width.set(var_herb_width.get())
    edit_luminosity.set(var_herb_luminosity.get())
    input_herb_photo = var_herb_image

    l1=Label(frame, text="PyFlora Container", font=("Arial", 23), fg="green")
    l1.pack(side=LEFT, expand=True)
    l1.bind("<Button-1>", main_window)
    l2=Label(frame, text="Herbs", font=("Arial", 23), fg="green")
    l2.pack(side=LEFT, expand=True)
    l2.bind("<Button-1>", herbs_window)
    Button(frame, text="MY PROFILE",fg="green", command=my_profile,width=12, height=1).pack(side=LEFT, expand=True)
    Button(tp, text = "SYNC", fg = "green", width=12).pack(anchor=E, side=TOP, pady=20, padx=173)
    frame_2 = Label(tp)
    frame_2.pack(fill=BOTH, expand=True, padx=160)
    Label(frame_2, textvariable=edit_herb_name, fg="green", font=("Arial", 20)).grid(row=0, column=0, sticky="w",pady=50, padx=50)
    Label(frame_2, text="Change herb name", fg="red").grid(row=1, column=0, sticky="w",  pady=5, padx=50)
    Entry(frame_2, textvariable=edit_herb_name,  background="white", fg="black", width=50).grid(row=2, column=0, pady=5, padx=50)
    Label(frame_2, text="Change soil moisture", fg="red").grid(row=3, column=0, sticky="w", pady=5, padx=50)
    Entry(frame_2, textvariable=edit_soil_moisture,  background="white", fg="black", width=50).grid(row=4, column=0, pady=5, padx=50)
    Label(frame_2, text="Change luminosity", fg="red").grid(row=5, column=0, sticky="w",  pady=5, padx=50)
    Entry(frame_2, textvariable=edit_luminosity,  background="white", fg="black", width=50).grid(row=6, column=0, pady=5, padx=50)
    Label(frame_2, text="Change herb height", fg="red").grid(row=7, column=0, sticky="w",  pady=5, padx=50)
    thumbnail_photo = Label(frame_2)
    thumbnail_photo.grid(row=9, column=0, sticky="e", padx=50)
    get_images()
    Button(frame_2,text="Change herb image", fg="green", command=add_herb_photo).grid(row=9, column=0, sticky="w",padx=50, pady=5)
    Entry(frame_2, textvariable=edit_herb_height,  background="white", fg="black", width=50).grid(row=8, column=0, pady=5, padx=50)
    Label(frame_2, text="Change air temperature", fg="red").grid(row=1, column=1, sticky="w", padx=20)
    Entry(frame_2, textvariable=edit_air_temperature,  background="white", fg="black", width=50).grid(row=2, column=1, sticky="w", padx=20)
    Label(frame_2, text="Change ph value", fg="red").grid(row=3, column=1, sticky="w", padx=20)
    Entry(frame_2, textvariable=edit_ph_value,  background="white", fg="black", width=50).grid(row=4, column=1, padx=20, sticky="w")
    Label(frame_2, text="Change features", fg="red").grid(row=5, column=1, sticky="w", padx=20)
    Entry(frame_2, textvariable=edit_features,  background="white", fg="black", width=50).grid(row=6, column=1, padx=20, sticky="w")
    Label(frame_2, text="Change herb width", fg="red").grid(row=7, column=1, sticky="w", padx=20)
    Entry(frame_2, textvariable=edit_herb_width,  background="white", fg="black", width=50).grid(row=8, column=1, padx=20)
    store_button =Button(frame_2, text="STORE", command=store_update_herb, height=1, width=12)
    store_button.grid(row=11, column=1, sticky="w", pady=180, padx=25)
    cancel_button =Button(frame_2, text="CANCEL", command=cancel_update_herb, height=1, width=12)
    cancel_button.grid(row=11, column=1, sticky="e", pady=180, padx=20)
    return event

#window sa detaljima o konkretnom pycontaineru
def delete_button_pycontainer():
    answer = askyesno(title="confirmation", message="Are you sure that you want to proceed with delete action?")
    if answer:
        db.delete_container(conn, var_container_id.get()) 
        main_window("<Button-1>")
    else:
       return

def update_pycontainers():
    update_pycontainer("<Button-1>")


var_container_id = StringVar(value="")
var_container_name = StringVar(value="")
var_container_herb_id = StringVar(value="")
def sync_sensors():
    pass

def details_pyflora_container(event, container_id):
    global tp, var_herb_image
    tp.withdraw()
    global photo_filename
    global img_obj
    tp = Toplevel()
    width=tp.winfo_screenwidth()
    height=tp.winfo_screenheight()
    tp.geometry("%dx%d" %(width, height))
    tp.title("")
    frame = LabelFrame(tp)
    frame.pack(side=TOP, fill=X, ipady=10)
    l1=Label(frame, text="PyFlora Container", font=("Arial", 23), fg="green")
    l1.pack(side=LEFT, expand=True)
    l1.bind("<Button-1>", main_window)
    l2=Label(frame, text="Herbs", font=("Arial", 23), fg="green")
    l2.pack(side=LEFT, expand=True)
    l2.bind("<Button-1>", herbs_window)
    Button(frame, text="MY PROFILE",fg="green", command=my_profile,width=12, height=1).pack(side=LEFT, expand=True)
    containers_id, container_name, container_herb_id = db.get_container(conn, container_id)
    var_container_id.set(containers_id)
    var_container_name.set(container_name)
    var_container_herb_id.set(container_herb_id)
    sync_button = Button(tp, text = "SYNC", fg = "green", width=12, command=sync_sensors)
    sync_button.pack(anchor=E, side=TOP, pady=20, padx=173)
    if container_herb_id == None:
        sync_button.config(state="disable")
    else:
        sync_button.config(state="normal")
    frame_2 = Label(tp)
    frame_2.pack(fill=BOTH, expand=True, padx=100)
    if container_herb_id == None:
        var_herb_image = "./pyflora/GUI/images/herb_photo.jpg"
    else:
        herbs_id, herb_name, soil_moisture, luminosity, air_temperature, ph_value, features, herb_height, herb_width, image = db.get_herb(conn, container_herb_id) 
        var_herb_image = image
    Label(frame_2, textvariable=var_container_name, fg="green", font=("Arial", 20)).grid(row=0, column=0, sticky=W,pady=10, padx=136)
    Button(frame_2, text="UPDATE", fg="green",command=update_pycontainers, width=12).grid(row=0, column=1, sticky="w", ipady=2, pady=10, padx=470)
    Button(frame_2, text="DELETE", fg="red",width=12, command=delete_button_pycontainer).grid(row=0, column=1, sticky="w", ipady=2, pady=10, padx=307)
    canvas = Canvas(frame_2, width= 300, height= 300, bg="SpringGreen2")
    canvas.grid(row=2, column=1, sticky="w", rowspan=8, padx=307)
    img = Image.open(var_herb_image).resize((305,305))
    img_obj = ImageTk.PhotoImage(img)
    canvas.create_image((0,0),image=img_obj, anchor=NW)
    sensor_soil_moisture_stringvar = StringVar(value="")
    sensor_ph_value_stringvar = StringVar(value="")
    sensor_luminosity_stringvar = StringVar(value="")
    sensor_temperature_stringvar = StringVar(value="")
    sensor_soil_moisture_stringvar.set(str(db.get_humidity(conn)) + " %")
    sensor_ph_value_stringvar.set(str(db.get_ph_value(conn)) + " pH")
    sensor_luminosity_stringvar.set(str(db.get_luminosity(conn)) + " lm")
    sensor_temperature_stringvar.set(str(db.get_temperature(conn)) + " °C")

    Label(frame_2, text="Sensor value: soil moisture", fg="red").grid(row=2, column=0, sticky=W, padx=136)
    Label(frame_2, textvariable=sensor_soil_moisture_stringvar, fg="green").grid(row=3, column=0, sticky=W, padx=136)
    Label(frame_2, text="Sensor value: ph value and salinity of the soil", fg="red").grid(row=4, column=0, sticky=W, padx=136)
    Label(frame_2, textvariable=sensor_ph_value_stringvar, fg="green").grid(row=5, column=0, sticky=W, padx=136)
    Label(frame_2, text="Sensor value: luminosity", fg="red").grid(row=6, column=0, sticky=W, padx=136)
    Label(frame_2, textvariable=sensor_luminosity_stringvar, fg="green").grid(row=7, column=0, sticky=W, padx=136)
    Label(frame_2, text="Sensor value:air temperature", fg="red").grid(row=8, column=0, sticky=W, padx=136)
    Label(frame_2, textvariable=sensor_temperature_stringvar, fg="green").grid(row=9, column=0, sticky=W, padx=136)
    canvas_graph = Canvas(frame_2, width=1020, height=405, bg="gray")
    canvas_graph.grid(row=10, column=0, columnspan=2, sticky="w", padx=137)
    Button(frame_2, text="HISTO", width=7, height=2, fg="green", bd="3").place(x=1063,y=360)
    Button(frame_2, text="PIE", width=7, height=2, fg="green", bd="3").place(x=967, y=360)
    Button(frame_2, text="LINE", width=7, height=2, fg="green", bd="3").place(x=870, y=360)
    return event   
status_of_container = StringVar(value="")
#window sa listom pycontainera
def main_window(event):
    global tp, var_herb_image, container, status_of_container
    tp.withdraw()
    tp = Toplevel()
    #width=tp.winfo_screenwidth()
    #height=tp.winfo_screenheight()
    tp.attributes("-fullscreen", False) #geometry("%dx%d" %(width, height))
    tp.title("")
    global img_obj
    global photo_filename
    tp.option_add("*Entry.disabledBackground", "white")
    frame = LabelFrame(tp)
    frame.pack(side=TOP, fill=X, ipady=10)
    l1=Label(frame, text="PyFlora Container", font=("Arial", 23), fg="green")
    l1.pack(side=LEFT, expand=True)
    l2=Label(frame, text="Herbs", font=("Arial", 23), fg="green")
    l2.pack(side=LEFT, expand=True)
    l2.bind("<Button-1>", herbs_window)
    Button(frame, text="MY PROFILE",fg="green", command=my_profile,width=12, height=1).pack(side=LEFT, expand=True)
    Button(tp, text = "SYNC", fg = "green", width=12).pack(anchor=E, side=TOP, pady=20, padx=173)
    frame_2 = Label(tp)
    frame_2.pack(fill=BOTH, expand=True)
    my_canvas = Canvas(frame_2)
    my_canvas.pack(side="left", fill="both", expand=True, padx=450)
    my_scrollbar = Scrollbar(frame_2, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side="right", fill="y")
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion= my_canvas.bbox("all")))
    second_frame = Frame(my_canvas)
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")
    get_all_containers = db.get_all_containers(conn=conn)
    i = 0
    j = 0
    for index, container in enumerate(get_all_containers):
        if j < 1:
            j += 1
        else:
           j = 0
           i = index + 1
        if container["herb_id"] == None:
            var_herb_image = "./pyflora/GUI/images/herb_photo.jpg"
            status_of_container = "Empty PyContainer"
        else:
            herbs_id, herb_name, soil_moisture, luminosity, air_temperature, ph_value, features, herb_height, herb_width, image = db.get_herb(conn, container["herb_id"]) 
            var_herb_image = image
            status_of_container = "OK"
        canvas = Canvas(second_frame, width= 260, height= 125, bg="SpringGreen2")
        canvas.grid(row=i, column=j, sticky=NSEW)
        canvas.create_text(100, 20, text=container["name"], fill="black",anchor="w", font=('Helvetica 10 bold'))
        canvas.create_text(115, 80, text = "Status",fill="black",anchor=N,justify="left", font=('Helvetica 10 bold') )
        canvas.create_text(150, 90, text = status_of_container,fill="black",anchor=N,justify="left", font=('Helvetica 10 bold') )
        img = Image.open(var_herb_image).resize((90,130))
        images.append(ImageTk.PhotoImage(img))
        canvas.create_image(0,0, anchor=NW, image=images[-1])
        canvas.bind("<Button-1>", lambda event, container_id=container["id"]: details_pyflora_container(event, container_id))
    canvas = Canvas(second_frame, width=260, height=125, bg="SpringGreen2")
    canvas.grid(row=0, column=0)
    canvas.create_text(130, 40, text="+", fill="black", anchor=CENTER,font=("Helvetica 30 bold"))
    canvas.create_text(130, 85, text="Add new\nPycontainer", fill="black", anchor=CENTER,font=("Helvetica 15 bold"))
    canvas.bind("<Button-1>",addnew_pycontainer )
    #Button(second_frame, text="Empty   PyFlora   Containers", fg="green", width=55).grid(row=container["id"] +1, column=0, columnspan=2)
    return event


#window sa detaljima o konkretnoj biljci
def delete_button_herb():
    answer = askyesno(title="confirmation", message="Are you sure that you want to proceed with delete action?")
    if answer:
        db.delete_herb(conn, var_herb_id.get()) 
        herbs_window("<Button-1>")
    else:
       return
def update_herbs():
    update_herb("<Button-1>")

def details_herb(event, herb_id):
    global tp, bigimg_herb_photo, thumbnail_photo, var_herb_image
    tp.withdraw()
    tp = Toplevel()
    width=tp.winfo_screenwidth()
    height=tp.winfo_screenheight()
    tp.geometry("%dx%d" %(width, height))
    tp.title("")
    frame = LabelFrame(tp)
    frame.pack(side=TOP, fill=X, ipady=10)
    l1=Label(frame, text="PyFlora Container", font=("Arial", 23), fg="green")
    l1.pack(side=LEFT, expand=True)
    l1.bind("<Button-1>", main_window)
    l2=Label(frame, text="Herbs", font=("Arial", 23), fg="green")
    l2.pack(side=LEFT, expand=True)
    l2.bind("<Button-1>", herbs_window)
    Button(frame, text="MY PROFILE",fg="green", command=my_profile,width=12, height=1).pack(side=LEFT, expand=True)
    frame_2 = Label(tp)
    frame_2.pack(fill=BOTH, expand=True, pady=170, padx=43)
    herbs_id, herb_name, soil_moisture, luminosity, air_temperature, ph_value, features, herb_height, herb_width, image = db.get_herb(conn, herb_id) 
    var_herb_id.set(herbs_id)
    var_herb_name.set(herb_name)
    var_herb_moisture.set(soil_moisture)
    var_herb_air_temp.set(air_temperature)
    var_herb_ph.set(ph_value)
    var_herb_features.set(features)
    var_herb_height.set(herb_height)
    var_herb_width.set(herb_width)
    var_herb_luminosity.set(luminosity)
    var_herb_image = image
    Label(frame_2, textvariable=var_herb_name, fg="green", font=("Arial", 20)).grid(row=0, column=0, padx=200, sticky="w")
    Button(frame_2, text="UPDATE", fg="green",command=update_herbs, width=12, height=1).grid(row=0, column=1, ipady=2, sticky=W, pady=20, padx=580)
    Button(frame_2, text="DELETE", fg="red",width=12, command=delete_button_herb).grid(row=0, column=1, sticky=W, ipady=2, pady=20, padx=420)
    canvas = Canvas(frame_2, width= 300, height= 300, bg="SpringGreen2")
    canvas .grid(row=1, column=1,  rowspan=5, sticky=W, padx=420)
    big_img = Image.open(var_herb_image).resize((303, 303))
    bigimg_herb_photo = ImageTk.PhotoImage(big_img)
    canvas.create_image((0,0),image=bigimg_herb_photo, anchor=NW)
    Label(frame_2, text="Herb cultivation", fg="yellow").grid(row=1, column=0, sticky=W, padx=200)
    Label(frame_2, textvariable=var_herb_moisture, fg="green").grid(row=2, column=0, sticky=W, padx=200) 
    Label(frame_2, textvariable=var_herb_luminosity, fg="green").grid(row=3, column=0, sticky=W, padx=200)
    Label(frame_2, textvariable=var_herb_ph, fg="green").grid(row=4, column=0, sticky=W, padx=200)
    Label(frame_2, textvariable=var_herb_air_temp, fg="green").grid(row=5, column=0, sticky=W, padx=200)
    return event

#window sa listom dohvaćenih/postavljenih biljaka
def herbs_window(event):
    global tp, smallimg_herb_photo, images
    tp.withdraw()
    tp=Toplevel()
    width=tp.winfo_screenwidth()
    height=tp.winfo_screenheight()
    tp.geometry("%dx%d" %(width, height))
    tp.title("")
    frame=LabelFrame(tp)
    frame.pack(side=TOP, fill=X, ipady=10)
    l1=Label(frame, text="PyFlora Container", font=("Arial", 23), fg="green")
    l1.pack(side=LEFT, expand=True)
    l1.bind("<Button-1>", main_window)
    l2=Label(frame, text="Herbs", font=("Arial", 23), fg="green")
    l2.pack(side=LEFT, expand=True)
    Button(frame, text="MY PROFILE",fg="green", command=my_profile,width=12, height=1).pack(side=LEFT, expand=True)
    frame_2 = Frame(tp)
    frame_2.pack(fill=BOTH, expand=True, pady=70)
    my_canvas = Canvas(frame_2)
    my_canvas.pack(side="left", fill="both", expand=True, padx=450)
    my_scrollbar = Scrollbar(frame_2, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side="right", fill="y")
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion= my_canvas.bbox("all")))
    second_frame = Frame(my_canvas)
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")
    get_all_herbs = db.get_all_herbs(conn=conn)
    i = 0
    j = 0
    for index, herb in enumerate(get_all_herbs):
        if j < 1:
            j += 1
        else:
           j = 0
           i = index + 1
        canvas = Canvas(second_frame, width= 260, height= 125, bg="SpringGreen2")
        canvas.grid(row=i, column=j, sticky=NSEW)
        canvas.create_text(100, 20, text =herb["name"], fill="black",anchor="w", font=('Helvetica 20 bold')) # var_herb_name.get()
        canvas.create_text(140, 50, text = "Features",fill="black",anchor=N,justify="left", font=('Helvetica 10 bold') )
        canvas.create_text(140, 60, text = herb["features"],fill="black",anchor=N,justify="left", font=('Helvetica 10 bold') ) #var_herb_features.get()
        canvas.create_text(133, 70, text = "Height",fill="black",anchor=N,justify="left", font=('Helvetica 10 bold') )
        canvas.create_text(140, 80, text =herb["herb_height"],fill="black",anchor=N,justify="left" ,font=('Helvetica 10 bold') ) #var_herb_height.get()
        canvas.create_text(133, 90, text = "Width", fill="black", anchor=N, justify="left", font=('Helvetica 10 bold'))
        canvas.create_text(140, 100, text =herb["herb_width"],fill="black",anchor=N,justify="left" ,font=('Helvetica 10 bold') ) #var_herb_width.get()
        small_img = Image.open(herb["image"]).resize((100, 140)) 
        images.append(ImageTk.PhotoImage(small_img))
        canvas.create_image((0,0), anchor=NW, image=images[-1])
        canvas.bind("<Button-1>", lambda event, herb_id=herb["id"]: details_herb(event, herb_id))
    canvas = Canvas(second_frame, width=260, height=125, bg="SpringGreen2")
    canvas.grid(row=0, column=0, sticky=NSEW)  
    canvas.create_text(130, 45, text="+", fill="black", anchor=CENTER,font=("Helvetica 30 bold"))
    canvas.create_text(130, 85, text="Add new herb", fill="black", anchor=CENTER,font=("Helvetica 15 bold"))
    canvas.bind("<Button-1>", addnew_herb)
    return event

#za update podataka o useru/adminu
def update_data():
    db.update_user(conn, var_name.get(), var_lastname.get(), var_password.get(), var_username.get())
#window za ueđivanje podataka o useru/adminu
var_edit_name = StringVar()
var_edit_lastname = StringVar()
var_edit_username = StringVar()
var_edit_password = StringVar()
def edit_profile_screen():  
    global new_root
    new_root.withdraw()
    tp = Toplevel()
    width=tp.winfo_screenwidth()
    height=tp.winfo_screenheight()
    tp.geometry("%dx%d" %(width, height))
    tp.focus()
    def update_profile():
        var_name.set(var_edit_name.get())
        var_lastname.set(var_edit_lastname.get())
        var_password.set(var_edit_password.get()) 
        user = var_username.get()  

        new_name = var_edit_name.get()
        new_lastname = var_edit_lastname.get()
        new_password = var_edit_password.get()  
        def remove(string):
            return string.replace(" ", "") 
        if remove(new_name) == "" or remove(new_lastname)  == "" or remove(new_password) == "":
            messagebox.showerror("Error!", "Name, last name and password cannot be empty!")
            return      
        update_data()
        messagebox.showinfo(tp, message=f"User {user} succesfully changed data!")   
        tp.withdraw()  
        my_profile()
    
    first_name, last_name, username, password = db.get_user(conn, "admin")
    var_edit_name.set(first_name)
    var_edit_lastname.set(last_name)
    var_edit_username.set(username)
    var_edit_password.set(password)  
    
    Label(tp, text="Enter name").pack()
    ent_update_name = Entry(tp, textvariable=var_edit_name)
    ent_update_name.pack()
    ent_update_name.focus()
      
    Label(tp, text="Enter last name").pack() 
    ent_update_username = Entry(tp, textvariable=var_edit_lastname) 
    ent_update_username.pack()

    Label(tp, text="Username").pack()
    ent_update_password = Entry(tp, textvariable=var_edit_username, state="disabled", disabledforeground="black")
    ent_update_password.pack()

    Label(tp, text="Enter password").pack()
    ent_update_password = Entry(tp, textvariable=var_edit_password, show="*" )
    ent_update_password.pack()
    def cancel():
        tp.withdraw()
        my_profile()
    Button(tp, text="Save",width=6, command=update_profile).pack()
    Button(tp, text="Cancel",width=6, command=cancel).pack()
    tp.mainloop() 

#window sa podacima o profilu usera/admina

var_name = StringVar(value="Name")
var_lastname = StringVar(value="Last name")
var_username = StringVar(value="Username") 
var_password = StringVar(value="Password")
def my_profile():
    global tp
    tp.withdraw()
    global new_root
    new_root = Toplevel()
    width=new_root.winfo_screenwidth()
    height=new_root.winfo_screenheight()
    new_root.geometry("%dx%d" %(width, height))
    new_root.title("")
    tab = ttk.Notebook(new_root) 
    tab.grid(row=0, column=0, padx=500)
    frm_profile = Frame(tab) 
    frm_profile.grid(row=0, column=0) 
    tab.add(frm_profile, text="Profile")
 
    first_name, last_name, username, password = db.get_user(conn, "admin")
    var_name.set(first_name)
    var_lastname.set(last_name)
    var_username.set(username)   
    var_password.set(password)

    def close_profile():
      new_root.withdraw()
      main_window("<Button-1>")
    
    Label(frm_profile, 
          text="Name", 
          font=("Arial", 16)).grid(row=0, column=1, sticky="w")

    Label(frm_profile, 
          textvariable=var_name,
          font=("Arial", 18),fg="green").grid(row=1, column=1, sticky="w") 

    Label(frm_profile, 
          text="Last name", 
          font=("Arial", 16)).grid(row=2, column=1, sticky="w")

    Label(frm_profile, 
          textvariable=var_lastname,
          font=("Arial", 18), fg="green").grid(row=3, column=1, sticky="w") 


    Label(frm_profile, 
          text="Username", 
          font=("Arial", 16)).grid(row=4, column=1, sticky="w")


    Label(frm_profile, 
          textvariable=var_username,
          font=("Arial", 18), fg="green").grid(row=5, column=1, sticky="w")
    

    Button(frm_profile, 
          text="Edit profile",
          command=edit_profile_screen).grid(row=6, column=0, sticky="w")
    Button(frm_profile,
           text = "Close profile",
           command=close_profile).grid(row=6, column=3, sticky = "n")
    new_root.mainloop()
    
    

#funkcija za pokretanje applikacije
    
if __name__ == '__main__':
    login_window()


#omogućava da se GUI vidi
root.mainloop()