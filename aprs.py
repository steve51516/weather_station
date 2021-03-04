import aprslib
import time
from bme280 import readBME280All

# The first four fields (wind direction, wind speed, temperature and gust) are required,
# in that order, and if a particular measurement is not present, 
# the three numbers should be replaced by "..." to indicate no data available.
def send_data(ztime, temperatureF, barometric_pressure, relative_humidity):
	#ztime = time.strftime('%H%M%S', time.gmtime())
	longitude = ""
	latitude = ""
	wdir = "..." # 3 numbers represents wind direction in degrees from true north. This is the direction that the wind is blowing from.
	avgwind = "..." # 3 numbers represents Average wind speed in MPH
	peakwind = "..." # 3 numbers represents Peak wind speed
	temperatureF = int(temperatureF) # The letter "t" followed by 3 characters (numbers and minus sign) represents the temperature in degrees F.
	rain1h = "..." # The letter "r" followed by 3 numbers represents the amount of rain in hundredths of inches that fell the past hour.
	rain24h = "..." # The letter "p" followed by 3 numbers represents the amount of rain in hundredths of inches that fell in the past 24 hours.

	if temperatureF < 100 and temperatureF > 9: # Add 0 in front if temperature is between 0 and 99
		temperatureF = f"0{temperatureF}"
	elif temperatureF > 9 and temperatureF >= 0: # add 00 in front if between 0 and 9
		temperatureF = f"00{temperatureF}"
	elif temperatureF < 0 and temperatureF > -9:
		temperatureF = f"00{temperatureF}"
	elif temperatureF < -9:
		temperatureF = f"0{temperatureF}"

	barometric_pressure = round(barometric_pressure, 1) # The letter "b" followed by 5 numbers represents the barometric pressure in tenths of a millibar.
	if relative_humidity == 100:
		relative_humidity = "00"
	else:
		relative_humidity = int(relative_humidity) # The letter "h" followed by 2 numbers represents the relative humidity in percent, where "h00" implies 100% RH.


	AIS = aprslib.IS("NOCALL", passwd="-1", host="cwop.aprs.net", port=14580)
	AIS.connect()

	packet = f"NOCALL>APRS,TCPIP*:@{ztime}z{longitude}/{latitude}_{wdir}/{avgwind}g{peakwind}t{temperatureF}r{rain1h}p{rain24h}b{barometric_pressure}h{relative_humidity}"
	AIS.sendall(packet)
	AIS.close()
	return packet

def test():
	ztime = time.strftime('%H%M%S', time.gmtime())
	temperature,pressure,humidity = readBME280All()
	temperatureF = temperature * 1.8 + 32
	packet = send_data(ztime, temperatureF, pressure, humidity)
	print(packet)

if __name__=="__main__":
	test()