from os import read
import serial, time, configparser

global air_values

def read_sds011(config):
    global air_values
    air_values = {}
    with serial.Serial() as ser:
        ser.baudrate = config['serial']['baudrate']
        ser.port = config['serial']['tty']
    
    try:
        ser.open()    
        data = []
        for i in range(0, 10):
            data.append(ser.read())
    except ser.Error as error:
        print(f"Error connecting to serial port: {error}")
    finally:
        ser.close()

    air_values['pm25'] = int.from_bytes(data[3], byteorder='little') * 256 + int.from_bytes(data[2], byteorder='little') / 10
    air_values['pm10'] = int.from_bytes(data[5], byteorder='little') * 256 + int.from_bytes(data[4], byteorder='little') / 10

    return air_values

def show_air_values(config):
    global air_values
    read_sds011(config)
    print("PM2.5, µg/m3: ", air_values['pm25'])
    print("PM10, µg/m3: ", air_values['pm10'])

if __name__=="__main__":
    config = configparser.ConfigParser()
    config.read('wxconf.ini')
    while True:
        show_air_values(config)
        time.sleep(10)
