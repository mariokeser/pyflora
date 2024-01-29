import os
from tkinter import *
from tkinter import Tk, Label, Frame

from gui.utils import db


class SimulatorApp(Tk):
    def __init__(self, db_client):
        super().__init__()

        self.db_client = db_client

        self.title("Pyflora Simulator")
        self.geometry("500x300")

        self.var_temp = DoubleVar(self, 20)
        self.sld_temp = Slider(self,
                               "Temperature (°C)",
                               -30,
                               105,
                               0.5,
                               250,
                               self.var_temp)

        self.sld_temp.grid(column=0, row=0)
        self.sld_temp.after(1000, self.save_temperature)

        self.var_ph_value = DoubleVar(self, 7)
        self.sld_ph_value = Slider(self,
                                   "pH_value (pH)",
                                   1,
                                   14,
                                   0.5,
                                   length=250,
                                   variable=self.var_ph_value)
        self.sld_ph_value.grid(column=1, row=0)
        self.sld_ph_value.after(1000, self.save_ph_value)
        self.var_hum = IntVar(self, 50)
        self.sld_hum = Slider(self,
                              "Humidity (%)",
                              0,  # from_
                              100,  # to
                              length=250,
                              variable=self.var_hum)
        self.sld_hum.grid(column=2, row=0)
        self.sld_hum.after(1000, self.save_humidity)

        self.var_lum = IntVar(self, 7000)
        self.sld_lum = Slider(self,
                              "Luminosity (pH)",
                              from_=0,
                              to=10500,
                              resolution=500,
                              length=250,
                              variable=self.var_lum)
        self.sld_lum.grid(column=3, row=0)
        self.sld_lum.after(1000, self.save_luminosity)

    def save_temperature(self):
        db.save_temperature_reading(self.db_client, self.var_temp.get())
        self.sld_temp.after(1000, self.save_temperature)

    def save_ph_value(self):
        db.save_ph_value_reading(self.db_client, self.var_ph_value.get())
        self.sld_ph_value.after(1000, self.save_ph_value)

    def save_humidity(self):
        db.save_humidity_reading(self.db_client, self.var_hum.get())
        self.sld_hum.after(1000, self.save_humidity)

    def save_luminosity(self):
        db.save_luminosity_reading(self.db_client, self.var_lum.get())
        self.sld_lum.after(1000, self.save_luminosity)


class Slider(Frame):
    def __init__(self,
                 master,
                 title,
                 from_,
                 to,
                 resolution=1,
                 length=None,
                 variable=None,
                 orientation=VERTICAL):
        super().__init__(master)

        if orientation == VERTICAL:
            from_, to = to, from_

        Label(self, text=title).grid(column=0, row=0)

        self.scale = Scale(self,
                           from_=from_,
                           to=to,
                           resolution=resolution,
                           tickinterval=abs(to - from_),

                           length=length,
                           variable=variable,
                           orient=orientation)
        self.scale.grid(column=0, row=1)


if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_directory, "utils", "data", "Pyflora.db")
    db_client = db.get_connection(db_path)
    app = SimulatorApp(db_client)
    app.mainloop()
