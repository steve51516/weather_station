from bme280pi import Sensor
from sds011 import read_sds011, show_air_values
import time, aprs, db, configparser

if __name__=="__main__":
    config = configparser.ConfigParser()
    config.read('wxconf.ini')
    sensor = Sensor(config['bme280']['device'])
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
        db.read_save(data)
        if config.getboolean('aprs', 'sendall'):
            print(aprs.send_data(data, config, sendall=True))
        else:
            print(aprs.send_data(data, config))
        show_air_values(config)
        time.sleep(10)