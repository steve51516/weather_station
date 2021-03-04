from os import read
import serial, time

with serial.Serial() as ser:
    ser.baudrate = 9600
    ser.port = '/dev/ttyUSB0'

def read_sds011():
    ser.open()    
    data = []
    for index in range(0, 10):
        datum = ser.read()
        data.append(datum)
    ser.close()
    pm25 = int.from_bytes(data[3], byteorder='little') * 256 + int.from_bytes(data[2], byteorder='little') / 10
    pm10 = int.from_bytes(data[5], byteorder='little') * 256 + int.from_bytes(data[4], byteorder='little') / 10

    return pm25,pm10

def show_air_values():
    pm25, pm10 = read_sds011()
    print("PM2.5, µg/m3: ", pm25)
    print("PM10, µg/m3: ", pm10)

if __name__=="__main__":
    while True:
        show_air_values()
        time.sleep(10)
