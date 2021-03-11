from bme280pi import Sensor
from sds011 import read_sds011, show_air_values
import time, aprs, db, configparser
from logger import log

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
            log(data['packet'])
        else:
            data['packet'] = aprs.send_data(data, config)
            data['sent'] = 0
            log(data['packet'])
        #show_air_values(config)
        db.read_save_enviro(data); db.read_save_packet(data)
        time.sleep(10)