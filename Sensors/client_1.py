import repo_1 
import time


db_client = repo_1.DbClient("./pyflora/Sensors/data/readings_1.db") 


while True: 
    print(f"Temperature: {db_client.get_temperature()}°C") 
    print(f"Pressure: {db_client.get_ph_value()} pH") 
    print(f"Humidity: {db_client.get_humidity()}%")
    print(f"Luminosity: {db_client.get_luminosity()} lm")
    time.sleep(0.9)  
    
