import os

from matplotlib import pyplot as plt

from gui.utils import db
from gui.utils.db import get_humidity, get_luminosity, get_temperature, get_ph_value, get_graph_temperature, \
    get_graph_humidity, get_graph_luminosity, get_graph_ph_value

script_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_directory, "data", "Pyflora.db")
conn = db.get_connection(db_path)


def get_container_status(soil_moisture, luminosity, air_temperature, ph_value):
    container_soil_moisture = get_humidity(conn=conn)
    container_luminosity = get_luminosity(conn=conn)
    container_air_temperature = get_temperature(conn=conn)
    container_ph_value = get_ph_value(conn=conn)

    if (
            container_soil_moisture == soil_moisture and
            container_luminosity == luminosity and
            container_air_temperature == air_temperature and
            container_ph_value == ph_value
    ):
        result_str = "Ok"
    else:
        result = []

        if container_soil_moisture < soil_moisture:
            result.append("Reduce water")
        else:
            result.append("Add water")

        if container_luminosity < luminosity:
            result.append("Decrease light exposure")
        else:
            result.append("Increase light exposure")

        if container_air_temperature < air_temperature:
            result.append("Decrease temperature")
        else:
            result.append("Increase temperature")

        if container_ph_value < ph_value:
            result.append("Decrease pH value")
        else:
            result.append("Increase pH value")

        result_str = "\n".join(result)

    return result_str


def create_line_chart():
    temp_y_values, temp_x_values = zip(*get_graph_temperature(conn))
    hum_y_values, hum_x_values = zip(*get_graph_humidity(conn))
    lum_y_values, lum_x_values = zip(*get_graph_luminosity(conn))
    ph_y_values, ph_x_values = zip(*get_graph_ph_value(conn))

    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    axs[0, 0].plot(temp_x_values, temp_y_values, label='Temperature', color='blue')
    axs[0, 0].set_xlabel('Time')
    axs[0, 0].set_ylabel('Temperature')
    axs[0, 0].legend()

    axs[0, 1].plot(hum_x_values, hum_y_values, label='Humidity', color='green')
    axs[0, 1].set_xlabel('Time')
    axs[0, 1].set_ylabel('Humidity')
    axs[0, 1].legend()

    axs[1, 0].plot(lum_x_values, lum_y_values, label='Luminosity', color='orange')
    axs[1, 0].set_xlabel('Time')
    axs[1, 0].set_ylabel('Luminosity')
    axs[1, 0].legend()

    axs[1, 1].plot(ph_x_values, ph_y_values, label='pH', color='red')
    axs[1, 1].set_xlabel('Time')
    axs[1, 1].set_ylabel('pH')
    axs[1, 1].legend()

    plt.tight_layout()

    return fig
