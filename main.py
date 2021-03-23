from bme280pi import Sensor
from sds011 import read_sds011, show_air_values
from sys import stdout
import time, aprs, db, configparser, mdb

if __name__=="__main__":
    config = configparser.ConfigParser()
    config.read('wxconf.ini')
    #sensor = Sensor(hex(config['bme280']['device']))
    sensor = Sensor(0x77)
    db.make_table()
    data = {}
    data['callsign'] = config['aprs']['callsign']
    for item in config['sensors']:
        if config['sensors'].getboolean(item) is False:
            data[item] = "..."
    while True:
        tmp = sensor.get_data()
        data['pressure'] = round(tmp['pressure'], 1)
        data['humidity'] = int(tmp['humidity'])
        data['temperature'] = int(sensor.get_temperature(unit='F'))
        data['ztime'] = time.strftime('%H%M%S', time.gmtime())
        pm25,pm10 = read_sds011(config)
        data['pm25'] = pm25
        data['pm10'] = pm10
        if config.getboolean('aprs', 'sendall'):
            data['packet'] = aprs.send_data(data, config, sendall=True)
            data['sent'] = 1
            print(f"Packet sent to {config['aprs']['server_pool']}")
        else:
            data['packet'] = aprs.send_data(data, config)
            data['sent'] = 0
        print(data['packet'])
        #show_air_values(config)
        if bool(config['database']['sqlite']) == True:
            db.read_save_enviro(data); db.read_save_packet(data)
        if bool(config['database']['sqlite']) == True:
            mariadb.read_save_sensors(data); mariadb.read_save_packet(data)
        stdout.flush()
        time.sleep(10)