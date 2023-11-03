from tkinter import *
from tkinter import Tk, Toplevel, Label, LabelFrame,Button, Entry, Frame, messagebox, ttk, Canvas, filedialog
from tkinter.messagebox import askyesno
from PIL import Image, ImageTk 
from repo import db
#konekcija na bazu podataka
conn = db.get_connection("./pyflora/GUI/data/Pyflora.db")
#root GUI-a
root = Tk()

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
    root.attributes("-fullscreen", True)
    root.title("")
    frame = Frame(root)
    frame.grid(row=0, column=0)
    Label(frame,bg="green", text="Pyflora Container",font=("Arial", 20)).grid(row=0, column=0, padx=100, sticky=W)

    frm_login=LabelFrame(frame,fg="green", text="Log in", font=("Arial", 30,))
    frm_login.grid(row=1, column=0,padx=550,pady=200)
    
    Label(frm_login,bg="green", text="User name:").grid(row=2, column=0, padx=30, pady=30)
    ent_username = Entry(frm_login) 
    ent_username.grid(row=2, column=1) 
    ent_username.focus()

    Label(frm_login,bg="green", text="Password:").grid(row=3, column=0, padx=30, pady=30)
    ent_pass = Entry(frm_login, show="*")
    ent_pass.grid(row=3, column=1)

    button_login=Button(frm_login,fg="green",text="Sign in", command=login)
    button_login.grid(row=4, column=0, columnspan=2, pady=20)
    def update_date_profile(event):
        login()
    root.bind("<Return>", update_date_profile)
    #root.protocol('WM_DELETE_WINDOW')


# za pohranu/odustanak od dodavanja novih pycontainera i povrat na window sa listom pycontainera-main window
def store_addnew_pycontainer():
    db.add_containers(conn=conn, name=input_container_name.get())
    input_container_name.set("")
    main_window("<Button-1>")
def cancel_addnew_container():
    main_window("<Button-1>")
empty_pycontainer = StringVar(value=" ")
input_container_name = StringVar(value=" ")
#input_container_4 = StringVar(value=" ")
#input_container_5 = StringVar(value=" ")
def addnew_pycontainer(event):
    global tp
    tp.withdraw()
    tp = Toplevel()
    width=tp.winfo_screenwidth()
    height=tp.winfo_screenheight()
    tp.geometry("%dx%d" %(width, height))
    tp.title("")
    frame = LabelFrame(tp)
    frame.grid(row=0, column=0,ipady=10, sticky=W)
    l1=Label(frame, text="PyFlora Container", font=("Arial", 23), fg="green")
    l1.grid(row=0, column=0, sticky=W, padx=180)
    l1.bind("<Button-1>", main_window)
    l2=Label(frame, text="Herbs", font=("Arial", 23), fg="green")
    l2.grid(row=0, column=1, sticky=W, padx=133)
    l2.bind("<Button-1>", herbs_window)
    Button(frame, text="MY PROFILE",fg="green", command=my_profile,width=12, height=1).grid(row=0, column=2, sticky=E, padx=202, ipady=1)
    Button(tp, text = "SYNC", fg = "green", width=12).grid(row=1, column=0,pady=10,sticky=E,padx=205, ipady=3)
    frame_2 = Label(tp)
    frame_2.grid(row=2, column=0, pady=20)
    Label(frame_2, text="Pycontainer", fg="green", font=("Arial", 20)).grid(row=0, column=0, sticky="w",pady=50, padx=50)
    Label(frame_2, text="Pycontainer name", fg="red").grid(row=1, column=0, sticky="w",  pady=5, padx=50)
    Entry(frame_2, textvariable=input_container_name,  background="white", fg="black", width=50).grid(row=2, column=0, pady=5, padx=50)
    #Label(frame_2, text="Name of input field", fg="red").grid(row=1, column=1, sticky="w", padx=20)
    #Entry(frame_2, textvariable=input_container_4,  background="white", fg="black", width=50).grid(row=2, column=1, sticky="w", padx=20)
    #Label(frame_2, text="Pycontainer name", fg="red").grid(row=3, column=1, sticky="w", padx=20)
    #Entry(frame_2, textvariable=input_container_5,  background="white", fg="black", width=50).grid(row=4, column=1, padx=20, sticky="w")
    option_list = ["Herb 1", "Herb 2", "Herb 3", "Herb 4"]
    value_inside = StringVar(frame_2)
    value_inside.set("Select a herb")
    herb_menu = OptionMenu(frame_2, value_inside, *option_list)
    herb_menu.config(width=46)
    herb_menu.grid(row=2, column=1, sticky="w", padx=22)
    store_button =Button(frame_2, text="STORE", command=store_addnew_pycontainer, height=1, width=12)
    store_button.grid(row=7, column=1, sticky="w", pady=180, padx=25)
    cancel_button =Button(frame_2, text="CANCEL", command=cancel_addnew_container, height=1, width=12)
    cancel_button.grid(row=7, column=1, sticky="e", pady=180, padx=20)
    return event

