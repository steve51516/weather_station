import aprslib
from bme280pi import Sensor

# The first four fields (wind direction, wind speed, temperature and gust) are required,
# in that order, and if a particular measurement is not present, 
# the three numbers should be replaced by "..." to indicate no data available.
def send_data(data, config, sendall=False):
    # data['longitude'] = ""
    # data['latitude'] = ""
    # data['wdir'] = "..." # 3 numbers represents wind direction in degrees from true north. This is the direction that the wind is blowing from.
    # data['avgwind'] = "..." # 3 numbers represents Average wind speed in MPH
    # data['peakwind'] = "..." # 3 numbers represents Peak wind speed
    # data['temperature'] =  # The letter "t" followed by 3 characters (numbers and minus sign) represents the temperature in degrees F.
    # data['rain1h'] = "..." # The letter "r" followed by 3 numbers represents the amount of rain in hundredths of inches that fell the past hour.
    # data['rain24h'] = "..." # The letter "p" followed by 3 numbers represents the amount of rain in hundredths of inches that fell in the past 24 hours.

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

    #   data['humidity'] = int(data['humidity']) 
    packet = f"{config['aprs']['callsign']}>APRS,TCPIP*:@{data['now']}z{config['aprs']['longitude']}/{config['aprs']['latitude']}_{data['wdir']}/{data['avgwind']}g{data['peakwind']}t{data['temperature']}r{data['rain1h']}p{data['rain24h']}b{data['pressure']}h{data['humidity']}"
    if sendall:
        AIS = aprslib.IS(config['aprs']['callsign'], passwd="-1", host="cwop.aprs.net", port=14580)
        AIS.connect()
        AIS.sendall(packet)
        AIS.close()

    return packet