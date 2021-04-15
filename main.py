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
    data = {
        'callsign': config['aprs']['callsign'],
        'wspeed': 0,
        'wgusts': 0
    }
    for item in config['sensors']: # If an item in config is boolean false assign value of 0 to signify uncollected data
        if config['sensors'].getboolean(item) is False: 
            data[item] = 0 # Zeros will be converted to "000" in aprs module
    return data

def wait_delay(start_time):
        end_time = time() # Capture end time
        wait_time = round(300 - (end_time - start_time)) # Calculate time to wait before restart loop
        if wait_time < 0:
            abs(wait_time)
        elif wait_time == 0:
            wait_time = 300
        print(f"Generating next report in {round((wait_time / 60), 2)} minutes")
        stdout.flush(); sleep(wait_time) # Flush buffered output and wait exactly 5 minutes from start time

if __name__=="__main__":
    config = configparser.ConfigParser()
    print("reading config file...")
    config.read('wxstation.conf')
    if config['sensors'].getboolean('bme280'):
        sensor = start_bme280()
    data = enable_disable_sensors()
    if config['sensors'].getboolean('rain1h'):
        from rainfall import RainMonitor
        rmonitor = RainMonitor()
        print("Starting rainfall monitoring thread.")
        th_rain = th.Thread(target=rmonitor.rmonitor.monitor, daemon=True)
        th_rain.start()
    else:
        data['rainfall'] = 0
    if config['sensors'].getboolean('wspeed'):
        from wspeed import WindMonitor
        from statistics import mean
        wmonitor = WindMonitor()
        print("Starting wind speed monitoring thread.")
        stop_event = th.Event()
        th_wmonitor = th.Thread(target=wmonitor.monitor_wind, daemon=True)
        th_wspeed = th.Thread(target=wmonitor.calculate_speed, args=[stop_event], daemon=True)
        th_wspeed.start(); th_wmonitor.start()
    if config['serial'].getboolean('enabled'): # If SDS011 is enabled collect readings
        from sds011 import read_sds011, air_values
        th_sds011 = th.Thread(target=read_sds011, args=config) # Assign true readings
    else:
        data['pm25'], data['pm10'] = 0, 0 # Assign 0 value if disabled
    if config['sensors'].getboolean('wdir'):
        from wdir import WindDirectionMonitor
        wdir_monitor = WindDirectionMonitor()
        print("Starting wind direction monitoring thread.")
        th_wdir = th.Thread(target=wdir_monitor.monitor, daemon=True)
        th_wdir.start()
    print("Done reading config file.\nStarting main program now.")

    while True:
        start_time = time() # Capture loop start time
        if 'th_sds011' in locals():
            th_sds011.start()
        
        if 'th_rain' in locals():
            data['rainfall'] = rmonitor.total_rain() # Get total rainfall and reset tips counter
        
        if config['sensors'].getboolean('bme280'):
            data['temperature'] = sensor.get_temperature(unit='F')
            data['pressure'] = sensor.get_pressure()
            data['humidity'] = sensor.get_humidity()

        if 'th_wmonitor' and 'th_wspeed' in locals():
            if len(wmonitor.wind_list) > 0:
                stop_event.set()
                with wmonitor.wind_list_lock:
                    data['wspeed'], data['wgusts'] = mean(wmonitor.wind_list), max(wmonitor.wind_list)
                    wmonitor.wind_list.clear()
                    stop_event.clear()
            else:
                data['wgusts'] = 0
            #elif data['wspeed'] != 0 and data['wgusts'] != 0:
                #data['wspeed'], data['wgusts'] = 0, 0

        if 'th_sds011' in locals():
            th_sds011.join()
            data['pm25'], data['pm10'] = air_values['pm25'], air_values['pm10']

        if 'th_wdir' in locals():            
            data['wdir'] = wdir_monitor.average() # Record average wind direction in degrees and reset readings to average

        th_senddata, th_sensorsave = th.Thread(target=aprs.send_data(data, config)), th.Thread(target=db.read_save_sensors(data))
        th_sensorsave.start(); th_senddata.start()
        th_senddata.join(); th_sensorsave.join()
        wait_delay(start_time)