# za gumb update/ažuriranje podataka o postojećim containerima

def store_update_pycontainer():
    details_pyflora_container("<Button-1>")
def cancel_update_pycontainer():
    details_pyflora_container("<Button-1>")

update_container_name = StringVar(value=" ")
#input_container_4 = StringVar(value=" ")
#input_container_5 = StringVar(value=" ")
def update_pycontainer(event):
    global tp
    tp.withdraw()
    tp = Toplevel()
    width=tp.winfo_screenwidth()
    height=tp.winfo_screenheight()
    tp.geometry("%dx%d" %(width, height))
    tp.title("")
    frame = LabelFrame(tp)
    frame.grid(row=0, column=0,ipady=10, sticky=W)
    l1=Label(frame, text="PyFlora Container", font=("Arial", 23), fg="green")
    l1.grid(row=0, column=0, sticky=W, padx=180)
    l1.bind("<Button-1>", main_window)
    l2=Label(frame, text="Herbs", font=("Arial", 23), fg="green")
    l2.grid(row=0, column=1, sticky=W, padx=133)
    l2.bind("<Button-1>", herbs_window)
    Button(frame, text="MY PROFILE",fg="green", command=my_profile,width=12, height=1).grid(row=0, column=2, sticky=E, padx=202, ipady=1)
    Button(tp, text = "SYNC", fg = "green", width=12).grid(row=1, column=0,pady=10,sticky=E,padx=205, ipady=3)
    frame_2 = Label(tp)
    frame_2.grid(row=2, column=0, pady=20)
    Label(frame_2, text="Pycontainer", fg="green", font=("Arial", 20)).grid(row=0, column=0, sticky="w",pady=50, padx=50)
    Label(frame_2, text="Change Pycontainer name", fg="red").grid(row=1, column=0, sticky="w",  pady=5, padx=50)
    Entry(frame_2, textvariable=update_container_name,  background="white", fg="black", width=50).grid(row=2, column=0, pady=5, padx=50)
    #Label(frame_2, text="Name of input field", fg="red").grid(row=1, column=1, sticky="w", padx=20)
    #Entry(frame_2, textvariable=input_container_4,  background="white", fg="black", width=50).grid(row=2, column=1, sticky="w", padx=20)
    #Label(frame_2, text="Pycontainer name", fg="red").grid(row=3, column=1, sticky="w", padx=20)
    #Entry(frame_2, textvariable=input_container_5,  background="white", fg="black", width=50).grid(row=4, column=1, padx=20, sticky="w")
    option_list = ["Herb 1", "Herb 2", "Herb 3", "Herb 4"]
    value_inside = StringVar(frame_2)
    value_inside.set("Select a herb")
    herb_menu = OptionMenu(frame_2, value_inside, *option_list)
    herb_menu.config(width=46)
    herb_menu.grid(row=2, column=1, sticky="w", padx=22)
    store_button =Button(frame_2, text="STORE", command=store_update_pycontainer, height=1, width=12)
    store_button.grid(row=7, column=1, sticky="w", pady=180, padx=25)
    cancel_button =Button(frame_2, text="CANCEL", command=cancel_update_pycontainer, height=1, width=12)
    cancel_button.grid(row=7, column=1, sticky="e", pady=180, padx=20)
    return event


