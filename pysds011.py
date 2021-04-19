from threading import Lock
from statistics import mean
from time import sleep, time
from sds011 import SDS011

class MonitorAirQuality:
    def __init__(self, baudrate=9600, tty="/dev/ttyUSB0", interval=60):
        self.air_values = {
            'pm25': 0.0,
            'pm10': 0.0,
            'pm25_total': [],
            'pm10_total': [],
            'pm25_errors': 0,
            'pm10_errors': 0
        }
        self.air_values_lock = Lock()
        self.interval = interval
        self.sensor = SDS011(serial_port=tty, baudrate=baudrate)

    def read_sds011(self):
        while True:
            if not self.air_values_lock.locked():        
                self.air_values_lock.acquire()

                self.air_values['pm25'], self.air_values['pm10'] = self.sensor.query()

                if self.air_values['pm25'] < 999.9:
                    self.air_values['pm25_total'].append(self.air_values['pm25'])
                else:
                    self.air_values['pm10_errors'] += 1
                    print(f"Error: PM25 value {self.air_values['pm25']} is out of range")
                if self.air_values['pm10'] < 999.9:
                    self.air_values['pm10_total'].append(self.air_values['pm10'])
                else:
                    self.air_values['pm10_errors'] += 1
                    print(f"Error: PM10 value {self.air_values['pm10']} is out of range")
                self.air_values_lock.release()
                return self.air_values['pm25'], self.air_values['pm10']
            else:
                print("air_values is locked, retry average calculating in 2 seconds...")
                sleep(2)

    def show_air_values(self):
        #self.read_sds011()
        print("PM2.5, µg/m3: ", self.air_values['pm25'])
        print("PM10, µg/m3: ", self.air_values['pm10'])
    
    def average(self): # Return average from total readings
        while True:
            if not self.air_values_lock.locked():
                if len(self.air_values['pm25_total']) > 0 and len(self.air_values['pm10_total']) > 0:
                    if len(self.air_values['pm25_total']) > 5 and len(self.air_values['pm10_total']) > 5: # delete first 5 readings
                        self.air_values['pm25_total'] = self.air_values['pm25_total'][5:]
                        self.air_values['pm10_total'] = self.air_values['pm10_total'][5:]
                        return round(mean(self.air_values['pm25_total']), 2), round(mean(self.air_values['pm10_total']), 2)
                    else:
                        return round(mean(self.air_values['pm25_total']), 2), round(mean(self.air_values['pm10_total']), 2)
            else:
                print("air_values locked, retry average calculating in 2 seconds...")
                sleep(2)
    
    def monitor(self):
        self.sensor.sleep(sleep=False)
        self.runtime = time() + self.interval
        while self.runtime - time() > 0:
            self.read_sds011()
            sleep(1)
        self.sensor.sleep()