from bme280pi import Sensor
from sds011 import read_sds011, show_air_values
from sys import stdout
import time, aprs, db, configparser, threading as th
from time import sleep
from rainfall import tips, monitor_rainfall, reset_rainfall

if __name__=="__main__":
    config = configparser.ConfigParser()
    print("reading config file...")
    config.read('wxstation.conf')
    #sensor = Sensor(hex(config['bme280']['device']))
    sensor = Sensor(0x77)
    data = { 'callsign': config['aprs']['callsign'] }
    for item in config['sensors']: # If an item in config is boolean false assign value of "000" to signify uncollected data
        if config['sensors'].getboolean(item) is False: data[item] = "000"
    if config['sensors'].getboolean('rain1h') is True:
        th_rain = th.Thread(target=monitor_rainfall, daemon=True)
        th_rain.start()
    print("Done reading config file.\nStarting main program now.")

    while True:
        tmp = sensor.get_data()
        data['temperature'] = sensor.get_temperature(unit='F')
        data['pressure'] = tmp['pressure']
        data['humidity'] = tmp['humidity']
        tmp.clear()
        data['rainfall'] = tips # 0 if disabled or actual value if enabled

        if config['serial'].getboolean('enabled') is True: # If SDS011 is enabled collect readings
            data['pm25'], data['pm10'] = read_sds011(config) # Assign true readings
        else:
            data['pm25'], data['pm10'] = 0, 0 # Assign 0 value if disabled

        th_senddata, th_sensorsave = th.Thread(target=aprs.send_data(data, config)), th.Thread(target=db.read_save_sensors(data))
        th_sensorsave.start(); th_senddata.start()
        th_senddata.join(); th_sensorsave.join()
        reset_rainfall() # reset tips variable
        stdout.flush(); time.sleep(300) # Flush buffered output and Wait 5 minutes