# za dodavanje novih biljaka u window addnew herb
input_herb_name = StringVar(value=" ")
input_soil_moisture =StringVar(value=" ")
input_luminosity = StringVar(value=" ")
input_air_temperature = StringVar(value=" ")
input_ph_value = StringVar(value=" ")
input_features = StringVar(value=" ")
input_herb_height = StringVar(value=" ")
input_herb_width = StringVar(value=" ")
input_herb_photo = "./pyflora/GUI/images/herb_photo.jpg"
#varijable za get funkciju
herb_name = StringVar(value="")
soil_moisture = StringVar(value="")
luminosity = StringVar(value="")
air_temperature = StringVar(value="")
ph_value = StringVar(value="")
features = StringVar(value="")
herb_height = StringVar(value="")
herb_width = StringVar(value="")
herb_image=StringVar(value="")
#varijable za input iz get unkcije u entrye, labele i canvas
herb_name_get = StringVar(value="")
herb_moisture_get = StringVar(value="")
herb_air_temp_get = StringVar(value="")
herb_ph_get = StringVar(value="")
herb_features_get = StringVar(value="")
herb_height_get = StringVar(value="")
herb_width_get = StringVar(value="")
herb_luminosity_get = StringVar(value="")
herb_image_get = StringVar(value="")

# za select/get images
bigimg_herb_photo = None 
smallimg_herb_photo = None 
thumbnail_herb_photo = None

# za dohvaćanje image iz get funkcije
def get_images():
   global bigimg_herb_photo, smallimg_herb_photo, herb_image
   big_img = Image.open(herb_image).resize((303, 303))
   bigimg_herb_photo = ImageTk.PhotoImage(big_img)
   small_img = Image.open(herb_image).resize((100, 140)) 
   smallimg_herb_photo = ImageTk.PhotoImage(small_img)
#za postavljanje image u dodavanje nove biljke windowu, addnew herb
def set_thumbnail():
       global thumbnail_photo, thumbnail_herb_photo
       if input_herb_photo == "":
           return 
       else:
        img_thumb = Image.open(input_herb_photo).resize((303, 303))
       img_thumb.thumbnail((80, 200))
       thumbnail_herb_photo = ImageTk.PhotoImage(img_thumb)
       thumbnail_photo.config(image=thumbnail_herb_photo)

def add_herb_photo():
        global input_herb_photo
        input_herb_photo = filedialog.askopenfilename(title="Select herb image")
        set_thumbnail()


        
def store_addnew_herb(): 
    global herb_name, soil_moisture, luminosity, air_temperature, ph_value, features, herb_height, herb_width, herb_image
    db.add_herbs(conn=conn, name=input_herb_name.get(), soil_moisture=input_soil_moisture.get(), luminosity=input_luminosity.get(), air_temperature=input_air_temperature.get(),
             ph_value=input_ph_value.get(), features=input_features.get(), herb_hight=input_herb_height.get(), herb_width=input_herb_width.get(),image=input_herb_photo)
    input_herb_name.set("")
    input_soil_moisture.set("")
    input_luminosity.set("")
    input_air_temperature.set("")
    input_ph_value.set("")
    input_features.set("")
    input_herb_height.set("")
    input_herb_width.set("")
    herb_name, soil_moisture, luminosity, air_temperature, ph_value, features, herb_height, herb_width, herb_image = db.get_herb(conn) 
    herb_name_get.set(herb_name)
    herb_moisture_get.set(soil_moisture)
    herb_air_temp_get.set(air_temperature)
    herb_ph_get.set(ph_value)
    herb_features_get.set(features)
    herb_height_get.set(herb_height)
    herb_width_get.set(herb_width)
    herb_luminosity_get.set(luminosity)
    get_images()
    herbs_window("<Button-1>")

def cancel_addnew_herb():
    herbs_window("<Button-1>")

