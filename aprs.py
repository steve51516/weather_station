import aprslib, time
from bme280pi import Sensor
from math import trunc
from db import rain_avg, read_save_packet

# Convert temperature, wind speed, and wind gusts to 3 digits
def add_zeros(num):
        if num < 100 and num > 9: # Add 0 in front if temperature is between 0 and 99
            return f"0{num}"
        elif num > 9 and num >= 0: # add 00 in front if between 0 and 9
            return f"00{num}"
        elif num < 0 and num > -9:
            return f"00{num}"
        elif num < -9:
            return f"0{num}"
        else:
            return num

# Humidity must be 2 digits. If humidity is 100% assign value of 00
def format_humidity(num):
    if num == 100:
        return "00"
    else:
        return num

def format_data(data, config):
        tmp = data.copy() # Create copy so that original data dictionary is not modified
        tmp['pressure'] = trunc(round(tmp['pressure'], 2) * 10.) # shift decimal point to the left 1 and round
        tmp['temperature'] = add_zeros(int(tmp['temperature']))
        tmp['wspeed'] = add_zeros(int(tmp['wspeed']))
        tmp['wgusts'] = add_zeros(int(tmp['wgusts']))
        tmp['humidity'] = format_humidity(int(tmp['humidity']))
        tmp['ztime'] = time.strftime('%d%H%M', time.gmtime()) # Get zulu/UTC time
        tmp['rain1h'], tmp['rain24h'], tmp['rain00m'] = rain_avg(1), rain_avg(24), rain_avg(00) # Get rain averages

        packet = f"{config['aprs']['callsign']}>APRS,TCPIP*:@{tmp['ztime']}z{config['aprs']['longitude']}/{config['aprs']['latitude']}_{tmp['wdir']}/{tmp['wspeed']}g{tmp['wgusts']}t{tmp['temperature']}r{tmp['rain1h']}p{tmp['rain24h']}P{data['rain00m']}b{tmp['pressure']}h{tmp['humidity']}{config['aprs']['comment']}"
        tmp.clear()
        return packet
        
def send_data(data, config):
    packet = format_data(data, config)
    if config.getboolean('aprs', 'sendall'):
        for server in config['servers']:
            for i in range(1, 4): # Retry 3 times increasing delay by 10 seconds each time
                delay = i * 10
                AIS = aprslib.IS(config['aprs']['callsign'], config['aprs']['passwd'], config['servers'][server], config['aprs']['port'])
                try:
                    AIS.connect()
                    AIS.sendall(packet)
                except Exception as error:
                    print(error)
                    print(f"Retry number: {i}\n Trying again in {delay} seconds...")
                    time.sleep(delay)
                    continue
                finally:
                    AIS.close()
            print(f"Packet sent to {config['servers'][server]}")
            transmitted = 1
    else:
        transmitted = 0
    read_save_packet(packet, transmitted)