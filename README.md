# Steven Fairchild
	* steve51516@gmail.com
## Create a weather station with a Raspberry pi!

### Hardware Components
1. [CanaKit Raspberry Pi 3 Kit with Clear Case and 2.5A Power Supply](https://www.amazon.com/gp/product/B01C6EQNNK/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
1. [Waveshare BME280 Environmental Sensor, Temperature, Humidity, Barometric Pressure Detection Module I2C/SPI Interface](https://www.amazon.com/gp/product/B07P4CWGGK/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1)
1. [DollaTek PM Sensor SDS011 High Precision PM2.5 Air Quality Detection Sensor Module Super Dust Sensors Digital Output](https://www.amazon.com/gp/product/B07M6JWCWQ/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1)
1. [MakerFocus Raspberry Pi GPIO Extension Board, Raspberry Pi 4 Expansion Board GPIO 1 to 3 for Pi 4B/Pi3/2](https://www.amazon.com/gp/product/B06WWRZ7PS/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
1. [SunFounder DS3231 RTC Real Time Clock Module High Precision for Raspberry Pi Arduino R3 Mega 2560](https://www.amazon.com/gp/product/B00HF4NUSS/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
\
### Power Components
1. [48V POE Injector Adapter Power Supply,10/100Mbps IEEE 802.3af Compliant](https://www.amazon.com/gp/product/B08DHWHQT8/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)
1. [UCTRONICS IEEE 802.3af Micro USB Active PoE Splitter Power Over Ethernet 48V to 5V 2.4A for Tablets, Dropcam or Raspberry Pi (48V to 5V 2.4A)](https://www.amazon.com/gp/product/B01MDLUSE7/ref=ppx_yo_dt_b_asin_title_o03_s02?ie=UTF8&psc=1)
1. [SunFounder Power Supply Module for Raspberry Pi UPS with Recharging Function 5V/3A Lithium Battery Power Pack Expansion Board for Raspberry Pi 4B 3B+ 3B/2B and 1 Model B+](https://www.amazon.com/gp/product/B08HLXGS3W/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)
	* It maybe possible to run completely from battery power and a solar panel. However power optimizations, two 3000 or 3500 mHA batteries, a large solar panel, and a Raspberry pi zero would be ideal for this.
\
### Software used
1. [Arch Linux Arm](https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3)
1. [Original python code copied and modified](https://www.raspberrypi-spy.co.uk/2016/07/using-bme280-i2c-temperature-pressure-sensor-in-python) [Raw script](https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/bme280.py)