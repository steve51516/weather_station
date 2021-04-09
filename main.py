from bme280pi import Sensor
from sys import stdout
import aprs, db, configparser, threading as th
from time import sleep, time

def start_bme280():
    try:
        sensor = Sensor(0x77)
    except Exception:
        sensor = Sensor(0x76)
    try:
        chipid, version = sensor._get_info_about_sensor()
        print(f"BME280 Information:\n\tChipID: {chipid}\n\tVersion: {version}")
    except Exception as e:
        print(f"{e}: Unable to get BME280 ChipID and Version")
    return sensor

def enable_disable_sensors():
    data = { 'callsign': config['aprs']['callsign'] }
    for item in config['sensors']: # If an item in config is boolean false assign value of 0 to signify uncollected data
        if config['sensors'].getboolean(item) is False: 
            data[item] = 0 # Zeros will be converted to "000" in aprs module
    return data

if __name__=="__main__":
    config = configparser.ConfigParser()
    print("reading config file...")
    config.read('wxstation.conf')
    if config['sensors'].getboolean('bme280'):
        sensor = start_bme280()
    data = enable_disable_sensors()
    if config['sensors'].getboolean('rain1h'):
        from rainfall import tips, monitor_rainfall, reset_rainfall
        print("Starting rainfall monitoring thread.")
        th_rain = th.Thread(target=monitor_rainfall, daemon=True)
        th_rain.start()
    else:
        data['rainfall'] = 0
    if config['sensors'].getboolean('wspeed'):
        from wspeed import monitor_wind, calculate_speed, wind_avg, wind_list
        print("Starting wind speed monitoring thread.")
        th_wmonitor = th.Thread(target=monitor_wind, daemon=True)
        th_wspeed = th.Thread(target=calculate_speed, daemon=True)
        th_wspeed.start(); th_wmonitor.start()
    if config['serial'].getboolean('enabled'): # If SDS011 is enabled collect readings
        from sds011 import read_sds011, show_air_values, air_values
        th_sds011 = th.Thread(target=read_sds011, args=config) # Assign true readings
    else:
        data['pm25'], data['pm10'] = 0, 0 # Assign 0 value if disabled
    print("Done reading config file.\nStarting main program now.")

    while True:
        start_time = time() # Capture loop start time
        if 'th_sds011' in locals():
            th_sds011.start()
        if 'th_rain' in locals():
            data['rainfall'] = tips; reset_rainfall() # 0 if disabled or actual value if enabled, reset after saving value
        if config['sensors'].getboolean('bme280'):
            data['temperature'] = sensor.get_temperature(unit='F')
            data['pressure'] = sensor.get_pressure()
            data['humidity'] = sensor.get_humidity()

        if 'th_wmonitor' and 'th_wspeed' in locals():
            data['wspeed'] = wind_avg(wind_list)
            if len(wind_list) > 0:
                data['wgusts'] = max(wind_list)
                wind_list.clear()
        if 'th_sds011' in locals():
            th_sds011.join()
            data['pm25'], data['pm10'] = air_values['pm25'], air_values['pm10']

        th_senddata, th_sensorsave = th.Thread(target=aprs.send_data(data, config)), th.Thread(target=db.read_save_sensors(data))
        th_sensorsave.start(); th_senddata.start()
        th_senddata.join(); th_sensorsave.join()
        end_time = time() # Capture end time
        wait_time = round(300 - (end_time - start_time)) # Calculate time to wait before restart loop
        print(f"Generating next report in {round((wait_time / 60), 2)} minutes")
        stdout.flush(); sleep(wait_time) # Flush buffered output and wait exactly 5 minutes from start time