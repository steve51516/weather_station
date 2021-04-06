from bme280pi import Sensor
from sds011 import read_sds011, show_air_values
from sys import stdout
import time, aprs, db, configparser, threading as th
from time import sleep
from rainfall import *

if __name__=="__main__":
    config = configparser.ConfigParser()
    config.read('wxstation.conf')
    #sensor = Sensor(hex(config['bme280']['device']))
    sensor = Sensor(0x77)
    db.create_db()
    data = { 'callsign': config['aprs']['callsign'] }
    for item in config['sensors']: # If an item in config is boolean false assign value of "..."
        if config['sensors'].getboolean(item) is False: data[item] = "..."
    th_rain = th.Thread(target=monitor_rainfall, daemon=True)
    th_rain.start()
        
    while True:
        tmp = sensor.get_data()
        data['temperature'] = sensor.get_temperature(unit='F')
        data['pressure'] = tmp['pressure']
        data['humidity'] = tmp['humidity']
        tmp.clear()

        if config['serial'].getboolean('enabled') is True: # If SDS011 is enabled collect readings
            pm25,pm10 = read_sds011(config) # Get readings from sds011
            data['pm25'], data['pm10'] = pm25, pm10 # Assign true readings
        else:
            data['pm25'], data['pm10'] = 0, 0 # Assign 0 value if disabled
        if config['sensors'].getboolean('rain1h') is True:
            data['rainfall'] = tips
            reset_rainfall() # reset tips variable

        db.read_save_sensors(data) # Write to weather table before values get rounded
        data['sent'], data['packet'] = aprs.send_data(data, config)

        db.read_save_packet(data) # Write to packet table
        #print(data['packet'])
        stdout.flush(); time.sleep(300) # Flush buffered output and Wait 5 minutes