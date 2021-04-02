import aprslib
from bme280pi import Sensor

def send_data(data, config, sendall=False):

    if data['temperature'] < 100 and data['temperature'] > 9: # Add 0 in front if temperature is between 0 and 99
        data['temperature'] = f"0{data['temperature']}"
    elif data['temperature'] > 9 and data['temperature'] >= 0: # add 00 in front if between 0 and 9
        data['temperature'] = f"00{data['temperature']}"
    elif data['temperature'] < 0 and data['temperature'] > -9:
        data['temperature'] = f"00{data['temperature']}"
    elif data['temperature'] < -9:
        data['temperature'] = f"0{data['temperature']}"

    data['pressure'] = round(data['pressure'], 1) # The letter "b" followed by 5 numbers represents the barometric pressure in tenths of a millibar.
    if data['humidity'] == 100:
        data['humidity'] = "00"
    
    packet = f"{config['aprs']['callsign']}>APRS,TCPIP*:@{data['ztime']}z{config['aprs']['longitude']}/{config['aprs']['latitude']}_{data['wdir']}/{data['avgwind']}g{data['peakwind']}t{data['temperature']}r{data['rain1h']}p{data['rain24h']}P{data['rain00m']}b{data['pressure']}h{data['humidity']}{config['aprs']['comment']}"

    if sendall:
        for server in config['servers']:
            AIS = aprslib.IS(config['aprs']['callsign'], config['aprs']['passwd'], config['servers'][server], config['aprs']['port'])
            AIS.connect()
            AIS.sendall(packet)
            AIS.close()

    return packet