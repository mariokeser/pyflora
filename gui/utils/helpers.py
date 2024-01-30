import os

from matplotlib import pyplot as plt

from gui.utils import db
from gui.utils.db import get_humidity, get_luminosity, get_temperature, get_ph_value, get_graph_temperature, \
    get_graph_humidity, get_graph_luminosity, get_graph_ph_value

script_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_directory, "data", "Pyflora.db")
conn = db.get_connection(db_path)


def get_container_status(soil_moisture, luminosity, air_temperature, ph_value):
    container_soil_moisture = get_humidity(conn=conn) or 0
    container_luminosity = get_luminosity(conn=conn) or 0
    container_air_temperature = get_temperature(conn=conn) or 0
    container_ph_value = get_ph_value(conn=conn) or 0

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
            result.append("Add water")
        else:
            result.append("Reduce water")

        if container_luminosity < luminosity:
            result.append("Increase light exposure")
        else:
            result.append("Decrease light exposure")

        if container_air_temperature < air_temperature:
            result.append("Increase temperature")
        else:
            result.append("Decrease temperature")

        if container_ph_value < ph_value:
            result.append("Increase pH value")
        else:
            result.append("Decrease pH value")

        result_str = "\n".join(result)

    return result_str


def create_line_chart():
    temp_y_values, temp_x_values = zip(*get_graph_temperature(conn))
    hum_y_values, hum_x_values = zip(*get_graph_humidity(conn))
    lum_y_values, lum_x_values = zip(*get_graph_luminosity(conn))
    ph_y_values, ph_x_values = zip(*get_graph_ph_value(conn))

    fig, axs = plt.subplots(2, 2, figsize=(10.2, 4))

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


def create_histogram():
    temp_y_values, _ = zip(*get_graph_temperature(conn))
    hum_y_values, _ = zip(*get_graph_humidity(conn))
    lum_y_values, _ = zip(*get_graph_luminosity(conn))
    ph_y_values, _ = zip(*get_graph_ph_value(conn))

    fig, axs = plt.subplots(2, 2, figsize=(10.2, 4))

    axs[0, 0].hist(temp_y_values, bins=20, color='blue', edgecolor='black')
    axs[0, 0].set_title('Temperature Histogram')
    axs[0, 0].set_xlabel('Temperature')
    axs[0, 0].set_ylabel('Frequency')

    axs[0, 1].hist(hum_y_values, bins=20, color='green', edgecolor='black')
    axs[0, 1].set_title('Humidity Histogram')
    axs[0, 1].set_xlabel('Humidity')
    axs[0, 1].set_ylabel('Frequency')

    axs[1, 0].hist(lum_y_values, bins=20, color='orange', edgecolor='black')
    axs[1, 0].set_title('Luminosity Histogram')
    axs[1, 0].set_xlabel('Luminosity')
    axs[1, 0].set_ylabel('Frequency')

    axs[1, 1].hist(ph_y_values, bins=20, color='red', edgecolor='black')
    axs[1, 1].set_title('pH Histogram')
    axs[1, 1].set_xlabel('pH')
    axs[1, 1].set_ylabel('Frequency')

    plt.tight_layout()

    return fig


def create_box_chart():
    temp_y_values, temp_x_values = zip(*get_graph_temperature(conn))
    hum_y_values, hum_x_values = zip(*get_graph_humidity(conn))
    lum_y_values, lum_x_values = zip(*get_graph_luminosity(conn))
    ph_y_values, ph_x_values = zip(*get_graph_ph_value(conn))

    fig, axs = plt.subplots(2, 2, figsize=(10.2, 4))

    axs[0, 0].boxplot(temp_y_values, labels=['Temperature'], patch_artist=True, boxprops=dict(facecolor='blue'))
    axs[0, 0].set_ylabel('Temperature')

    axs[0, 1].boxplot(hum_y_values, labels=['Humidity'], patch_artist=True, boxprops=dict(facecolor='green'))
    axs[0, 1].set_ylabel('Humidity')

    axs[1, 0].boxplot(lum_y_values, labels=['Luminosity'], patch_artist=True, boxprops=dict(facecolor='orange'))
    axs[1, 0].set_ylabel('Luminosity')

    axs[1, 1].boxplot(ph_y_values, labels=['pH'], patch_artist=True, boxprops=dict(facecolor='red'))
    axs[1, 1].set_ylabel('pH')

    plt.tight_layout()

    return fig