def addnew_herb(event):
    global tp, thumbnail_photo,input_herb_photo
    tp.withdraw()
    tp = Toplevel()
    width=tp.winfo_screenwidth()
    height=tp.winfo_screenheight()
    tp.geometry("%dx%d" %(width, height))
    tp.title("")
    frame = LabelFrame(tp)
    frame.grid(row=0, column=0,ipady=10, sticky=W)
    l1=Label(frame, text="PyFlora Container", font=("Arial", 23), fg="green")
    l1.grid(row=0, column=0, sticky=W, padx=180)
    l1.bind("<Button-1>", main_window)
    l2=Label(frame, text="Herbs", font=("Arial", 23), fg="green")
    l2.grid(row=0, column=1, sticky=W, padx=133)
    l2.bind("<Button-1>", herbs_window)
    Button(frame, text="MY PROFILE",fg="green", command=my_profile,width=12, height=1).grid(row=0, column=2, sticky=E, padx=202, ipady=1)
    Button(tp, text = "SYNC", fg = "green", width=12).grid(row=1, column=0,pady=10,sticky=E,padx=205, ipady=3)
    frame_2 = Label(tp)
    frame_2.grid(row=2, column=0, pady=20)
    Label(frame_2, text="Herb", fg="green", font=("Arial", 20)).grid(row=0, column=0, sticky="w",pady=50, padx=50)
    Label(frame_2, text="Add herb name", fg="red").grid(row=1, column=0, sticky="w",  pady=5, padx=50)
    Entry(frame_2, textvariable=input_herb_name,  background="white", fg="black", width=50).grid(row=2, column=0, pady=5, padx=50)
    Label(frame_2, text="Add soil moisture", fg="red").grid(row=3, column=0, sticky="w", pady=5, padx=50)
    Entry(frame_2, textvariable=input_soil_moisture,  background="white", fg="black", width=50).grid(row=4, column=0, pady=5, padx=50)
    Label(frame_2, text="Add luminosity", fg="red").grid(row=5, column=0, sticky="w",  pady=5, padx=50)
    Entry(frame_2, textvariable=input_luminosity,  background="white", fg="black", width=50).grid(row=6, column=0, pady=5, padx=50)
    Label(frame_2, text="Add herb height", fg="red").grid(row=7, column=0, sticky="w",  pady=5, padx=50)
    Entry(frame_2, textvariable=input_herb_height,  background="white", fg="black", width=50).grid(row=8, column=0, pady=5, padx=50)
    thumbnail_photo = Label(frame_2)
    thumbnail_photo.grid(row=9, column=0, sticky="e", padx=50)
    Button(frame_2, text="Select herb image", command=add_herb_photo).grid(row=9, column=0, sticky="w", padx=50)
    
    Label(frame_2, text="Add air temperature", fg="red").grid(row=1, column=1, sticky="w", padx=20)
    Entry(frame_2, textvariable=input_air_temperature,  background="white", fg="black", width=50).grid(row=2, column=1, sticky="w", padx=20)
    Label(frame_2, text="Add ph value", fg="red").grid(row=3, column=1, sticky="w", padx=20)
    Entry(frame_2, textvariable=input_ph_value,  background="white", fg="black", width=50).grid(row=4, column=1, padx=20, sticky="w")
    Label(frame_2, text="Add features", fg="red").grid(row=5, column=1, sticky="w", padx=20)
    Entry(frame_2, textvariable=input_features,  background="white", fg="black", width=50).grid(row=6, column=1, padx=20, sticky="w")
    Label(frame_2, text="Add herb width", fg="red").grid(row=7, column=1, sticky="w", padx=20)
    Entry(frame_2, textvariable=input_herb_width,  background="white", fg="black", width=50).grid(row=8, column=1, padx=20)
    store_button =Button(frame_2, text="STORE", command=store_addnew_herb, height=1, width=12)
    store_button.grid(row=11, column=1, sticky="w", pady=180, padx=25)
    cancel_button =Button(frame_2, text="CANCEL", command=cancel_addnew_herb, height=1, width=12)
    cancel_button.grid(row=11, column=1, sticky="e", pady=180, padx=20)
    return event

#za gumb update/ažuriranje podataka o postojećoj/dodanoj biljci
def store_update_herb():
    details_herb("<Button-1>")
def cancel_update_herb():
    details_herb("<Button-1>")

