import aprslib, time
from bme280pi import Sensor
from math import trunc

def format_data(data, config):
        tmp = data # Create copy so that original data dictionary is not modified
        tmp['pressure'] = trunc(round(tmp['pressure'], 2) * 10.) # shift decimal point to the left 1 and round
        tmp['temperature'] = int(data['temperature'])
        tmp['humidity'] = int(tmp['humidity'])
        tmp['ztime'] = time.strftime('%d%H%M', time.gmtime()) # Get zulu/UTC time
        # Temperature must be 3 digits
        if tmp['temperature'] < 100 and tmp['temperature'] > 9: # Add 0 in front if temperature is between 0 and 99
            tmp['temperature'] = f"0{tmp['temperature']}"
        elif tmp['temperature'] > 9 and tmp['temperature'] >= 0: # add 00 in front if between 0 and 9
            tmp['temperature'] = f"00{tmp['temperature']}"
        elif tmp['temperature'] < 0 and tmp['temperature'] > -9:
            tmp['temperature'] = f"00{tmp['temperature']}"
        elif tmp['temperature'] < -9:
            tmp['temperature'] = f"0{tmp['temperature']}"
        # Humidity must be 2 digits. If humidity is 100% assign value of 00
        if tmp['humidity'] == 100:
            tmp['humidity'] = "00"

        packet = f"{config['aprs']['callsign']}>APRS,TCPIP*:@{tmp['ztime']}z{config['aprs']['longitude']}/{config['aprs']['latitude']}_{tmp['wdir']}/{tmp['avgwind']}g{tmp['peakwind']}t{tmp['temperature']}r{tmp['rain1h']}p{tmp['rain24h']}P{data['rain00m']}b{tmp['pressure']}h{tmp['humidity']}{config['aprs']['comment']}"
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
            sent = 1
    else:
        sent = 0
    return sent,packet