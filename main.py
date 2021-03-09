from bme280pi import Sensor
from sds011 import *
import time, aprs, db, configparser



if __name__=="__main__":
    config = configparser.ConfigParser()
    config.read('wxconf.ini')
    sensor = Sensor(0x77)
    db.make_table()
    
    while True:
        data = sensor.get_data()
        data['temperature'] = sensor.get_temperature(unit='F')
        data['now'] = time.strftime('%H%M%S', time.gmtime())
        data['call'] = 'NOCALL'
        pm25,pm10 = read_sds011(config)
        data['pm25'] = pm25
        data['pm10'] = pm10
        db.read_save(data)
        if config.getboolean('aprs', 'sendall'):
            print(aprs.send_data(data, config, sendall=True))
        else:
            print(aprs.send_data(data, config))
        show_air_values(config)
        time.sleep(300)