update_herb_name = StringVar(value=" ")
update_soil_moisture = StringVar(value=" ")
update_luminosity = StringVar(value=" ")
update_air_temperature = StringVar(value=" ")
update_ph_value = StringVar(value=" ")
update_features = StringVar(value=" ")
update_herb_height = StringVar(value=" ")
update_herb_width = StringVar(value=" ")
def update_herb(event):
    global tp
    tp.withdraw()
    tp = Toplevel()
    width=tp.winfo_screenwidth()
    height=tp.winfo_screenheight()
    tp.geometry("%dx%d" %(width, height))
    tp.title("")
    frame = LabelFrame(tp)
    frame.grid(row=0, column=0,ipady=10, sticky=W)
    l1=Label(frame, text="PyFlora Container", font=("Arial", 23), fg="green")
    l1.grid(row=0, column=0, sticky=W, padx=180)
    l1.bind("<Button-1>", main_window)
    l2=Label(frame, text="Herbs", font=("Arial", 23), fg="green")
    l2.grid(row=0, column=1, sticky=W, padx=133)
    l2.bind("<Button-1>", herbs_window)
    Button(frame, text="MY PROFILE",fg="green", command=my_profile,width=12, height=1).grid(row=0, column=2, sticky=E, padx=202, ipady=1)
    Button(tp, text = "SYNC", fg = "green", width=12).grid(row=1, column=0,pady=10,sticky=E,padx=205, ipady=3)
    frame_2 = Label(tp)
    frame_2.grid(row=2, column=0, pady=20)
    Label(frame_2, text="Herb", fg="green", font=("Arial", 20)).grid(row=0, column=0, sticky="w",pady=50, padx=50)
    Label(frame_2, text="Change herb name", fg="red").grid(row=1, column=0, sticky="w",  pady=5, padx=50)
    Entry(frame_2, textvariable=update_herb_name,  background="white", fg="black", width=50).grid(row=2, column=0, pady=5, padx=50)
    Label(frame_2, text="Change soil moisture", fg="red").grid(row=3, column=0, sticky="w", pady=5, padx=50)
    Entry(frame_2, textvariable=update_soil_moisture,  background="white", fg="black", width=50).grid(row=4, column=0, pady=5, padx=50)
    Label(frame_2, text="Change luminosity", fg="red").grid(row=5, column=0, sticky="w",  pady=5, padx=50)
    Entry(frame_2, textvariable=update_luminosity,  background="white", fg="black", width=50).grid(row=6, column=0, pady=5, padx=50)
    Label(frame_2, text="Change herb height", fg="red").grid(row=7, column=0, sticky="w",  pady=5, padx=50)
    Entry(frame_2, textvariable=update_herb_height,  background="white", fg="black", width=50).grid(row=8, column=0, pady=5, padx=50)
    Label(frame_2, text="Change herb image", fg="red").grid(row=9, column=0, sticky="w", padx=50, pady=5)
    option_list = ["Image 1", "Image 2", "Image 3", "Image 4"]
    value_inside = StringVar(frame_2)
    value_inside.set("Select a herb image")
    herb_menu = OptionMenu(frame_2, value_inside, *option_list)
    herb_menu.config(width=46)
    herb_menu.grid(row=10, column=0, sticky="w", padx=50)
    Label(frame_2, text="Change air temperature", fg="red").grid(row=1, column=1, sticky="w", padx=20)
    Entry(frame_2, textvariable=update_air_temperature,  background="white", fg="black", width=50).grid(row=2, column=1, sticky="w", padx=20)
    Label(frame_2, text="Change ph value", fg="red").grid(row=3, column=1, sticky="w", padx=20)
    Entry(frame_2, textvariable=update_ph_value,  background="white", fg="black", width=50).grid(row=4, column=1, padx=20, sticky="w")
    Label(frame_2, text="Change features", fg="red").grid(row=5, column=1, sticky="w", padx=20)
    Entry(frame_2, textvariable=update_features,  background="white", fg="black", width=50).grid(row=6, column=1, padx=20, sticky="w")
    Label(frame_2, text="Change herb width", fg="red").grid(row=7, column=1, sticky="w", padx=20)
    Entry(frame_2, textvariable=update_herb_width,  background="white", fg="black", width=50).grid(row=8, column=1, padx=20)
    store_button =Button(frame_2, text="STORE", command=store_update_herb, height=1, width=12)
    store_button.grid(row=11, column=1, sticky="w", pady=180, padx=25)
    cancel_button =Button(frame_2, text="CANCEL", command=cancel_update_herb, height=1, width=12)
    cancel_button.grid(row=11, column=1, sticky="e", pady=180, padx=20)
    return event

#window sa detaljima o konkretnom pycontaineru
def delete_pycontainer():
    pass
