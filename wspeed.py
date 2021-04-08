from gpiozero import Button
import math
from time import sleep

wind_sensor = Button(6)
wind_count = 0
wind_list = []

def calculate_speed():
    while True:
        global wind_list; global wind_count
        radius_cm = 9.0
        cm_in_mile = 160934.4
        circumference_cm = (2 * math.pi) * radius_cm
        rotations = wind_count / 2.0
        dist_miles = (circumference_cm * rotations) / cm_in_mile
        speed = dist_miles / 5 # Divide distance by time, 5 seconds
        wind_list.append(speed)
        wind_count = 0 # Reset wind count
        sleep(5)

def wind_avg(wlist):
    try:
        return sum(wlist) / len(wlist)
    except ZeroDivisionError:
        return 0

def spin():
    global wind_count
    wind_count += 1

def monitor_wind():
    wind_sensor.when_pressed = spin