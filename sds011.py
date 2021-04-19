from os import read
from serial import Serial
from threading import Lock
from statistics import mean
from time import sleep, time

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
        self.baudrate = baudrate
        self.tty = tty
        self.air_values_lock = Lock()
        self.interval = interval

    def read_sds011(self):        
        with Serial() as ser:
            ser.baudrate = self.baudrate
            ser.port = self.tty
        
        try:
            self.air_values_lock.acquire()
            ser.open()    
            data = []
            for i in range(0, 10):
                data.append(ser.read())

            self.air_values['pm25'] = int.from_bytes(data[3], byteorder='little') * 256 + int.from_bytes(data[2], byteorder='little') / 10
            self.air_values['pm10'] = int.from_bytes(data[5], byteorder='little') * 256 + int.from_bytes(data[4], byteorder='little') / 10

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

        except ser.Error as error:
            print(f"Error connecting to serial port: {error}")
        finally:
            ser.close()
            self.air_values_lock.release()

        return self.air_values['pm25'], self.air_values['pm10']

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
                print("AirMonitorThread locked, retry average calculating in 2 seconds...")
                sleep(2)
    
    def monitor(self):
        self.runtime = time() + self.interval
        while self.runtime - time() > 0:
            self.read_sds011()
            sleep(1)