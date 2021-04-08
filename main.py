from bme280pi import Sensor
from sds011 import read_sds011, show_air_values
from sys import stdout
import time, aprs, db, configparser, threading as th
from time import sleep
from rainfall import tips, monitor_rainfall, reset_rainfall
from wspeed import monitor_wind, calculate_speed, wind_avg, wind_list

if __name__=="__main__":
    config = configparser.ConfigParser()
    print("reading config file...")
    config.read('wxstation.conf')
    try:
        sensor = Sensor(0x77)
    except Exception:
        sensor = Sensor(0x76)
    try:
        print(sensor._get_info_about_sensor())
    except Exception as e:
        print(e)
        print("Unable to display sensor device information")
    data = { 'callsign': config['aprs']['callsign'] }
    for item in config['sensors']: # If an item in config is boolean false assign value of "000" to signify uncollected data
        if config['sensors'].getboolean(item) is False: data[item] = "000"
    if config['sensors'].getboolean('rain1h') is True:
        print("Starting rainfall monitoring thread.")
        th_rain = th.Thread(target=monitor_rainfall, daemon=True)
        th_rain.start()
    if config['sensors'].getboolean('wspeed'):
        print("Starting wind speed monitoring thread.")
        th_wmonitor = th.Thread(target=monitor_wind, daemon=True)
        th_wspeed = th.Thread(target=calculate_speed, daemon=True)
        th_wspeed.start(); th_wmonitor.start()
    print("Done reading config file.\nStarting main program now.")

    while True:
        data['temperature'] = sensor.get_temperature(unit='F')
        data['pressure'] = sensor.get_pressure()
        data['humidity'] = sensor.get_humidity()
        data['rainfall'] = tips; reset_rainfall() # 0 if disabled or actual value if enabled, reset after saving value

        if config['serial'].getboolean('enabled') is True: # If SDS011 is enabled collect readings
            data['pm25'], data['pm10'] = read_sds011(config) # Assign true readings
        else:
            data['pm25'], data['pm10'] = 0, 0 # Assign 0 value if disabled
        if th_wmonitor and th_wspeed in globals():
            data['wspeed'] = wind_avg(wind_list)
            if len(wind_list) < 0:
                data['wgusts'] = max(wind_list)
                wind_list.clear()

        th_senddata, th_sensorsave = th.Thread(target=aprs.send_data(data, config)), th.Thread(target=db.read_save_sensors(data))
        th_sensorsave.start(); th_senddata.start()
        th_senddata.join(); th_sensorsave.join()

        stdout.flush(); time.sleep(300) # Flush buffered output and Wait 5 minutes