def delete_button_pycontainer():
    answer = askyesno(title="confirmation", message="Are you sure that you want to proceed with delete action?")
    if answer:
        delete_pycontainer()
    else:
        return
def update_pycontainers():
    update_pycontainer("<Button-1>")

def details_pyflora_container(event):
    global tp
    tp.withdraw()
    global photo_filename
    global img_obj
    tp = Toplevel()
    width=tp.winfo_screenwidth()
    height=tp.winfo_screenheight()
    tp.geometry("%dx%d" %(width, height))
    tp.title("")
    frame = LabelFrame(tp)
    frame.grid(row=0, column=0,ipady=10, sticky=W)
    l1=Label(frame, text="PyFlora Container", font=("Arial", 23), fg="green")
    l1.grid(row=0, column=0, sticky=W, padx=180)
    l1.bind("<Button-1>", main_window)
    l2=Label(frame, text="Herbs", font=("Arial", 23), fg="green")
    l2.grid(row=0, column=1, sticky=W, padx=133)
    l2.bind("<Button-1>", herbs_window)
    Button(frame, text="MY PROFILE",fg="green", command=my_profile,width=12, height=1).grid(row=0, column=2, sticky=E, padx=202, ipady=1)
    Button(tp, text = "SYNC", fg = "green", width=12).grid(row=1, column=0,pady=10,sticky=E,padx=204, ipady=3)
    
    frame_2 = Label(tp)
    frame_2.grid(row=2, column=0, pady=20)
    Label(frame_2, text="Pycontainer name", fg="green", font=("Arial", 20)).grid(row=0, column=0, sticky=W,pady=10)
    Button(frame_2, text="UPDATE", fg="green",command=update_pycontainers, width=12).grid(row=0, column=1, sticky=E, ipady=2, pady=10)
    Button(frame_2, text="DELETE", fg="red",width=12, command=delete_button_pycontainer).grid(row=0, column=1, sticky=E, ipady=2, pady=10, padx=165)
    canvas = Canvas(frame_2, width= 300, height= 300, bg="SpringGreen2")
    canvas.grid(row=2, column=1, sticky=E, rowspan=8)
    photo_filename = "./pyflora/GUI/images/Herb_photo.jpg"  
    img = Image.open(photo_filename).resize((305,305))
    img_obj = ImageTk.PhotoImage(img)
    canvas.create_image((0,0),image=img_obj, anchor=NW)
    Label(frame_2, text="Sensor value: soil moisture", fg="red").grid(row=2, column=0, sticky=W)
    Label(frame_2, text="Last activity", fg="green").grid(row=3, column=0, sticky=W)
    Label(frame_2, text="Sensor value: ph value and salinity of the soil", fg="red").grid(row=4, column=0, sticky=W)
    Label(frame_2, text="Last activity", fg="green").grid(row=5, column=0, sticky=W)
    Label(frame_2, text="Sensor value: luminosity", fg="red").grid(row=6, column=0, sticky=W)
    Label(frame_2, text="Last activity", fg="green").grid(row=7, column=0, sticky=W)
    Label(frame_2, text="Sensor value:air temperature", fg="red").grid(row=8, column=0, sticky=W)
    Label(frame_2, text="Last activity", fg="green").grid(row=9, column=0, sticky=W)
    canvas_graph = Canvas(frame_2, width=1020, height=405, bg="gray")
    canvas_graph.grid(row=10, column=0, columnspan=2, sticky=N)
    Button(frame_2, text="HISTO", width=7, height=2, fg="green", bd="3").place(x=926,y=360)
    Button(frame_2, text="PIE", width=7, height=2, fg="green", bd="3").place(x=826, y=360)
    Button(frame_2, text="LINE", width=7, height=2, fg="green", bd="3").place(x=726, y=360)
    return event   

