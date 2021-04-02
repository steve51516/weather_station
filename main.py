from bme280pi import Sensor
from sds011 import read_sds011, show_air_values
from sys import stdout
import time, aprs, db, configparser

def init():
    config = configparser.ConfigParser()
    config.read('wxstation.conf')
    #sensor = Sensor(hex(config['bme280']['device']))
    sensor = Sensor(0x77)
    db.make_table()
    data = { 'callsign': config['aprs']['callsign'] }
    for item in config['sensors']: # If an item in config is boolean false assign value of "..."
        if config['sensors'].getboolean(item) is False: data[item] = "..."
    return (config,data,sensor)

if __name__=="__main__":
    (config,data,sensor) = init()
    while True:
        data += sensor.get_data()
        data['temperature'] = int(sensor.get_temperature(unit='F'))

        if config['serial'].getboolean('enabled') is True: # If SDS011 is enabled collect readings
            pm25,pm10 = read_sds011(config)
            data['pm25'], data['pm10'] = pm25, pm10
        else:
            data['pm25'], data['pm10'] = 0, 0

        if config.getboolean('aprs', 'sendall'):
            data['sent'], data['packet'] = 1, aprs.send_data(data, config, sendall=True)
        else:
            data['sent'], data['packet'] = 0, aprs.send_data(data, config)

        if config['sensors'].getboolean('quiet') is False:
            print(data['packet'])
            show_air_values(config)

        db.read_save_enviro(data); db.read_save_packet(data) # Write to database
        stdout.flush(); time.sleep(300) # Wait 5 minutes