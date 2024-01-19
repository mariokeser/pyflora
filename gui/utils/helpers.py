import os

from matplotlib import pyplot as plt
from numpy.random import randint

from gui.utils import db
from gui.utils.db import get_humidity, get_luminosity, get_temperature, get_ph_value

script_directory = os.path.dirname(os.path.abspath("./data"))
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


def create_bar_chart():
    # Generate some sample data
    categories = ['Category 1', 'Category 2', 'Category 3', 'Category 4']
    values = [randint(1, 10) for _ in range(len(categories))]

    # Create a bar chart
    fig, ax = plt.subplots()
    ax.bar(categories, values)
    ax.set_ylabel('Values')
    ax.set_title('Bar Chart')