#window sa listom pycontainera
def main_window(event):
    global tp
    tp.withdraw()
    tp = Toplevel()
    width=tp.winfo_screenwidth()
    height=tp.winfo_screenheight()
    tp.geometry("%dx%d" %(width, height))
    tp.title("")
    global img_obj
    global photo_filename
    tp.option_add("*Entry.disabledBackground", "white")
    frame = LabelFrame(tp)
    frame.grid(row=0, column=0,ipady=10, sticky=W)
    l1=Label(frame, text="PyFlora Container", font=("Arial", 23), fg="green")
    l1.grid(row=0, column=0, sticky=W, padx=180)
    l2=Label(frame, text="Herbs", font=("Arial", 23), fg="green")
    l2.grid(row=0, column=1, sticky=W, padx=133)
    l2.bind("<Button-1>", herbs_window)
    Button(frame, text="MY PROFILE",fg="green", command=my_profile,width=12, height=1).grid(row=0, column=2, sticky=E, padx=202, ipady=1)
    Button(tp, text = "SYNC", fg = "green", width=12).grid(row=1, column=0, sticky=E, padx=204,pady=20, ipady=3)
    frame_2 = Label(tp)
    frame_2.grid(row=2, column=0, pady=50)
    canvas = Canvas(frame_2, width= 260, height= 125, bg="SpringGreen2")
    canvas.grid(row=0, column=0, sticky=E)
    canvas.create_text(100, 20, text="Kitchen\n - shelf by the window", fill="black",anchor="w", font=('Helvetica 10 bold'))
    canvas.create_text(115, 80, text = "Status",fill="black",anchor=N,justify="left", font=('Helvetica 10 bold') )
    canvas.create_text(150, 90, text = "EMPTY pycontainer",fill="black",anchor=N,justify="left", font=('Helvetica 10 bold') )
    photo_filename = "./pyflora/GUI/images/herb_photo.jpg"
    img = Image.open(photo_filename).resize((90,130))
    img_obj = ImageTk.PhotoImage(img, master=root)
    canvas.create_image(0,0, anchor=NW, image=img_obj)
    canvas.bind("<Button-1>", details_pyflora_container)
   
    canvas = Canvas(frame_2, width=260, height=125, bg="SpringGreen2")
    canvas.grid(row=0, column=1, sticky=W)
    canvas.create_text(130, 40, text="+", fill="black", anchor=CENTER,font=("Helvetica 30 bold"))
    canvas.create_text(130, 85, text="Add new\nPycontainer", fill="black", anchor=CENTER,font=("Helvetica 15 bold"))
    canvas.bind("<Button-1>",addnew_pycontainer )
    Button(frame_2, text="Empty   PyFlora   Containers", fg="green", width=55).grid(row=1, column=0, columnspan=2)
    return event


#window sa detaljima o konkretnoj biljci
def delete_herb():
    pass
def delete_button_herb():
    answer = askyesno(title="confirmation", message="Are you sure that you want to proceed with delete action?")
    if answer:
        delete_herb()
    else:
        return
def update_herbs():
    update_herb("<Button-1>")
def details_herb(event):
    global tp, herb_name_get, bigimg_herb_photo, herb_moisture_get, herb_air_temp_get, herb_luminosity_get, herb_ph_get
    tp.withdraw()
    tp = Toplevel()
    width=tp.winfo_screenwidth()
    height=tp.winfo_screenheight()
    tp.geometry("%dx%d" %(width, height))
    tp.title("")
    frame = LabelFrame(tp)
    frame.grid(row=0, column=0,ipady=10, sticky=W)
    l1=Label(frame, text="PyFlora Container", font=("Arial", 23), fg="green")
    l1.grid(row=0, column=0, sticky=W, padx=180)
    l1.bind("<Button-1>", main_window)
    l2=Label(frame, text="Herbs", font=("Arial", 23), fg="green")
    l2.grid(row=0, column=1, sticky=W, padx=133)
    l2.bind("<Button-1>", herbs_window)
    Button(frame, text="MY PROFILE",fg="green", command=my_profile,width=12, height=1).grid(row=0, column=2, sticky=E, padx=202, ipady=1)
    Button(tp, text = "SYNC", fg = "green", width=12).grid(row=1, column=0,pady=20, ipady=3, sticky=W, padx=1090)
    frame_2 = Label(tp)
    frame_2.grid(row=2, column=0, sticky=W)
    
    Label(frame_2, textvariable=herb_name_get, fg="green", font=("Arial", 20)).grid(row=0, column=0, padx=200)
    Button(frame_2, text="UPDATE", fg="green",command=update_herbs, width=12, height=1).grid(row=0, column=1, ipady=2, sticky=W, pady=20, padx=580)
    Button(frame_2, text="DELETE", fg="red",width=12, command=delete_button_herb).grid(row=0, column=1, sticky=W, ipady=2, pady=20, padx=420)
    canvas = Canvas(frame_2, width= 300, height= 300, bg="SpringGreen2")
    canvas .grid(row=1, column=1,  rowspan=5, sticky=W, padx=420)
    canvas.create_image((0,0),image=bigimg_herb_photo, anchor=NW)
    Label(frame_2, text="Herb cultivation", fg="yellow").grid(row=1, column=0, sticky=W, padx=200)
    Label(frame_2, textvariable=herb_moisture_get, fg="green").grid(row=2, column=0, sticky=W, padx=200)
    Label(frame_2, textvariable=herb_luminosity_get, fg="green").grid(row=3, column=0, sticky=W, padx=200)
    Label(frame_2, textvariable=herb_ph_get, fg="green").grid(row=4, column=0, sticky=W, padx=200)
    Label(frame_2, textvariable=herb_air_temp_get, fg="green").grid(row=5, column=0, sticky=W, padx=200)
    return event

