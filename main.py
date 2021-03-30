from bme280pi import Sensor
from sds011 import read_sds011, show_air_values
from sys import stdout
import time, aprs, db, configparser

if __name__=="__main__":
    config = configparser.ConfigParser()
    config.read('wxconf.ini')
    #sensor = Sensor(hex(config['bme280']['device']))
    sensor = Sensor(0x77)
    db.make_table()
    data = {}
    data['callsign'] = config['aprs']['callsign']
    for item in config['sensors']:
        if config['sensors'].getboolean(item) is False: # If an item in config is boolean false assign value of "..."
            data[item] = "..."
    while True:
        tmp = sensor.get_data()
        #data['pressure'] = round(tmp['pressure'], 1)
        data['pressure'] = int(tmp['pressure']) # Temp fix to remove decimal point from pressure. Zero is appended in packet string to make 5 digits
                                                # TODO convert float to 5 digit number without rounding
        data['humidity'] = int(tmp['humidity'])
        data['temperature'] = int(sensor.get_temperature(unit='F'))
        data['ztime'] = time.strftime('%H%M%S', time.gmtime()) # Get zulu/UTC time
        if config['serial'].getboolean('enabled') is True: # If SDS011 is enabled collect readings
            pm25,pm10 = read_sds011(config)
            data['pm25'] = pm25
            data['pm10'] = pm10
        else:
            data['pm25'] = 0
            data['pm10'] = 0
        if config.getboolean('aprs', 'sendall'):
            data['packet'] = aprs.send_data(data, config, sendall=True)
            data['sent'] = 1
            print(f"Packet sent to {config['aprs']['server_pool']}")
        else:
            data['packet'] = aprs.send_data(data, config)
            data['sent'] = 0
        if config['sensors'].getboolean('quiet') is False:
            print(data['packet'])
            show_air_values(config)
        db.read_save_enviro(data); db.read_save_packet(data) # Write to database
        stdout.flush()
        time.sleep(300) # Wait 5 minutes