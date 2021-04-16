from os import read
from serial import Serial
from threading import Lock
from statistics import mean
from time import sleep

class MonitorAirQuality:
    def __init__(self, baudrate=9600, tty="/dev/ttyUSB0"):
        self.air_values = {
            'pm25': 0,
            'pm10': 0,
            'pm25_avg': 0,
            'pm10_avg': 0
        }
        self.pm25_total, self.pm10_total = [], []
        self.baudrate = baudrate
        self.tty = tty
        self.air_values_lock = Lock()

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
            self.pm25_total.append(self.air_values['pm25'])
            self.pm10_total.append(self.air_values['pm10'])

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
    
    def average(self):
        while True:
            if not self.air_values_lock.locked():
                if len(self.pm25_total) > 0 and len(self.pm10_total) > 0:
                    return mean(self.pm25_total), mean(self.pm10_total)
                else:
                    return 0, 0
            else:
                print("AirMonitorThread locked, retry average calculating in 2 seconds...")
                sleep(2)
    
    def monitor(self):
        while True:
            self.read_sds011()
            sleep(30)