#window sa listom dohvaćenih/postavljenih biljaka
def herbs_window(event):
    global tp, smallimg_herb_photo, herb_name_get, herb_features_get, herb_height_get, herb_width_get
    tp.withdraw()
    tp=Toplevel()
    width=tp.winfo_screenwidth()
    height=tp.winfo_screenheight()
    tp.geometry("%dx%d" %(width, height))
    tp.title("")
    frame=LabelFrame(tp)
    frame.grid(row=0, column=0, ipady=10, sticky=W)
    l1=Label(frame, text="PyFlora Container", font=("Arial", 23), fg="green")
    l1.grid(row=0, column=0,  sticky=W, padx=180)
    l1.bind("<Button-1>", main_window)
    l2=Label(frame, text="Herbs", font=("Arial", 23), fg="green")
    l2.grid(row=0, column=1, sticky=W, padx=133)
    Button(frame, text="MY PROFILE",fg="green", command=my_profile,width=12, height=1).grid(row=0, column=2, sticky=E, padx=202, ipady=1)
    
    Button(tp, text = "SYNC", fg = "green", width=12).grid(row=1, column=0, sticky=E, padx=204,pady=20, ipady=3)
    frame_2 = Label(tp)
    frame_2.grid(row=2, column=0, pady=50)
    canvas = Canvas(frame_2, width= 260, height= 125, bg="SpringGreen2")
    canvas.grid(row=0, column=0, sticky=E)
    canvas.create_text(100, 20, text=herb_name_get.get(), fill="black",anchor="w", font=('Helvetica 20 bold'))
    canvas.create_text(140, 50, text = "Features",fill="black",anchor=N,justify="left", font=('Helvetica 10 bold') )
    canvas.create_text(140, 60, text = herb_features_get.get(),fill="black",anchor=N,justify="left", font=('Helvetica 10 bold') )
    canvas.create_text(133, 70, text = "Height",fill="black",anchor=N,justify="left", font=('Helvetica 10 bold') )
    canvas.create_text(140, 80, text = herb_height_get.get(),fill="black",anchor=N,justify="left" ,font=('Helvetica 10 bold') )
    canvas.create_text(133, 90, text="Width", fill="black", anchor=N, justify="left", font=('Helvetica 10 bold'))
    canvas.create_text(140, 100, text = herb_width_get.get(),fill="black",anchor=N,justify="left" ,font=('Helvetica 10 bold') )

  
    canvas.create_image((0,0), anchor=NW, image=smallimg_herb_photo)
    canvas.bind("<Button-1>", details_herb)
    canvas = Canvas(frame_2, width=260, height=125, bg="SpringGreen2")
    canvas.grid(row=0, column=1, sticky=W)
    canvas.create_text(130, 45, text="+", fill="black", anchor=CENTER,font=("Helvetica 30 bold"))
    canvas.create_text(130, 85, text="Add new herb", fill="black", anchor=CENTER,font=("Helvetica 15 bold"))
    canvas.bind("<Button-1>", addnew_herb)
    return event

#za update podataka o useru/adminu
def update_data():
    db.update(conn, var_name.get(), var_lastname.get(), var_password.get(), var_username.get())
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