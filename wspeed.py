from gpiozero import Button
import math
from time import sleep

wind_sensor = Button(6)
wind_count = 0
wind_list = []
ADJUSTMENT = 1.18 # compensate for anemometer factor
delay = 5 # seconds to wait

def calculate_speed():
    while True:
        global wind_list, wind_count
        if wind_count > 0:
            radius_cm = 9.0
            cm_in_mile = 160934.4
            circumference_cm = (2 * math.pi) * radius_cm
            rotations = wind_count / 2.0
            dist_miles = (circumference_cm * rotations) / cm_in_mile
            miles_per_sec = dist_miles / delay # Divide distance by time
            miles_per_hour = (miles_per_sec * 3600) * ADJUSTMENT # miles per second times seconds in an hour
            wind_list.append(miles_per_hour)
            wind_count = 0 # Reset wind count
        sleep(delay)

def spin():
    global wind_count
    wind_count += 1

def monitor_wind():
    wind_sensor.when_pressed = spin