from tkinter import *
from tkinter import Tk, Toplevel, Label, LabelFrame,Button, Entry
from app import main_window, my_profile, herbs_window, input_container_name
from app import herbs_window

root = Tk()

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
    store_button =Button(frame_2, text="STORE", command=store_update_container, height=1, width=12)
    store_button.grid(row=7, column=1, sticky="w", pady=180, padx=25)
    cancel_button =Button(frame_2, text="CANCEL", command=cancel_update_container, height=1, width=12)
    cancel_button.grid(row=7, column=1, sticky="e", pady=180, padx=20)
    return event

def update_container():
    update_pycontainer("<Button-1>")

def store_update_container():
    main_window("<Button-1>")

def cancel_update_container():
    main_window("<Button-1>")


def store_pycontainer(event):
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
    store_button =Button(frame_2, text="STORE", command=store_container, height=1, width=12)
    store_button.grid(row=7, column=1, sticky="w", pady=180, padx=25)
    cancel_button =Button(frame_2, text="CANCEL", command=cancel_store_container, height=1, width=12)
    cancel_button.grid(row=7, column=1, sticky="e", pady=180, padx=20)
    return event

def store_container():
    update_pycontainer("<Button-1>")

def store_container():
    main_window("<Button-1>")

def cancel_store_container():
    main_window("<Button-1>")